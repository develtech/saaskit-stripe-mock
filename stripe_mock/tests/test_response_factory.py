# -*- coding: utf-8 -*-

import responses
import stripe

from ..factory import StripeMockAPI, add_response
from ..fake import fake_customer


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
