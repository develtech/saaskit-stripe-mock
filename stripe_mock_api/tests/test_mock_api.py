# -*- coding: utf-8 -*-
import pytest

import responses
import stripe

from ..factory import StripeMockAPI


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

    plan_id = 'my_special_plan'
    s.add_plan(plan_id)
    s.sync()

    plan = stripe.Plan.retrieve(plan_id)
    assert plan.id == plan_id

    plan_404_id = 'plan_that_doesnt_exist'
    message = 'No such plan: {}'.format(plan_404_id)
    with pytest.raises(stripe.error.InvalidRequestError, message=message):
        stripe.Plan.retrieve(plan_404_id)
