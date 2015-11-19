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

:mod:`pathlib` like manipulations of Artifactory URLs and paths.
"""

from __future__ import absolute_import

import artifactory


class AuthenticatedPathFactory(object):
    """Callable to create new Artifactory paths with the injected authentication."""

    def __init__(self, username, password):
        """Set the username and password to use when creating new paths

        :param str username: Username to use for auth
        :param str password: Password to use for auth
        """
        self._username = username
        self._password = password

    def __call__(self, *args, **kwargs):
        """Create a new :class:`artifactory.ArtifactoryPath` instance based on the
         given parameters and the injected authentication to use (if any).

        :param args: Positional arguments to pass
        :param kwargs: Keyword arguments to pass
        :return: new Artifactory path with appropriate authentication
        :rtype: artifactory.ArtifactoryPath
        """
        if self._username is not None and self._password is not None:
            kwargs['auth'] = (self._username, self._password)
        return artifactory.ArtifactoryPath(*args, **kwargs)
