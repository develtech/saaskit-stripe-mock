# -*- coding: utf-8 -*-

from ..fake import (
    fake_customer,
    fake_customer_source,
    fake_customer_sources,
    fake_customer_subscriptions,
    fake_plan,
    fake_subscription,
)


def test_fake_customer():
    customer_id = 'cus_ok'
    customer = fake_customer(customer_id)
    assert customer['id'] == customer_id


def test_fake_customer_source():
    customer_id = 'cus_ok'
    source_id = 'src_hihi'
    source = fake_customer_source(customer_id, source_id)
    assert source['customer'] == customer_id
    assert source['id'] == source_id


def test_fake_plan():
    plan_id = 'test_plan'
    plan = fake_plan(plan_id)
    assert plan['id'] == plan_id


def test_fake_subscription():
    customer_id = 'cus_ok'
    subscription_id = 'test_subscription'
    subscription = fake_subscription(customer_id, subscription_id)
    assert subscription['id'] == subscription_id


def test_fake_customer_sources():
    customer_id = 'cus_ok'
    source = fake_customer_sources(customer_id, [])
    assert customer_id in source['url']


def test_fake_customer_subscriptions():
    customer_id = 'cus_ok'
    subscription = fake_customer_subscriptions(customer_id, [])
    assert customer_id in subscription['url']
