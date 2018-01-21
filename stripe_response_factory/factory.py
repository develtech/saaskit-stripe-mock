# -*- coding: utf-8 -*-
import json

import responses


def add_response(method, url, body, status):
    """Utility function to register a responses mock.

    - handles setting content_type as json
    - dumps data (dict) to a json-encoded string literal

    :param method: GET, POST, UPDATE, etc.
    :type method: string
    :param url: url
    :type url: string
    :param data: data will be dumped into json string automatically
    :type data: dict
    :param status: http status to return
    :type status: int
    :rtype: void (nothing)
    """
    json_body = json.dumps(body)
    responses.add(
        getattr(responses, method),
        url,
        body=json_body,
        status=status,
        content_type='application/json',
    )
