# -*- coding: utf-8 -*-
#
# Artifacts - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artifacts.scheme.mvn
~~~~~~~~~~~~~~~~~~~~

Maven repository layout ArtifactoryClient implementation.
"""

from __future__ import absolute_import

import artifacts.client
import artifacts.path
import artifacts.scheme.base
import artifacts.util


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

    def __init__(self, config):
        #: List of extensions that artifacts are expected to use, in order in which they
        #: will be preferred when finding the artifact that corresponds to a particular
        #: release or integration version
        self.extensions = ['.war', '.jar', '.pom']

        self._version_client = config.version_client
        self._artifact_urls = _MavenArtifactUrlGenerator(
            config.path_factory, config.base_url, config.repo)

    def get_release(self, full_name, version, descriptor=None):
        group, artifact = full_name.rsplit('.', 1)
        base, matches = self._artifact_urls.get_release_url(group, artifact, version, descriptor)
        release = self._get_preferred_result_by_ext(matches)

        if release is None:
            raise RuntimeError("Could not find any artifacts for {0}".format(base))
        return release

    def get_latest_release(self, full_name, descriptor=None):
        group, artifact = full_name.rsplit('.', 1)
        version = self._version_client.get_most_recent_release(group, artifact)
        base, matches = self._artifact_urls.get_release_url(group, artifact, version, descriptor)
        release = self._get_preferred_result_by_ext(matches)

        if release is None:
            raise RuntimeError("Could not find any artifacts for {0}".format(base))
        return release

    def get_latest_releases(self, full_name, descriptor=None, limit=artifacts.scheme.base.DEFAULT_RELEASE_LIMIT):
        if limit < 1:
            raise ValueError("Releases limit must be positive")

        group, artifact = full_name.rsplit('.', 1)
        versions = self._version_client.get_most_recent_releases(group, artifact, limit)

        out = []
        for version in versions:
            base, matches = self._artifact_urls.get_release_url(group, artifact, version, descriptor)
            release = self._get_preferred_result_by_ext(matches)

            if release is not None:
                self._logger.debug(
                    "Found artifact %s for version %s of %s", release, version, full_name)
                out.append(release)
            else:
                self._logger.debug(
                    "Could not find any artifact for version %s of %s - %s",
                    version, full_name, base)

        return out

    def _get_preferred_result_by_ext(self, results):
        by_extension = dict((p.suffix, p) for p in results)
        self._logger.debug("Found potential artifacts by extension - %s", by_extension)

        for ext in self.extensions:
            if ext in by_extension:
                return by_extension[ext]
        return None


class _MavenArtifactUrlGenerator(object):
    def __init__(self, path_factory, base, repo):
        self._path_factory = path_factory
        self._base = base
        self._repo = repo

    def get_release_url(self, group, artifact, version, descriptor):
        group_path = group.replace('.', '/')

        if descriptor is not None:
            artifact_name = "{0}-{1}-{2}".format(artifact, version, descriptor)
        else:
            artifact_name = "{0}-{1}".format(artifact, version)

        url = self._path_factory(self._base + '/' + self._repo)
        url = url.joinpath(group_path, artifact, version)

        return url, url.glob(artifact_name + ".*")
