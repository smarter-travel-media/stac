# -*- coding: utf-8 -*-

"""
"""

from __future__ import print_function, division

import requests

from .scheme.mvn import MavenArtifactoryClient, MavenArtifactoryClientConfig

def new_maven_client(base_url=None, repo=None, username=None, password=None):
    config = MavenArtifactoryClientConfig()
    config.base_url = base_url
    config.repo = repo
    config.username = username
    config.password = password
    config.session = requests.Session()

    return MavenArtifactoryClient(config)
