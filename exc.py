# -*- coding: utf-8 -*-
"""SAASKit Exceptions.

SAASKit uses these typed errors (anything subclassing SAASKitError) as a way
to denote an error propagated from library code.

In some instances, SAASKitError may also propagate contextual information to
allow you to recover. In the instance of _setup_membership, errors propagate
depending on local data being out of synchronization with the payment
processor's
"""


class SAASKitException(Exception):

    """Base exception for execeptions emitted from SAASKit."""
    pass
