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
    'StacNoMatchingVersionsError'
]


class StacError(RuntimeError):
    """Base for exceptions raised by the Stac library"""


class StacNoMatchingVersionsError(RuntimeError):
    """Raised when there is no version or versions matching given criteria"""

    def __init__(self, *args, **kwargs):
        #: Originating exception, likely coming from making a request to the Artifactory
        #: API using the requests library.
        self.cause = kwargs.pop("cause", None)
        super(StacNoMatchingVersionsError, self).__init__(*args, **kwargs)

    def __str__(self):
        return "{0} {1}".format(super(StacNoMatchingVersionsError, self).__str__(), self.cause)
