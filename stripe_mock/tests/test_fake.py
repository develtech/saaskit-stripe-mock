# -*- coding: utf-8 -*-

from ..fake import fake_customer


def test_fake_customer():
    customer_id = 'cus_ok'
    customer = fake_customer(customer_id)
    assert customer['id'] == customer_id
