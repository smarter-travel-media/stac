# -*- coding: utf-8 -*-
#
# Artificium - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artificium.exceptions
~~~~~~~~~~~~~~~~~~~~~

Exceptions raised by the Artifacts library.
"""

from __future__ import print_function, division

__all__ = [
    'ArtifactsError',
    'NoMatchingVersionsError'
]


class ArtifactsError(RuntimeError):
    """Base for exceptions raised by the Artifacts library"""


class NoMatchingVersionsError(RuntimeError):
    """Raised when there is no version or versions matching given criteria"""

    def __init__(self, *args, **kwargs):
        #: Originating exception, likely coming from making a request to the Artifactory
        #: API using the requests library.
        self.cause = kwargs.pop("cause", None)
        super(NoMatchingVersionsError, self).__init__(*args, **kwargs)

    def __str__(self):
        return "{0} {1}".format(super(NoMatchingVersionsError, self).__str__(), self.cause)