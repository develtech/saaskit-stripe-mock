# -*- coding: utf-8 -*-
import re

import stripe

CUSTOMER_URL_BASE = '{}/v1/customers'.format(stripe.api_base)
CUSTOMER_OBJECT_URL_TPL = '{customer_url_base}/{customer_id}'
CUSTOMER_URL_RE = re.compile(
    CUSTOMER_OBJECT_URL_TPL.format(
        customer_url_base=CUSTOMER_URL_BASE, customer_id='(\w+)'))
CUSTOMER_SOURCE_OBJECT_URL_RE = re.compile(
    r'{}/(\w+)/sources(\w+)'.format(CUSTOMER_URL_BASE))
CUSTOMER_SOURCE_LIST_URL_RE = re.compile(
    r'{}/(\w+)/sources(\?object=(\w+)?)?'.format(CUSTOMER_URL_BASE))
CUSTOMER_SOURCE_OBJECT_URL_TPL = """
{customer_url_base}/{customer_id}/sources/{source_id}
""".strip()
SOURCE_URL_BASE = '{}/v1/sources'.format(stripe.api_base)
SOURCE_URL_RE = re.compile(r'{}/(\w+)'.format(SOURCE_URL_BASE))
PLAN_URL_BASE = '{}/v1/plans'.format(stripe.api_base)
PLAN_URL_RE = re.compile(r'{}/(\w+)'.format(PLAN_URL_BASE))
SUBSCRIPTION_URL_BASE = '{}/v1/subscriptions'.format(stripe.api_base)
SUBSCRIPTION_OBJECT_URL_TPL = '{}/{{subscription_id}}'.format(
    SUBSCRIPTION_URL_BASE)
SUBSCRIPTION_URL_RE = re.compile(r'{}/(\w+)'.format(SUBSCRIPTION_URL_BASE))
CUSTOMER_SUBSCRIPTION_OBJECT_URL_RE = re.compile(
    r'{}/(\w+)/subscriptions/(\w+)'.format(SUBSCRIPTION_URL_BASE))
CUSTOMER_SUBSCRIPTION_LIST_URL_RE = re.compile(
    r'{}/(\w+)/subscriptions(\?limit=(\w+)?)?'.format(CUSTOMER_URL_BASE))
CUSTOMER_SUBSCRIPTION_LIST_URL_TPL = """
{customer_url_base}/{customer_id}/subscriptions
""".strip()
COUPON_URL_BASE = '{}/v1/coupons'.format(stripe.api_base)
COUPON_URL_RE = re.compile(r'{}/(\w+)'.format(COUPON_URL_BASE))
