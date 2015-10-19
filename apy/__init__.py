# -*- coding: utf-8 -*-

"""
"""

from __future__ import print_function, division

from .scheme.mvn import MavenArtifactoryClient, MavenArtifactoryClientConfig


def new_maven_client(base_url, repo, username=None, password=None):
    config = MavenArtifactoryClientConfig()
    config.base_url = base_url
    config.repo = repo
    config.username = username
    config.password = password

    return MavenArtifactoryClient(config)
