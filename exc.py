# -*- coding: utf-8 -*-
"""SAASKit Exceptions.

SAASKit uses these typed errors (anything subclassing SAASKitError) as a way
to denote an error propagated from library code.

In some instances, SAASKitError may also propagate contextual information to
allow you to recover. In the instance of _setup_membership, errors propagate
depending on local data being out of synchronization with the payment
processor's copy of data.

Try/catch in Python is powerful. You can use a parent class of the exception,
such as SAASKitException, as a catch-all exception for more specific situations.

Suggestion: Examine setup_membership()'s default behavior for handling cases.

Other Idea: Have a command to create plans on the payment processor side.
"""


class SAASKitException(Exception):

    """Base exception for execeptions emitted from SAASKit."""
    pass
