# -*- coding: utf-8 -*-
import responses
import stripe

from ..fake import fake_customer
from ..helpers import add_callback, add_response


@responses.activate
def test_add_response():
    customer_id = 'cus_hihi'
    add_response(
        'GET',
        '{}/v1/customers/{}'.format(stripe.api_base, customer_id),
        fake_customer(customer_id),
        200,
    )

    customer = stripe.Customer.retrieve(customer_id)
    assert customer.id == customer_id


@responses.activate
def test_add_callback():
    customer_id = 'cus_hihi'
    add_callback(
        'GET',
        '{}/v1/customers/{}'.format(stripe.api_base, customer_id),
        lambda request: (200, {}, fake_customer(customer_id)),
    )

    customer = stripe.Customer.retrieve(customer_id)
    assert customer.id == customer_id
