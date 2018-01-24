# -*- coding: utf-8 -*-
"""Functions to generate stripe responses. For use w/ responses.add_callback()
"""
from .patterns import (
    CUSTOMER_URL_RE,
    PLAN_URL_RE,
    SOURCE_URL_RE,
    SUBSCRIPTION_URL_RE,
)


def stripe_object_not_found(object_name, object_id):
    """Return responses callback templated for mimicking response from stripe.

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


def source_not_found(request):
    """Callback for source not being found, for responses.

    :param request: request object from responses
    :type request: :class:`requests.Request`
    :returns: signature required by :meth:`responses.add_callback`
    :rtype: (int, dict, dict) (status, headers, body)
    """
    source_id = SOURCE_URL_RE.match(request.url).group(2)
    return stripe_object_not_found('source', source_id)
