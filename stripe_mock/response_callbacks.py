# -*- coding: utf-8 -*-
from .patterns import (
    CUSTOMER_URL_RE,
    PLAN_URL_RE,
    SOURCE_URL_RE,
    SUBSCRIPTION_URL_RE,
)


def customer_not_found(request):
    """Callback for customer not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    customer_id = CUSTOMER_URL_RE.match(request.url).group(1)
    return (
        404, {}, {
            'error': {
                'type': 'invalid_request_error',
                'message': 'No such customer: {}'.format(customer_id),
                'param': 'id'
            }
        })


def plan_not_found(request):
    """Callback for plan not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    plan_id = PLAN_URL_RE.match(request.url).group(1)
    return (
        404, {}, {
            'error': {
                'type': 'invalid_request_error',
                'message': 'No such plan: {}'.format(plan_id),
                'param': 'id'
            }
        })


def subscription_not_found(request):
    """Callback for subscription not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    subscription_id = SUBSCRIPTION_URL_RE.match(request.url).group(1)
    return (
        404, {}, {
            'error': {
                'type': 'invalid_request_error',
                'message': 'No such subscription: {}'.format(subscription_id),
                'param': 'id'
            }
        })


def source_not_found(request):
    """Callback for source not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    source_id = SOURCE_URL_RE.match(request.url).group(2)
    return (
        404, {}, {
            'error': {
                'type': 'invalid_request_error',
                'message': 'No such source: {}'.format(source_id),
                'param': 'id'
            }
        })
