# -*- coding: utf-8 -*-
#
# Stac - Smarter Travel Artifactory Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
stac.api
~~~~~~~~

Public API of the Stac library.
"""

from __future__ import absolute_import as _

from .client import (
    new_maven_client,
    ArtifactoryClient,
    GenericArtifactoryClient,
    GenericArtifactoryClientConfig,
    ArtifactUrlGenerator,
    MavenArtifactUrlGenerator
)
from .exceptions import (
    StacError,
    NoMatchingVersionsError
)
from .http import (
    VersionApiDao
)

__all__ = [
    'new_maven_client',
    'ArtifactoryClient',
    'GenericArtifactoryClient',
    'GenericArtifactoryClientConfig',
    'ArtifactUrlGenerator',
    'MavenArtifactUrlGenerator',
    'VersionApiDao',
    'StacError',
    'NoMatchingVersionsError'
]
