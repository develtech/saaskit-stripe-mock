# -*- coding: utf-8 -*-
import itertools

import responses

from .fake import (
    fake_coupon,
    fake_coupons,
    fake_customer,
    fake_customer_source,
    fake_customer_source_card,
    fake_customer_source_bank_account,
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
    customer_source_not_found,
    plan_not_found,
    source_callback_factory,
    source_list_callback_factory,
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
        """Add a source attached to customer ID.

        :param customer_id: customer id to add source for
        :type customer_id: string
        :param source_id: source id to add source for
        :type source_id: string

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
            fake_customer_source(customer_id, source_id, **kwargs),
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

        if customer_id not in self.customer_source_cards:
            self.customer_source_cards[customer_id] = []

        for idx, source in enumerate(self.customer_source_cards[customer_id]):
            # existing source?
            if card_id == source['id']:  # update and return void
                self.customer_source_cards[customer_id][idx].update(kwargs)
                return

        # new source, append
        self.customer_source_cards[customer_id].append(
            fake_customer_source_card(customer_id, card_id, **kwargs),
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

        if customer_id not in self.customer_source_bank_accounts:
            self.customer_source_bank_accounts[customer_id] = []

        for idx, source in enumerate(self.customer_source_bank_accounts[customer_id]):
            # existing source?
            if bank_account_id == source['id']:  # update and return void
                self.customer_source_bank_accounts[customer_id][idx].update(kwargs)
                return

        # new source, append
        self.customer_source_bank_accounts[customer_id].append(
            fake_customer_source_bank_account(customer_id, bank_account_id, **kwargs),
        )

    def add_plan(self, plan_id, **kwargs):
        """Add a plan.

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
                    fake_customer_sources(customer_id, sources),
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
