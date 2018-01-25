# -*- coding: utf-8 -*-
import itertools

import responses

from .fake import (
    fake_coupon,
    fake_coupons,
    fake_customer,
    fake_customer_source,
    fake_customer_sources,
    fake_customer_subscriptions,
    fake_customers,
    fake_plan,
    fake_plans,
    fake_subscription,
    fake_subscriptions,
)
from .helpers import add_callback, add_response
from .patterns import (
    COUPON_URL_BASE,
    COUPON_URL_RE,
    CUSTOMER_SOURCE_URL_RE,
    CUSTOMER_URL_BASE,
    CUSTOMER_URL_RE,
    PLAN_URL_BASE,
    PLAN_URL_RE,
    SOURCE_URL_BASE,
    SOURCE_URL_RE,
    SUBSCRIPTION_URL_BASE,
    SUBSCRIPTION_URL_RE,
)
from .response_callbacks import (
    coupon_not_found,
    customer_not_found,
    customer_source_not_found,
    plan_not_found,
    source_callback_factory,
    source_not_found,
    subscription_not_found,
)


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

    @property
    def sources(self):
        """Return all sources in stripe storage, regardless of customer.

        :returns: list of sources
        :rtype: list[dict]
        """
        return [
            src for src in itertools.chain.from_iterable(
                self.customer_sources.values())
        ]

    def add_customer(self, customer_id, **kwargs):
        """
        If sources exist in kwargs, add_source will be triggered automatically.
        """
        for idx, c in enumerate(self.customers):
            # customer already exists, overwrite properties
            if customer_id == c['id']:
                self.customers[idx].update(kwargs)
                return

        # add customer
        self.customers.append(fake_customer(customer_id, **kwargs))

    def add_source(self, customer_id, source_id, **kwargs):
        """Add a source for a customer ID.

        :param customer_id: customer id to add source for
        :type customer_id: string
        :param source_id: source id to add source for
        :type source_id: string

        Reminder: Stripe sources are always attached customers.

        Behavioral notes:

        If source ID already exists, overwrite properties.
        """

        if customer_id not in self.customer_sources:
            self.customer_sources[customer_id] = []

        for idx, source in enumerate(self.customer_sources[customer_id]):
            # existing source?
            if source_id == source['id']:  # update and return void
                self.customer_sources[customer_id][idx].update(kwargs)
                return

        # new source, append
        self.customer_sources[customer_id].append(
            fake_customer_source(customer_id, source_id, **kwargs))

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

    def add_coupon(self, coupon_id, **kwargs):
        """
        If sources exist in kwargs, add_source will be triggered automatically.
        """
        for idx, c in enumerate(self.coupons):
            # coupon already exists, overwrite properties
            if coupon_id == c.id:
                self.coupons[idx].update(kwargs)
                return

        # add coupon
        self.coupons.append(fake_coupon(coupon_id, **kwargs))

    def add_subscription(self, customer_id, subscription_id, **kwargs):
        """
        If sources exist in kwargs, add_source will be triggered automatically.
        """
        if customer_id not in self.customer_subscriptions:
            self.customer_subscriptions[customer_id] = []

        for idx, subscription in enumerate(
                self.customer_subscriptions[customer_id]):
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
                    '{}/{}'.format(PLAN_URL_BASE, p['id']),
                    p,
                    200,
                )
            add_response(
                'GET',
                PLAN_URL_BASE,
                fake_plans(self.plans),
                200,
            )

        add_callback(
            'GET',
            PLAN_URL_RE,
            plan_not_found,
        )

        if self.coupons:
            for p in self.coupons:
                add_response(
                    'GET',
                    '{}/{}'.format(COUPON_URL_BASE, p['id']),
                    p,
                    200,
                )
            add_response(
                'GET',
                COUPON_URL_BASE,
                fake_coupons(self.coupons),
                200,
            )

        add_callback(
            'GET',
            COUPON_URL_RE,
            coupon_not_found,
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
                    '{}/{}/subscriptions'.format(
                        CUSTOMER_URL_BASE, customer_id),
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
            # sources are different, they can be gotten via Customer,
            # but in some instances, globally.
            for customer_id, sources in self.customer_sources.items():
                for source in sources:
                    print(source['id'])
                    add_response(
                        'GET',
                        '{}/sources/{}'.format(
                            CUSTOMER_URL_BASE, customer_id, source['id']),
                        source,
                        200,
                    )
                    add_response(
                        'GET',
                        '{}/{}'.format(SOURCE_URL_BASE, source['id']),
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
            source_callback_factory(self.sources),
        )

        add_callback(
            'GET',
            SOURCE_URL_RE,
            source_not_found,
        )
        add_callback(
            'GET',
            CUSTOMER_SOURCE_URL_RE,
            customer_source_not_found,
        )

        if self.customers:
            for c in self.customers:
                add_response(
                    'GET',
                    '{}/{}'.format(CUSTOMER_URL_BASE, c['id']),
                    {
                        **c, **{
                            'subscriptions': fake_customer_subscriptions(
                                c['id'],
                                self.customer_subscriptions.get(c['id'], []),
                            ),
                            'sources': fake_customer_sources(
                                c['id'],
                                self.customer_sources.get(c['id'], []),
                            ),
                        }
                    },
                    200,
                )  # yapf: disable
            add_response(
                'GET',
                CUSTOMER_URL_BASE,
                fake_customers(self.customers),
                200,
            )

        # fill in 404's for customers
        add_callback(
            'GET',
            CUSTOMER_URL_RE,
            customer_not_found,
        )
