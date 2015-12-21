# -*- coding: utf-8 -*-
#
# Stac - Smarter Travel Artifactory Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
stac.exceptions
~~~~~~~~~~~~~~~

Exceptions raised by the Stac library.
"""

from __future__ import print_function, division

__all__ = [
    'StacError',
    'NoMatchingVersionsError'
]


class StacError(RuntimeError):
    """Base for exceptions raised by the Stac library"""


class NoMatchingVersionsError(RuntimeError):
    """Raised when there is no version or versions matching given criteria"""

    def __init__(self, *args, **kwargs):
        #: Originating exception, likely coming from making a request to the Artifactory
        #: API using the requests library.
        self.cause = kwargs.pop("cause", None)
        super(NoMatchingVersionsError, self).__init__(*args, **kwargs)

    def __str__(self):
        if self.cause is not None:
            return "{0} {1}".format(super(NoMatchingVersionsError, self).__str__(), self.cause)
        return super(NoMatchingVersionsError, self).__str__()
