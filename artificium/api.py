# -*- coding: utf-8 -*-
#
# Artificium - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artificium.api
~~~~~~~~~~~~~~

Public API of the Artifacts library.
"""

from __future__ import absolute_import as _

from .client import (
    new_maven_client,
    ArtifactoryClient,
    MavenArtifactoryClient,
    MavenArtifactoryClientConfig,
)
from .exceptions import (
    ArtifactsError,
    NoMatchingVersionsError
)

__all__ = [
    'new_maven_client',
    'ArtifactoryClient',
    'MavenArtifactoryClient',
    'MavenArtifactoryClientConfig',
    'ArtifactsError',
    'NoMatchingVersionsError'
]
