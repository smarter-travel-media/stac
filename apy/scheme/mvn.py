# -*- coding: utf-8 -*-

"""
"""

import apy.scheme.base

import apy.artifacts
import apy.util
import apy.versions


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
        session_factory = apy.versions.AuthenticatedSessionFactory(config.username, config.password)
        api_url_generator = apy.versions.VersionApiUrlGenerator(config.base_url, config.repo)
        self._api_client = apy.versions.VersionApiClient(session_factory, api_url_generator)

        path_factory = apy.artifacts.AuthenticatedPathFactory(config.username, config.password)
        self._artifact_urls = _MavenArtifactUrlGenerator(path_factory, config.base_url, config.repo)

    def get_release(self, group, artifact, version):
        url = self._artifact_urls.get_release_url(group, artifact, version)
        return self._get_preferred_result_by_ext(url)

    def get_latest_release(self, group, artifact):
        version = self._api_client.get_most_recent_release(group, artifact)

        return self._get_preferred_result_by_ext(
            self._artifact_urls.get_release_url(group, artifact, version))

    def get_latest_releases(self, group, artifact, limit=apy.scheme.base.DEFAULT_RELEASE_LIMIT):
        if limit < 1:
            raise ValueError("Releases limit must be positive")

        versions = self._api_client.get_most_recent_releases(group, artifact, limit)

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
