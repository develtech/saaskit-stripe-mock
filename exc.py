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

Another benefit of this is SAASKitException supports wrapping the original
exception, should one exist. In payment processor exceptions, exceptions also
can come from requests (a dependency used when stripe library is making API
calls).

Suggestion: Examine setup_membership()'s default behavior for handling cases.

Other Idea: Have a command to create plans on the payment processor side.
"""


class SAASKitException(Exception):

    """Base exception for execeptions emitted from SAASKit."""
    pass


class RemoteCustomerNotFound(SAASKitException):
    """Customer in local database doesn't exist on payment processor's side.

    Troubleshooting:

    Log into the payment processor and determine if the customer's account
    is a subscriber.

    - Did prior manual intervention by a colleague leave the local customer ID
      association out of sync? If so, update it manually.

    - Are the Django configuration settings targetting the correct API
      environment? If a testing API key is being used in database synchronized
      for production records, or vice versa, fix the settings.

    - Verify if the wrong environment's could have been sync'd to the database.
      Did you synchronize production stripe API information on a local server?

      Check to see if the customer is livemode (True for production, False for
      tests)

      You may want to delete the local copies of API data synchronized from
      the wrong mode, but if you correctly lookup via livemode, the issue
      should be fixed.
    """
    pass


class RemoteMultipleCustomersFound(SAASKitException):
    """Exception raised if multiple customers are found for the same email.
    To resolve this, pick the correct customer.
    """
    pass


class RemoteCustomerAlreadyExists(SAASKitException):
    pass
