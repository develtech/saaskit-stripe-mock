# -*- coding: utf-8 -*-
import itertools

import responses

from .fake import (
    fake_coupon,
    fake_coupon_list,
    fake_customer,
    fake_customer_source,
    fake_customer_source_card,
    fake_customer_source_bank_account,
    fake_customer_source_list,
    fake_customer_subscription_list,
    fake_customer_list,
    fake_plan,
    fake_plan_list,
    fake_subscription,
    fake_subscription_list,
)
from .helpers import add_callback, add_response
from .patterns import (
    COUPON_URL_BASE,
    COUPON_URL_RE,
    CUSTOMER_SOURCE_OBJECT_URL_RE,
    CUSTOMER_SOURCE_LIST_URL_RE,
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
    plan_not_found,
    source_callback_factory,
    source_list_callback_factory,
    subscription_not_found,
)


def _add_object(storage, object_id, fake_fn, **kwargs):
    for idx, c in enumerate(storage):
        if object_id == c.id:  # plan already exists, overwrite properties
            storage[idx].update(kwargs)
            return

    storage.append(fake_fn(object_id, **kwargs))  # add object


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

    def __init__(self):
        self.customers = []
        self.customer_sources = {}
        self.customer_source_cards = {}
        self.customer_source_bank_accounts = {}
        self.customer_subscriptions = {}
        self.customer_discounts = {}
        self.subscription_discounts = {}
        self.coupons = []
        self.plans = []

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
        sources = {}
        for source in self.sources_list:
            customer_id = source['customer']
            if customer_id not in sources:
                sources[customer_id] = []

            sources[customer_id].append(source)
        return sources

    @property
    def sources_list(self):
        """
        Return a list
        """
        return [
            src for src in itertools.chain(
                *self.customer_sources.values(),
                *self.customer_source_cards.values(),
                *self.customer_source_bank_accounts.values(),
            )
        ]

    def _add_customer_object(
        self, customer_id, object_id, object_type, fake_fn, **kwargs,
    ):
        """Generic function for storing / updating a customer-bound object.

        Stripe objects bound to customer's all stored in an instance variable
        where the customer is the key. For instance, for 'subscription'
        object_type::

            self.customer_subscriptions = {
                '{customer_id}': [

                ]
            }
        """

        storage = getattr(self, 'customer_{}s'.format(object_type))
        if customer_id not in storage:
            storage[customer_id] = []

        for idx, subscription in enumerate(storage[customer_id]):
            # existing subscription?
            if kwargs['id'] == subscription['id']:  # update and return void
                storage[customer_id][idx].update(kwargs)
                return

        # new subscription, append
        storage[customer_id].append(
            fake_fn(customer_id, object_id, **kwargs),
        )

    def add_source(self, customer_id, source_id, **kwargs):
        """Add a source attached to customer ID.

        :param customer_id: customer id to add source for
        :type customer_id: string
        :param source_id: source id to add source for
        :type source_id: string

        Behavioral notes:

        If source ID already exists, overwrite properties.
        """
        self._add_customer_object(
            customer_id, source_id, 'source', fake_customer_source,
            **kwargs,
        )

    def add_source_card(self, customer_id, card_id, **kwargs):
        """Add a card source attached to a customer ID.

        :param customer_id: customer id to add source for
        :type customer_id: string
        :param card_id: card id to add source for
        :type card_id: string

        Reminder: Stripe card sources are always attached customers.

        Behavioral notes:

        If card ID already exists, overwrite properties.
        """

        self._add_customer_object(
            customer_id, card_id, 'source_card', fake_customer_source_card,
            **kwargs,
        )

    def add_source_bank_account(self, customer_id, bank_account_id, **kwargs):
        """Add a bank_account source attached to a customer ID.

        :param customer_id: customer id to add source for
        :type customer_id: string
        :param bank_account_id: bank_account id to add source for
        :type bank_account_id: string

        Reminder: Stripe bank_account sources are always attached customers.

        Behavioral notes:

        If bank_account ID already exists, overwrite properties.
        """

        self._add_customer_object(
            customer_id, bank_account_id, 'source_bank_account',
            fake_customer_source_bank_account, **kwargs,
        )

    def add_subscription(self, customer_id, subscription_id, **kwargs):
        """Add / Update a subscription for a customer."""
        self._add_customer_object(
            customer_id, subscription_id, 'subscription', fake_subscription,
            **kwargs,
        )

    def add_plan(self, plan_id, **kwargs):
        """Add / update a plan by id."""
        _add_object(self.plans, plan_id, fake_plan, **kwargs)

    def add_coupon(self, coupon_id, **kwargs):
        """Add / update coupon object."""
        _add_object(self.coupons, coupon_id, fake_coupon, **kwargs)

    def add_customer(self, customer_id, **kwargs):
        """Add / update customer object."""
        _add_object(self.customers, customer_id, fake_customer, **kwargs)

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
                fake_plan_list(self.plans),
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
                fake_coupon_list(self.coupons),
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
                    fake_customer_subscription_list(customer_id, subs),
                    200,
                )

            add_response(
                'GET',
                SUBSCRIPTION_URL_BASE,
                fake_subscription_list(self.subscriptions),
                200,
            )

        add_callback(
            'GET',
            SUBSCRIPTION_URL_RE,
            subscription_not_found,
        )

        if self.sources:
            # sources are different, they can be gotten via Customer,
            # but in some instances, globally.
            for customer_id, sources in self.sources.items():
                for source in sources:
                    add_response(
                        'GET',
                        '{}/{}/sources/{}'.format(
                            CUSTOMER_URL_BASE, customer_id, source['id'],
                        ),
                        source,
                        200,
                    )
                    add_response(
                        'GET',
                        '{}/{}'.format(SOURCE_URL_BASE, source['id']),
                        source,
                        200,
                    )

                # this includes *all sources*
                add_response(
                    'GET',
                    '{}/{}/sources'.format(CUSTOMER_URL_BASE, customer_id),
                    fake_customer_source_list(customer_id, sources),
                    200,
                )

        add_callback(
            'GET',
            SOURCE_URL_RE,
            source_callback_factory(self.sources_list, blocked_objects=['card']),
        )

        add_callback(
            'GET',
            CUSTOMER_SOURCE_OBJECT_URL_RE,
            source_callback_factory(self.sources_list),
        )

        add_callback(
            'GET',
            CUSTOMER_SOURCE_LIST_URL_RE,
            source_list_callback_factory(self.sources_list),
        )

        if self.customers:
            for c in self.customers:
                add_response(
                    'GET',
                    '{}/{}'.format(CUSTOMER_URL_BASE, c['id']),
                    {
                        **c, **{
                            'subscriptions': fake_customer_subscription_list(
                                c['id'],
                                self.customer_subscriptions.get(c['id'], []),
                            ),
                            'sources': fake_customer_source_list(
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
                fake_customer_list(self.customers),
                200,
            )

        # fill in 404's for customers
        add_callback(
            'GET',
            CUSTOMER_URL_RE,
            customer_not_found,
        )
