# -*- coding: utf-8 -*-

"""
"""

import distutils.version

import artifactory
import requests
import apy.scheme.base
import apy.util


class MavenArtifactoryClientConfig(object):
    def __init__(self):
        self.base_url = None
        self.repo = None
        self.username = None
        self.password = None


class MavenArtifactoryClient(apy.scheme.base.ArtifactoryClient):
    _logger = apy.util.get_log()

    _extensions = ['.war', '.jar', '.pom']

    def __init__(self, config):
        path_factory = _ArtifactoryPathFactory(config.username, config.password)
        self._artifact_urls = _ArtifactUrlGenerator(path_factory, config.base_url, config.repo)
        self._api_urls = _ApiUrlGenerator(config.base_url, config.repo)
        self._session = requests.Session()

    def get_release(self, group, artifact, version):
        url = self._artifact_urls.get_release_url(group, artifact, version)
        return self._get_preferred_result_by_ext(url)

    def get_latest_release(self, group, artifact):
        url, params = self._api_urls.get_latest_version_url(group, artifact)
        self._logger.debug("Using latest version API at %s - params %s", url, params)

        r = self._session.get(str(url), params=params)
        r.raise_for_status()

        version = r.text.strip()
        return self._get_preferred_result_by_ext(
            self._artifact_urls.get_release_url(group, artifact, version))

    def get_latest_releases(self, group, artifact, limit=apy.scheme.base.DEFAULT_RELEASE_LIMIT):
        if limit < 1:
            raise ValueError("Releases limit must be positive")

        url, params = self._api_urls.get_all_version_url(group, artifact)
        self._logger.debug("Using all version API at %s - params %s", url, params)

        r = self._session.get(str(url), params=params)
        r.raise_for_status()

        response = r.json()
        versions = [item['version'] for item in response['results']]
        versions.sort(key=distutils.version.LooseVersion, reverse=True)
        recent_versions = versions[:limit]

        out = []
        for version in recent_versions:
            out.append(
                self._get_preferred_result_by_ext(
                    self._artifact_urls.get_release_url(group, artifact, version)))

        return out

    def _get_preferred_result_by_ext(self, result_generator):
        by_extension = dict((p.suffix, p) for p in result_generator)
        self._logger.debug("Found potential artifacts by extension - %s", by_extension)

        for ext in self._extensions:
            if ext in by_extension:
                return by_extension[ext]

        raise ValueError(
            "Unable to find any acceptable extensions in mapping {0}".format(by_extension))


class _ArtifactoryPathFactory(object):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def __call__(self, *args, **kwargs):
        if self._username is not None and self._password is not None:
            kwargs['auth'] = (self._username, self._password)
        return artifactory.ArtifactoryPath(*args, **kwargs)


class _RequestsSessionFactory(object):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def __call__(self):
        session = requests.Session()
        if self._username is not None and self._password is not None:
            session.auth = (self._username, self._password)
        return session


class _ArtifactUrlGenerator(object):
    def __init__(self, path_factory, base, repo):
        self._path_factory = path_factory
        self._base = base
        self._repo = repo

    def get_release_url(self, group, artifact, version):
        return self._get_artifact_url(group, artifact, version, is_snapshot=False)

    def get_snapshot_url(self, group, artifact, version):
        return self._get_artifact_url(group, artifact, version, is_snapshot=True)

    def _get_artifact_url(self, group, artifact, version, is_snapshot=False):
        group_path = group.replace('.', '/')

        if is_snapshot:
            artifact_name = "{0}-{1}-SNAPSHOT".format(artifact, version)
        else:
            artifact_name = "{0}-{1}".format(artifact, version)

        url = self._path_factory(self._base + '/' + self._repo)
        url = url.joinpath(group_path, artifact, version)

        # TODO: This is an extra HTTP request per artifact but it means we can
        # give a meaningful exception here instead of blowing up later during the
        # part where we try to find the right extension. Maybe return a tuple of the
        # base URL and the glob? Allow callers to decide if they want to call it?
        # if not url.exists():
        #    raise IOError("Artifact URL {0} does not appear to exist".format(url))
        return url.glob(artifact_name + ".*")


# TODO: Auth?!
class _ApiUrlGenerator(object):
    def __init__(self, base, repo):
        self._base = base
        self._repo = repo

    def get_latest_version_url(self, group, artifact):
        url = self._base + '/api/search/latestVersion'
        return url, {'g': group, 'a': artifact, 'repos': self._repo}

    def get_all_version_url(self, group, artifact):
        url = self._base + '/api/search/versions'
        return url, {'g': group, 'a': artifact, 'repos': self._repo}
