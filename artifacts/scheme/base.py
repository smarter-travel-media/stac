# -*- coding: utf-8 -*-
#
# Artifacts - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artifacts.scheme.base
~~~~~~~~~~~~~~~~~~~~~

Interface for clients that interact with Artifactory.
"""

from __future__ import absolute_import

from abc import ABCMeta, abstractmethod

DEFAULT_RELEASE_LIMIT = 5


class ArtifactoryClient(object):
    """Interface for getting artifact paths based on an artifact name.

    How artifact names and descriptors are interpreted is implementation
    specific and typically based on a particular repository layout. For example
    a Maven layout based client would use ``full_name`` for the full group and
    artifact (e.g. 'com.example.project.service'). While a Python layout based
    client would use ``full_name`` as unique name in a flat namespace (e.g
    'my-project').
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_release(self, full_name, version, descriptor=None):
        """Get the path to a specific release of the given project, optionally using
        a descriptor to get a particular variant of the release (associated sources vs
        the actual application for example). How the ``full_name`` and ``descriptor``
        are used is implementation dependent.

        :param str full_name: Fully qualified name of the artifact to get the path of.
        :param str version: Version of the artifact to get the path of.
        :param str descriptor: Tag to get a particular variant of a release.
        :return: Artifactory URL/path to the artifact with given name and version
        :rtype: artifactory.ArtifactoryPath
        """

    @abstractmethod
    def get_latest_release(self, full_name, descriptor=None):
        """Get the path to the most recent release of the given project, optionally using
        a descriptor to get a particular variant of the release (associated sources vs the
        actual application for example). How the ``full_name`` and ``descriptor`` are used
        is implementation dependent.

        :param str full_name: Fully qualified name of the artifact to get the path of.
        :param str descriptor: Tag to get a particular variant of a release.
        :return: Artifactory URL/path to the artifact with given name
        :rtype: artifactory.ArtifactoryPath
        """

    @abstractmethod
    def get_latest_releases(self, full_name, descriptor=None, limit=DEFAULT_RELEASE_LIMIT):
        """Get the paths to the most recent releases of the given project, optionally using
        a descriptor to get a particular variant of the releases (associated sources vs the
        actual application for example). How the ``full_name`` and ``descriptor`` are used
        is implementation dependent.

        :param str full_name: Full qualified name of the artifacts to get the path of.
        :param str descriptor: Tag to get a particular variant of each release
        :param int limit: Only get the ``limit`` most recent releases.
        :return: Artifactory URL/path to each of the most recent artifacts with the
            given name
        :rtype: list
        """
