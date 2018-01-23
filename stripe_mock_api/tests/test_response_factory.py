# -*- coding: utf-8 -*-
import pytest

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


@responses.activate
def test_stripe_mock_api():
    customer_id = 'cus_hihi'

    s = StripeMockAPI()

    s.add_customer(customer_id)
    s.sync()

    customer = stripe.Customer.retrieve(customer_id)
    assert customer.id == customer_id

    customer_404_id = 'cus_that_doesnt_exist'
    message = 'No such customer: {}'.format(customer_404_id)
    with pytest.raises(stripe.error.InvalidRequestError, message=message):
        stripe.Customer.retrieve(customer_404_id)

    plan_404_id = 'plan_that_doesnt_exist'
    message = 'No such plan: {}'.format(plan_404_id)
    with pytest.raises(stripe.error.InvalidRequestError, message=message):
        stripe.Plan.retrieve(plan_404_id)
