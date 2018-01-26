# -*- coding: utf-8 -*-
import pytest

import responses
import stripe

from ..mock_api import StripeMockAPI


@responses.activate
def test_customers():
    customer_id = 'cus_hihi'

    s = StripeMockAPI()

    s.add_customer(customer_id)
    s.sync()

    customer = stripe.Customer.retrieve(customer_id)
    assert customer.id == customer_id

    assert len(stripe.Customer.list()) == 1

    customer_404_id = 'cus_that_doesnt_exist'
    message = 'No such customer: {}'.format(customer_404_id)
    with pytest.raises(stripe.error.InvalidRequestError, message=message):
        stripe.Customer.retrieve(customer_404_id)


@responses.activate
def test_plans():
    s = StripeMockAPI()
    plan_id = 'my_special_plan'
    s.add_plan(plan_id)
    s.sync()

    plan = stripe.Plan.retrieve(plan_id)
    assert plan.id == plan_id

    assert len(stripe.Plan.list()) == 1

    plan_404_id = 'plan_that_doesnt_exist'
    message = 'No such plan: {}'.format(plan_404_id)
    with pytest.raises(stripe.error.InvalidRequestError, message=message):
        stripe.Plan.retrieve(plan_404_id)


@responses.activate
def test_subscriptions():
    s = StripeMockAPI()
    customer_id = 'cus_hihi'
    subscription_id = 'sub_CAmsLPVVHEQadsfd'
    s.add_subscription(customer_id, subscription_id)
    s.sync()

    subscription = stripe.Subscription.retrieve(subscription_id)
    assert subscription.id == subscription_id

    assert len(stripe.Subscription.list()) == 1

    s.add_customer(customer_id)
    s.sync()
    customer = stripe.Customer.retrieve(customer_id)
    assert len(customer.subscriptions.list()) == 1

    subscription_404_id = 'sub_that_doesnt_exist'
    message = 'No such subscription: {}'.format(subscription_404_id)
    with pytest.raises(stripe.error.InvalidRequestError, message=message):
        stripe.Subscription.retrieve(subscription_404_id)


@responses.activate
def test_sources():
    s = StripeMockAPI()

    customer_id = 'cus_hihi'
    source_id = 'src_CAmsLPVVHEQadsfd'

    s.add_source(customer_id, source_id)
    s.add_customer(customer_id)
    s.sync()

    customer = stripe.Customer.retrieve(customer_id)
    source = stripe.Source.retrieve(source_id)

    assert source.id == source_id
    assert len(customer.sources.list()) == 1

    assert customer.sources.retrieve(source_id)

    source_404_id = 'src_that_doesnt_exist'
    message = 'No such source: {}'.format(source_404_id)
    with pytest.raises(stripe.error.InvalidRequestError, message=message):
        stripe.Source.retrieve(source_404_id)


@responses.activate
def test_cards():
    s = StripeMockAPI()

    customer_id = 'cus_hihi'
    card_id = 'card_CAmsLPVVHEQadsfd'
    s.add_source_card(customer_id, card_id)
    s.add_customer(customer_id)

    s.sync()
    customer = stripe.Customer.retrieve(customer_id)

    assert len(customer.sources.list()) == 1
    s.sync()
    assert len(customer.sources.list(object='card')) == 1
    assert len(customer.sources.list(object='bank_account')) == 0

    assert customer.sources.retrieve(card_id).id == card_id

    source_404_id = 'card_that_doesnt_exist'
    message = 'No such source: {}'.format(source_404_id)
    with pytest.raises(stripe.error.InvalidRequestError, message=message):
        customer.sources.retrieve(source_404_id)


@responses.activate
def test_coupon():
    s = StripeMockAPI()
    coupon_id = 'my_coupon_thing'
    s.add_coupon(coupon_id)
    s.sync()

    coupon = stripe.Coupon.retrieve(coupon_id)
    assert coupon.id == coupon_id

    assert len(stripe.Coupon.list()) == 1

    coupon_404_id = 'coupon_that_doesnt_exist'
    message = 'No such coupon: {}'.format(coupon_404_id)
    with pytest.raises(stripe.error.InvalidRequestError, message=message):
        stripe.Coupon.retrieve(coupon_404_id)
