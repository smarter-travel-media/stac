# -*- coding: utf-8 -*-
#
# Stac - Smarter Travel Artifactory Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
stac.http
~~~~~~~~~

Clients and functionality for interacting with portions of the Artifactory JSON
API. It is typically not required for users of the Stac library to interact
with this module directly.
"""

from __future__ import absolute_import

import distutils.version

import stac.exceptions
import stac.util


class VersionApiDao(object):
    """HTTP DAO to get one or multiple versions of a particular artifact.

    This DAO interacts with the Artifactory API over HTTP or HTTPS.

    This class is thread safe.
    """
    _logger = stac.util.get_log()

    def __init__(self, session, base_url, repo):
        """Set the factory for requests session and factory for API urls.

        :param requests.Session session: Session for making HTTP requests to
            the Artifactory API. This session should be configured with any required
            credentials for accessing the API.
        :param str|unicode base_url: Base URL to the Artifactory installation
        :param str|unicode repo: Name of repository to search against.
        """
        self._session = session
        self._base_url = base_url
        self._repo = repo

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
        url = self._base_url + '/api/search/latestVersion'
        params = {'g': group, 'a': artifact, 'repos': self._repo}
        self._logger.debug("Using latest version API at %s - params %s", url, params)

        r = self._session.get(url, params=params)
        r.raise_for_status()
        return r.text.strip()

    def get_most_recent_versions(self, group, artifact, limit, integration=False):
        """Get a list of the version numbers of the most recent artifacts (integration
        or non-integration), ordered by the version number, for a particular group and
        artifact combination.

        :param str group: Group of the artifact to get versions of
        :param str artifact: Name of the artifact to get versions of
        :param int limit: Fetch only this many of the most recent releases
        :param bool integration: If true, fetch only "integration versions", otherwise
            fetch only non-integration versions.
        :return: Version numbers of the most recent artifacts
        :rtype: list
        :raises requests.exceptions.HTTPError: For any non-success HTTP responses
            from the Artifactory API.
        :raises ValueError: If limit is 0 or negative.
        """
        if limit < 1:
            raise ValueError("Releases limit must be positive")

        url = self._base_url + '/api/search/versions'
        params = {'g': group, 'a': artifact, 'repos': self._repo}
        self._logger.debug("Using all version API at %s - params %s", url, params)

        r = self._session.get(url, params=params)
        r.raise_for_status()

        response = r.json()
        versions = [item['version'] for item in response['results'] if item['integration'] is integration]
        versions.sort(key=distutils.version.LooseVersion, reverse=True)
        return versions[:limit]
