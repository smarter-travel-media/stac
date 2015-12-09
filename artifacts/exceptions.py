# -*- coding: utf-8 -*-
#
# Artifacts - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artifacts.exceptions
~~~~~~~~~~~~~~~~~~~~

Exceptions raised by the Artifacts library.
"""

from __future__ import print_function, division


class ArtifactsError(RuntimeError):
    """Base for all exceptions raised by the Artifacts library"""


class ArtifactoryApiError(ArtifactsError):
    """Root for errors interacting with the Artifactory REST API"""

    def __init__(self, *args, **kwargs):
        #: HTTP status code returned by the Artifactory REST API
        self.code = kwargs.pop('code', None)

        #: URL used for making a request to the Artifactory REST API
        self.url = kwargs.pop('url', None)

        super(ArtifactoryApiError, self).__init__(*args, **kwargs)


class NoReleaseArtifactsError(ArtifactoryApiError):
    """There were no release artifacts for the project in the given repository"""


class NoArtifactVersionsError(ArtifactoryApiError):
    """There were no versions for the project in the given repository"""
