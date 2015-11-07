# -*- coding: utf-8 -*-
#
# Artifacts - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artifacts.api
~~~~~~~~~~~~~

Public API of the Artifacts library.
"""

from __future__ import absolute_import

__all__ = [
    'new_maven_client',
    'MavenArtifactoryClient',
    'MavenArtifactoryClientConfig'
]

from .scheme.mvn import (
    new_maven_client,
    MavenArtifactoryClient,
    MavenArtifactoryClientConfig,
)
