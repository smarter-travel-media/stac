# -*- coding: utf-8 -*-
#
# Artifacts - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artifacts.path
~~~~~~~~~~~~~~


"""

import artifactory


class AuthenticatedPathFactory(object):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def __call__(self, *args, **kwargs):
        if self._username is not None and self._password is not None:
            kwargs['auth'] = (self._username, self._password)
        return artifactory.ArtifactoryPath(*args, **kwargs)
