# -*- coding: utf-8 -*-

"""
"""

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
