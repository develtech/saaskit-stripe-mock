# -*- coding: utf-8 -*-
import re

import responses
import stripe

from .fake import (
    fake_customer,
    fake_customer_source,
    fake_customer_sources,
    fake_customer_subscriptions,
    fake_plan,
    fake_subscription,
    fake_subscriptions,
)
from .helpers import add_callback, add_response

CUSTOMER_URL_BASE = '{}/v1/customers'.format(stripe.api_base)
CUSTOMER_URL_RE = re.compile(r'{}/(\w+)'.format(CUSTOMER_URL_BASE))
SOURCE_URL_BASE = '{}/sources/'.format(CUSTOMER_URL_BASE)
SOURCE_URL_RE = re.compile(r'{}/(\w+)'.format(CUSTOMER_URL_RE))
PLAN_URL_BASE = '{}/v1/plans/'.format(stripe.api_base)
PLAN_URL_RE = re.compile(r'{}(\w+)'.format(PLAN_URL_BASE))
SUBSCRIPTION_URL_BASE = '{}/v1/subscriptions'.format(stripe.api_base)
SUBSCRIPTION_URL_RE = re.compile(r'{}/(\w+)'.format(SUBSCRIPTION_URL_BASE))


def customer_not_found(request):
    """Callback for customer not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    customer_id = CUSTOMER_URL_RE.match(request.url).group(1)
    return (
        404, {}, {
            'error': {
                'type': 'invalid_request_error',
                'message': 'No such customer: {}'.format(customer_id),
                'param': 'id'
            }
        })


def plan_not_found(request):
    """Callback for plan not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    plan_id = PLAN_URL_RE.match(request.url).group(1)
    return (
        404, {}, {
            'error': {
                'type': 'invalid_request_error',
                'message': 'No such plan: {}'.format(plan_id),
                'param': 'id'
            }
        })


def subscription_not_found(request):
    """Callback for subscription not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    subscription_id = SUBSCRIPTION_URL_RE.match(request.url).group(1)
    return (
        404, {}, {
            'error': {
                'type': 'invalid_request_error',
                'message': 'No such subscription: {}'.format(subscription_id),
                'param': 'id'
            }
        })


def source_not_found(request):
    """Callback for source not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    source_id = SOURCE_URL_RE.match(request.url).group(2)
    return (
        404, {}, {
            'error': {
                'type': 'invalid_request_error',
                'message': 'No such source: {}'.format(source_id),
                'param': 'id'
            }
        })


class StripeMockAPI(object):

    """Sets responses against the stripe API with dummy data.

    In addition to providing an API for adding stripe data and mocking
    network calls in requests (via responses), it acts a storage object for
    customers, plans, and sources.

    Mocks by setting/deleting the responses singleton object.

    - Adding objects also not only updates GET id-lookups, but also listing
      objects.
    - When adding stripe responses, other information will be filled in by
      default data.

    Other benefits:

    - No needs to worry about URL's
    - No need to worry about encoding
    - Automatically creates mocks for empty stripe resources (instead of
      raising ConnectionError).

      - TODO: Including pattern matchings
        https://github.com/getsentry/responses/pull/25

        for instances where a GET id for a customer/plan doesn't exist

    Without this factory object, tests need to repeat this every process every
    single time.

    Usage:
        s = StripeResponses()

    """
    customers = []
    customer_sources = {}
    customer_subscriptions = {}
    customer_discounts = {}
    subscription_discounts = {}
    coupons = []
    plans = []

    @property
    def subscriptions(self):
        """Return all subscriptions in stripe storage, regardless of customer.

        :returns: list of subscriptions
        :rtype: list[dict]
        """
        return [
            sub for sub in
            [subs for _, subs in self.customer_subscriptions.items()]
        ]

    def add_customer(self, customer_id, **kwargs):
        """
        If sources exist in kwargs, add_source will be triggered automatically.
        """
        for idx, c in enumerate(self.customers):
            # customer already exists, overwrite properties
            if customer_id == c.id:
                self.customers[idx].update(kwargs)
                return

        # add customer
        self.customers.append(fake_customer(customer_id, **kwargs))

    def add_source(self, customer_id, **kwargs):
        """Add a source for a customer ID.

        :param customer_id: customer id to add source for
        :type customer_id: string

        Reminder: Stripe sources are always attached customers.

        Behavioral notes:

        If source ID already exists, overwrite properties.
        """

        if customer_id not in self.customer_sources:
            self.customer_sources[customer_id] = []

        for idx, source in enumerate(self.customer_sources[customer_id]):
            # existing source?
            if kwargs['id'] == source['id']:  # update and return void
                self.customer_sources[customer_id][idx].update(kwargs)
                return

        # new source, append
        self.customer_sources[customer_id].append(
            fake_customer_source(customer_id, **kwargs))

    def add_plan(self, plan_id, **kwargs):
        """
        If sources exist in kwargs, add_source will be triggered automatically.
        """
        for idx, c in enumerate(self.plans):
            # plan already exists, overwrite properties
            if plan_id == c.id:
                self.plans[idx].update(kwargs)
                return

        # add plan
        self.plans.append(fake_plan(plan_id, **kwargs))

    def add_subscription(self, customer_id, subscription_id, **kwargs):
        """
        If sources exist in kwargs, add_source will be triggered automatically.
        """
        if customer_id not in self.customer_subscriptions:
            self.customer_subscriptions[customer_id] = []

        for idx, subscription in enumerate(self.customer_subscriptions[customer_id]):
            # existing subscription?
            if kwargs['id'] == subscription['id']:  # update and return void
                self.customer_subscriptions[customer_id][idx].update(kwargs)
                return

        # new subscription, append
        self.customer_subscriptions[customer_id].append(
            fake_subscription(subscription_id, customer_id, **kwargs),
        )

    def sync(self):  # NOQA C901
        """Clear and recreate all responses based on stripe objects."""

        responses.reset()

        if self.plans:
            for p in self.plans:
                add_response(
                    'GET',
                    '{}{}'.format(PLAN_URL_BASE, p['id']),
                    p,
                    200,
                )

        add_callback(
            'GET',
            PLAN_URL_RE,
            plan_not_found,
        )

        if self.customer_subscriptions:
            for customer_id, subs in self.customer_subscriptions.items():
                for sub in subs:
                    add_response(
                        'GET',
                        '{}/{}'.format(SUBSCRIPTION_URL_BASE, sub['id']),
                        sub,
                        200,
                    )
                add_response(
                    'GET',
                    '{}/{}/subscriptions'.format(CUSTOMER_URL_BASE, customer_id),
                    fake_customer_subscriptions(customer_id, subs),
                    200,
                )

            add_response(
                'GET',
                SUBSCRIPTION_URL_BASE,
                fake_subscriptions(self.subscriptions),
                200,
            )

        add_callback(
            'GET',
            SUBSCRIPTION_URL_RE,
            subscription_not_found,
        )

        if self.customer_sources:
            for customer_id, sources in self.customer_sources.items():
                for source in sources:
                    add_response(
                        'GET',
                        '{}{}'.format(SOURCE_URL_BASE, source['id']),
                        source,
                        200,
                    )
                add_response(
                    'GET',
                    '{}/{}/sources'.format(CUSTOMER_URL_BASE, customer_id),
                    fake_customer_sources(customer_id, sources),
                    200,
                )

        add_callback(
            'GET',
            SOURCE_URL_RE,
            source_not_found,
        )

        if self.customers:
            for c in self.customers:
                add_response(
                    'GET',
                    '{}/{}'.format(CUSTOMER_URL_BASE, c['id']),
                    c,
                    200,
                )

        # fill in 404's for customers
        add_callback(
            'GET',
            CUSTOMER_URL_RE,
            customer_not_found,
        )
