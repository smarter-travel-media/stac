# -*- coding: utf-8 -*-

"""
"""

import collections

import artifactory

import apy
import apy.util

MavenArtifactoryClientConfig = collections.namedtuple('MavenArtifactoryClientConfig', [
    'base_url',
    'repo',
    'session'
])


class MavenArtifactoryClient(apy.ArtifactoryClient):
    _logger = apy.util.get_log()

    _extensions = ['.war', '.jar', '.pom']

    def __init__(self, config):
        self._artifact_urls = _ArtifactUrlGenerator(config.base_url, config.repo)
        self._api_urls = _ApiUrlGenerator(config.base_url, config.repo)
        self._session = config.session

    def get_latest_release(self, group, artifact):
        url, params = self._api_urls.get_latest_version_url(group, artifact)
        self._logger.debug("Using latest version API at %s - params %s", url, params)

        r = self._session.get(str(url), params=params)
        r.raise_for_status()

        version = r.text.strip()
        by_extension = dict((p.suffix, p) for p in self._artifact_urls.get_url(group, artifact, version))
        self._logger.debug("Found potential artifacts by extension - %s", by_extension)

        for ext in self._extensions:
            if ext in by_extension:
                return by_extension[ext]
        return None

    def get_latest_releases(self, artifact, group, limit=None):
        pass


class _ArtifactUrlGenerator(object):
    def __init__(self, base, repo):
        self._base = base
        self._repo = repo

    def get_url(self, group, artifact, version):
        group_path = group.replace('.', '/')
        artifact_name = artifact + '-' + version

        url = artifactory.ArtifactoryPath(self._base + '/' + self._repo)
        url = url.joinpath(group_path, artifact, version)
        return url.glob(artifact_name + ".*")


class _ApiUrlGenerator(object):
    def __init__(self, base, repo):
        self._base = base
        self._repo = repo

    def get_latest_version_url(self, group, artifact):
        url = artifactory.ArtifactoryPath(self._base + '/api/search/latestVersion')
        return url, {'g': group, 'a': artifact, 'repos': self._repo}

    def get_all_version_url(self, group, artifact):
        url = artifactory.ArtifactoryPath(self._base + '/api/search/versions')
        return url, {'g': group, 'a': artifact, 'repos': self._repo}
