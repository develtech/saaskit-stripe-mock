# -*- coding: utf-8 -*-
"""Functions to generate stripe responses. For use w/ responses.add_callback()
"""
from .fake import fake_customer_sources
from .patterns import (
    COUPON_URL_RE,
    CUSTOMER_SOURCE_LIST_URL_RE,
    CUSTOMER_SOURCE_OBJECT_URL_RE,
    CUSTOMER_URL_RE,
    PLAN_URL_RE,
    SOURCE_URL_RE,
    SUBSCRIPTION_URL_RE,
)


def stripe_object_not_found(object_name, object_id):
    """Return responses callback templated for mimicking response from stripe.

    :param object_name: name of stripe object, e.g. 'card', 'customer'
    :type object_name: string
    :param object_id: id of stripe object, e.g. 'cus_Bwrbeyo88aaUYP'
    :type object_id: string
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    return (
        404, {}, {
            'error': {
                'type': 'invalid_request_error',
                'message': 'No such {}: {}'.format(object_name, object_id),
                'param': 'id'
            }
        })


def customer_not_found(request):
    """Callback for customer not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    customer_id = CUSTOMER_URL_RE.match(request.url).group(1)
    return stripe_object_not_found('customer', customer_id)


def plan_not_found(request):
    """Callback for plan not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    plan_id = PLAN_URL_RE.match(request.url).group(1)
    return stripe_object_not_found('plan', plan_id)


def subscription_not_found(request):
    """Callback for subscription not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    subscription_id = SUBSCRIPTION_URL_RE.match(request.url).group(1)
    return stripe_object_not_found('subscription', subscription_id)


def customer_source_not_found(request):
    """Callback for source not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    source_id = CUSTOMER_SOURCE_OBJECT_URL_RE.match(request.url).group(2)
    return stripe_object_not_found('source', source_id)


def source_not_found(request):
    """Callback for source not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    source_id = SOURCE_URL_RE.match(request.url).group(1)

    return stripe_object_not_found('source', source_id)


def coupon_not_found(request):
    """Callback for coupon not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    coupon_id = COUPON_URL_RE.match(request.url).group(1)
    return stripe_object_not_found('coupon', coupon_id)


def source_callback_factory(source_list, blocked_objects=[]):
    """A factory to create a callback to handle sources.

    Filters out cards, wich do not fit this URL schema.

    This is needed to handle the incongruency between GET with sources and
    cards.

    Card's are accessible via /v1/customers/{customer_id}/sources.

    :param source_list: list of source data
    :type source_list: list[dict]
    :returns: response of data immitating stripe's listing
    :rtype: dict
    """
    cleaned_sources = [
        source for source in source_list if source['object'] not in blocked_objects
    ]

    def request_callback(request):
        print('hi', request.url)
        source_id = SOURCE_URL_RE.match(request.url).group(1)
        for source in cleaned_sources:
            if source_id == source['id']:
                return (200, {}, source)
        return stripe_object_not_found('source', source_id)

    return request_callback


def source_list_callback_factory(source_list):
    """A factory to create a callback to handle sources for customer.

    Handles ?object=(card|bank_account) if exists.

    This is needed to handle the incongruency between GET with sources and
    cards.

    Card's are accessible via /v1/customers/{customer_id}/sources.

    :param source_list: list of source data
    :type source_list: list[dict]
    :returns: response of data immitating stripe's listing
    :rtype: dict
    """

    def request_callback(request):
        customer_id = CUSTOMER_SOURCE_LIST_URL_RE.match(request.url).group(1)
        object_type = CUSTOMER_SOURCE_LIST_URL_RE.match(request.url).group(3)
        cleaned_sources = [
            source for source in source_list if source['object'] == object_type
        ]
        response = fake_customer_sources(customer_id, cleaned_sources)
        return (200, {}, response)

    return request_callback
