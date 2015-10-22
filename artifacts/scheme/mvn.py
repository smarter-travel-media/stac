# -*- coding: utf-8 -*-

"""
"""

import artifacts.scheme.base

import artifacts.path
import artifacts.util
import artifacts.client


def new_maven_client(base_url, repo, username=None, password=None):
    session_factory = artifacts.client.AuthenticatedSessionFactory(username, password)
    api_url_generator = artifacts.client.VersionApiUrlGenerator(base_url, repo)
    version_client = artifacts.client.VersionApiClient(session_factory, api_url_generator)
    path_factory = artifacts.path.AuthenticatedPathFactory(username, password)

    config = MavenArtifactoryClientConfig()
    config.base_url = base_url
    config.repo = repo
    config.version_client = version_client
    config.path_factory = path_factory

    return MavenArtifactoryClient(config)


class MavenArtifactoryClientConfig(object):
    def __init__(self):
        self.base_url = None
        self.repo = None
        self.version_client = None
        self.path_factory = None


class MavenArtifactoryClient(artifacts.scheme.base.ArtifactoryClient):
    _logger = artifacts.util.get_log()

    _extensions = ['.war', '.jar', '.pom']

    def __init__(self, config):
        self._version_client = config.version_client
        self._artifact_urls = _MavenArtifactUrlGenerator(config.path_factory, config.base_url, config.repo)

    def get_release(self, full_name, version):
        group, artifact = full_name.rsplit('.', 1)
        url = self._artifact_urls.get_release_url(group, artifact, version)
        return self._get_preferred_result_by_ext(url)

    def get_latest_release(self, full_name):
        group, artifact = full_name.rsplit('.', 1)
        version = self._version_client.get_most_recent_release(group, artifact)

        return self._get_preferred_result_by_ext(
            self._artifact_urls.get_release_url(group, artifact, version))

    def get_latest_releases(self, full_name, limit=artifacts.scheme.base.DEFAULT_RELEASE_LIMIT):
        if limit < 1:
            raise ValueError("Releases limit must be positive")

        group, artifact = full_name.rsplit('.', 1)
        versions = self._version_client.get_most_recent_releases(group, artifact, limit)

        out = []
        for version in versions:
            out.append(
                self._get_preferred_result_by_ext(
                    self._artifact_urls.get_release_url(group, artifact, version)))

        return out

    def _get_preferred_result_by_ext(self, results):
        by_extension = dict((p.suffix, p) for p in results)
        self._logger.debug("Found potential artifacts by extension - %s", by_extension)

        for ext in self._extensions:
            if ext in by_extension:
                return by_extension[ext]

        raise ValueError(
            "Unable to find any acceptable extensions in mapping {0}".format(by_extension))


class _MavenArtifactUrlGenerator(object):
    def __init__(self, path_factory, base, repo):
        self._path_factory = path_factory
        self._base = base
        self._repo = repo

    def get_release_url(self, group, artifact, version):
        group_path = group.replace('.', '/')
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
