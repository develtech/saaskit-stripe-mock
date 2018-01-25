# -*- coding: utf-8 -*-
import re

import stripe

CUSTOMER_URL_BASE = '{}/v1/customers'.format(stripe.api_base)
CUSTOMER_URL_RE = re.compile(r'{}/(\w+)'.format(CUSTOMER_URL_BASE))
CUSTOMER_SOURCE_URL_BASE = '{}/sources'.format(CUSTOMER_URL_BASE)
CUSTOMER_SOURCE_URL_RE = re.compile(r'{}/sources/(\w+)'.format(CUSTOMER_URL_RE))
SOURCE_URL_BASE = '{}/v1/sources'.format(stripe.api_base)
SOURCE_URL_RE = re.compile(r'{}/(\w+)'.format(SOURCE_URL_BASE))
PLAN_URL_BASE = '{}/v1/plans'.format(stripe.api_base)
PLAN_URL_RE = re.compile(r'{}/(\w+)'.format(PLAN_URL_BASE))
SUBSCRIPTION_URL_BASE = '{}/v1/subscriptions'.format(stripe.api_base)
SUBSCRIPTION_URL_RE = re.compile(r'{}/(\w+)'.format(SUBSCRIPTION_URL_BASE))
COUPON_URL_BASE = '{}/v1/coupons'.format(stripe.api_base)
COUPON_URL_RE = re.compile(r'{}/(\w+)'.format(COUPON_URL_BASE))
