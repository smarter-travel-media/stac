# -*- coding: utf-8 -*-
#
# Artifacts - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artifacts.http
~~~~~~~~~~~~~~

Clients and functionality for interacting with portions of the Artifactory JSON
API. It is typically not required for users of the Artifacts library to interact
with this module directly.
"""

from __future__ import absolute_import

import distutils.version

import requests
import artifacts.util


class VersionApiClient(object):
    """Client to get one or multiple versions of a particular artifact.

    This client interacts with the Artifactory API over HTTP or HTTPS.

    This class is thread safe.
    """
    _logger = artifacts.util.get_log()

    def __init__(self, session_factory, url_factory):
        """Set the factory for requests session and factory for API urls.

        :param AuthenticatedSessionFactory session_factory: Factory for new
            :class:`requests.Session` instances, optionally with authentication
            injected.
        :param VersionApiUrlGenerator url_factory: Factory for creating new
            URL and parameter pairs for making requests to the Artifactory API.
        """
        self._session_factory = session_factory
        self._url_factory = url_factory

    def get_most_recent_release(self, group, artifact):
        """Get the version number of the most recent release (non-integration version)
        of a particular group and artifact combination.

        :param str group: Group of the artifact to get the version of
        :param str artifact: Name of the artifact to get the version of
        :return: Version number of the most recent release
        :rtype: str
        :raises requests.exceptions.HTTPError: For any non-success HTTP responses
            from the Artifactory API.
        """
        url, params = self._url_factory.get_latest_version_url(group, artifact)
        self._logger.debug("Using latest version API at %s - params %s", url, params)

        r = self._session_factory().get(url, params=params)
        r.raise_for_status()

        return r.text.strip()

    def get_most_recent_releases(self, group, artifact, limit):
        """Get a list of the version numbers of the most recent releases (non-integration
        versions), ordered by the version number, for a particular group and artifact
        combination.

        :param str group: Group of the artifact to get versions of
        :param str artifact: Name of the artifact to get versions of
        :param limit: Fetch only this many of the most recent releases
        :return: Version numbers of the most recent releases
        :rtype: list
        :raises requests.exceptions.HTTPError: For any non-success HTTP responses
            from the Artifactory API.
        :raises ValueError: If limit is 0 or negative.
        """
        if limit < 1:
            raise ValueError("Releases limit must be positive")

        url, params = self._url_factory.get_all_version_url(group, artifact)
        self._logger.debug("Using all version API at %s - params %s", url, params)

        r = self._session_factory().get(url, params=params)
        r.raise_for_status()

        response = r.json()
        versions = [item['version'] for item in response['results']]
        versions.sort(key=distutils.version.LooseVersion, reverse=True)
        return versions[:limit]


class AuthenticatedSessionFactory(object):
    """Factory for creating new :class:`requests.Session` instances with
    username/password authentication injected if available.

    This class is thread safe.
    """

    def __init__(self, username, password):
        """Set the username and password to use.

        :param str username: Username to use for authentication with
            the Artifactory API. May be ``None``.
        :param str password: Password to use for authentication with
            the Artifactory API. May be ``None``.

        """
        self._username = username
        self._password = password

    def __call__(self):
        """Get a new session with authentication injected, if available.

        :return: New session for making HTTP requests, with authentication
        :rtype: requests.Session
        """
        session = requests.Session()
        if self._username is not None and self._password is not None:
            session.auth = (self._username, self._password)
        return session


class VersionApiUrlGenerator(object):
    """Logic for creating URLs and maps of parameters for making API calls.

    This class is thread safe.
    """

    def __init__(self, base, repo):
        """Set the base Artifactory URL and repository to make API calls against.

        The repository set here will limit the results returned by the API so make
        sure it reflects the types of requests you'll be making. For example, if you
        want to get the most recent release version of an artifact, make sure you
        don't supply an integration artifact repository here.

        :param str base: Base URL to the Artifactory installation
        :param str repo: Artifact repository to generate URLs for

        """
        self._base = base
        self._repo = repo

    def get_latest_version_url(self, group, artifact):
        """Get the full URL and required parameters for getting the latest version
        of an artifact from the Artifactory API.

        :param str group: Group the artifact belongs to. E.g. "com.example.services"
        :param str artifact: Name of the artifact. E.g. "authentication"
        :return: A tuple of a URL string and a dictionary of parameters to include in the
            request to the API
        :rtype: tuple
        """
        url = self._base + '/api/search/latestVersion'
        return url, {'g': group, 'a': artifact, 'repos': self._repo}

    def get_all_version_url(self, group, artifact):
        """Get the full URL and required parameteres for getting all versions of an
        artifact from the Artifactory API.

        :param str group: Group the artifact belongs to. E.g. "com.example.services"
        :param str artifact: Name of the artifact. E.g. "authentication"
        :return: A tuple of a URL string and a dictionary of parameters to include in the
            request to the API
        :rtype: tuple
        """
        url = self._base + '/api/search/versions'
        return url, {'g': group, 'a': artifact, 'repos': self._repo}
