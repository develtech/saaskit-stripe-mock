# -*- coding: utf-8 -*-
import re

import stripe

CUSTOMER_URL_BASE = '{}/v1/customers'.format(stripe.api_base)
CUSTOMER_URL_RE = re.compile(r'{}/(\w+)'.format(CUSTOMER_URL_BASE))
SOURCE_URL_BASE = '{}/sources/'.format(CUSTOMER_URL_BASE)
SOURCE_URL_RE = re.compile(r'{}/(\w+)'.format(CUSTOMER_URL_RE))
PLAN_URL_BASE = '{}/v1/plans/'.format(stripe.api_base)
PLAN_URL_RE = re.compile(r'{}(\w+)'.format(PLAN_URL_BASE))
SUBSCRIPTION_URL_BASE = '{}/v1/subscriptions'.format(stripe.api_base)
SUBSCRIPTION_URL_RE = re.compile(r'{}/(\w+)'.format(SUBSCRIPTION_URL_BASE))
