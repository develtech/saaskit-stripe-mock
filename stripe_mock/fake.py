# -*- coding: utf-8 -*-
"""Functions for generating response bodies from stripe API."""
from faker import Faker


def fake_empty_sources(customer_id):
    return {
        'data': [],
        'has_more': False,
        'object': 'list',
        'total_count': 0,
        'url': '/v1/customers/{}/sources'.format(customer_id),
    }


def fake_customer(customer_id, **kwargs):
    return {**{
        'account_balance': 0,
        'created': 1513262366,
        'currency': 'usd',
        'default_source': 'card_1BYxtEEzushJqDoiJUQkSyER',
        'delinquent': False,
        'description': 'Test user',
        'discount': None,
        'email': 'tony@local.com',
        'id': customer_id,
        'livemode': False,
        'metadata': {},
        'object': 'customer',
        'shipping': None,
        'sources': fake_empty_sources(customer_id)
    }, **kwargs}


def fake_source(customer_id, **kwargs):

    return {**{
        'address_city': 'new york',
        'address_country': 'usa',
        'address_line1': 'McAllister St',
        'address_line1_check': 'pass',
        'address_line2': None,
        'address_state': 'ny',
        'address_zip': '10013',
        'address_zip_check': 'pass',
        'brand': 'Visa',
        'country': 'US',
        'customer': customer_id,
        'cvc_check': 'pass',
        'dynamic_last4': None,
        'exp_month': 4,
        'exp_year': 2032,
        'fingerprint': 'ZX4L088dUFClwtPD',
        'funding': 'credit',
        'id': 'card_1BYxtEEzushJqDoiJUQkSyER',
        'last4': '4242',
        'metadata': {},
        'name': 'John Doe',
        'object': 'card',
        'tokenization_method': None,
    }, **kwargs}
