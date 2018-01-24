# -*- coding: utf-8 -*-
"""Functions for generating response bodies from stripe API."""
from faker import Faker


def fake_subscriptions(subscription_list):
    """Fake the subscription listings (globally).

    :param subscription_list: list of subscription data
    :type subscription_list: list[dict]
    :returns: response of data immitating stripe's listing
    :rtype: dict
    """
    return {
        'data': subscription_list,
        'has_more': False,
        'object': 'list',
        'total_count': len(subscription_list),
        'url': '/v1/subscriptions',
    }


def fake_coupons(coupon_list):
    """Fake the coupon listings (globally).

    :param coupon_list: list of coupon data
    :type coupon_list: list[dict]
    :returns: response of data immitating stripe's listing
    :rtype: dict
    """
    return {
        'data': coupon_list,
        'has_more': False,
        'object': 'list',
        'total_count': len(coupon_list),
        'url': '/v1/coupons',
    }


def fake_customers(customer_list):
    """Fake the customer listings (globally).

    :param customer_list: list of customer data
    :type customer_list: list[dict]
    :returns: response of data immitating stripe's listing
    :rtype: dict
    """
    return {
        'data': customer_list,
        'has_more': False,
        'object': 'list',
        'total_count': len(customer_list),
        'url': '/v1/customers',
    }


def fake_plans(plan_list):
    """Fake the plan listings (globally).

    :param plan_list: list of plan data
    :type plan_list: list[dict]
    :returns: response of data immitating stripe's listing
    :rtype: dict
    """
    return {
        'data': plan_list,
        'has_more': False,
        'object': 'list',
        'total_count': len(plan_list),
        'url': '/v1/plans',
    }


def fake_customer_subscriptions(customer_id, subscription_list):
    """Fake the subscription listings for a customer.

    :param customer_id: stripe customer id
    :type customer_id: string
    :param subscription_list: list of subscription data
    :type subscription_list: list[dict]
    :returns: response of data immitating stripe's listing
    :rtype: dict
    """
    return {
        'data': subscription_list,
        'has_more': False,
        'object': 'list',
        'total_count': len(subscription_list),
        'url': '/v1/customers/{}/subscriptions'.format(customer_id),
    }


def fake_customer_sources(customer_id, source_list):
    """Fake the source listings for a customer.

    :param customer_id: stripe customer id
    :type customer_id: string
    :param source_list: list of source data
    :type source_list: list[dict]
    :returns: response of data immitating stripe's listing
    :rtype: dict
    """
    return {
        'data': source_list,
        'has_more': False,
        'object': 'list',
        'total_count': len(source_list),
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
        'sources': fake_customer_sources(customer_id, [])
    }, **kwargs}


def fake_coupon(coupon_id, **kwargs):
    return {**{
        'amount_off': 1500,
        'created': 1513532343,
        'currency': 'usd',
        'duration': 'once',
        'duration_in_months': None,
        'id': coupon_id,
        'livemode': False,
        'max_redemptions': 5,
        'metadata': {},
        'object': 'coupon',
        'percent_off': None,
        'redeem_by': 1515650399,
        'times_redeemed': 1,
        'valid': True
    }, **kwargs}


def fake_customer_discount(customer_id, subscription_id=None, **kwargs):
    return {**{
        'coupon': fake_coupon('my-coupon'),
        'customer': customer_id,
        'end': None,
        'object': 'discount',
        'start': 1513532388,
        'subscription': subscription_id,
    }, **kwargs}


def fake_customer_source(customer_id, **kwargs):
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


def fake_plan(plan_id, **kwargs):
    return {**{
        'amount': 999,
        'created': 1513273051,
        'currency': 'usd',
        'id': plan_id,
        'interval': 'month',
        'interval_count': 1,
        'livemode': False,
        'metadata': {},
        'name': 'Devel.tech 9.99',
        'object': 'plan',
        'statement_descriptor': None,
        'trial_period_days': None
    }, **kwargs}


def fake_subscription(subscription_id, customer_id, **kwargs):
    return {**{
        'application_fee_percent': None,
        'billing': 'charge_automatically',
        'cancel_at_period_end': False,
        'canceled_at': None,
        'created': 1513273056,
        'current_period_end': 1515951456,
        'current_period_start': 1513273056,
        'customer': customer_id,
        'days_until_due': None,
        'discount': {
            'coupon': {
                'amount_off': 1500,
                'created': 1513532343,
                'currency': 'usd',
                'duration': 'once',
                'duration_in_months': None,
                'id': '15-off',
                'livemode': False,
                'max_redemptions': 5,
                'metadata': {},
                'object': 'coupon',
                'percent_off': None,
                'redeem_by': 1515650399,
                'times_redeemed': 2,
                'valid': True
            },
            'customer': 'cus_Bwrbeyo88aaUYP',
            'end': None,
            'object': 'discount',
            'start': 1513532569,
            'subscription': 'sub_BwuTCVDt1Klbil'
        },
        'ended_at': None,
        'id': subscription_id,
        'items': {
            'data': [{
                'created': 1513273056,
                'id': 'si_BwuToPkPLdw9g0',
                'metadata': {},
                'object': 'subscription_item',
                'plan': {
                    'amount': 999,
                    'created': 1513273051,
                    'currency': 'usd',
                    'id': 'develtech_999',
                    'interval': 'month',
                    'interval_count': 1,
                    'livemode': False,
                    'metadata': {},
                    'name': 'Devel.tech 9.99',
                    'object': 'plan',
                    'statement_descriptor': None,
                    'trial_period_days': None
                },
                'quantity': 1
            }],
            'has_more': False,
            'object': 'list',
            'total_count': 1,
            'url': '/v1/subscription_items?subscription=sub_BwuTCVDt1Klbil'
        },
        'livemode': False,
        'metadata': {},
        'object': 'subscription',
        'plan': {
            'amount': 999,
            'created': 1513273051,
            'currency': 'usd',
            'id': 'develtech_999',
            'interval': 'month',
            'interval_count': 1,
            'livemode': False,
            'metadata': {},
            'name': 'Devel.tech 9.99',
            'object': 'plan',
            'statement_descriptor': None,
            'trial_period_days': None
        },
        'quantity': 1,
        'start': 1513273056,
        'status': 'active',
        'tax_percent': None,
        'trial_end': None,
        'trial_start': None
    }, **kwargs}
