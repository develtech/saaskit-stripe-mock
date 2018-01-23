# -*- coding: utf-8 -*-

from ..fake import fake_customer, fake_empty_sources, fake_source, fake_plan


def test_fake_customer():
    customer_id = 'cus_ok'
    customer = fake_customer(customer_id)
    assert customer['id'] == customer_id


def test_fake_source():
    customer_id = 'cus_ok'
    source = fake_source(customer_id)
    assert source['customer'] == customer_id


def test_fake_plan():
    plan_id = 'test_plan'
    plan = fake_plan(plan_id)
    assert plan['id'] == plan_id


def test_fake_empty_sources():
    customer_id = 'cus_ok'
    source = fake_empty_sources(customer_id)
    assert customer_id in source['url']
