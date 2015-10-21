# -*- coding: utf-8 -*-

"""
"""

import distutils.version

import requests
import apy.scheme.base
import apy.util


class VersionApiClient(object):
    _logger = apy.util.get_log()

    def __init__(self, session_factory, url_factory):
        self._session_factory = session_factory
        self._url_factory = url_factory

    def get_most_recent_release(self, group, artifact):
        url, params = self._url_factory.get_latest_version_url(group, artifact)
        self._logger.debug("Using latest version API at %s - params %s", url, params)

        r = self._session_factory().get(url, params=params)
        r.raise_for_status()

        return r.text.strip()

    def get_most_recent_releases(self, group, artifact, limit):
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
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def __call__(self):
        session = requests.Session()
        if self._username is not None and self._password is not None:
            session.auth = (self._username, self._password)
        return session


class VersionApiUrlGenerator(object):
    def __init__(self, base, repo):
        self._base = base
        self._repo = repo

    def get_latest_version_url(self, group, artifact):
        url = self._base + '/api/search/latestVersion'
        return url, {'g': group, 'a': artifact, 'repos': self._repo}

    def get_all_version_url(self, group, artifact):
        url = self._base + '/api/search/versions'
        return url, {'g': group, 'a': artifact, 'repos': self._repo}
