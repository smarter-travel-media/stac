# -*- coding: utf-8 -*-
#
# Artifacts - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artifacts.client
~~~~~~~~~~~~~~~~

Interface for clients that interact with Artifactory and a implementations of
it for various repository layouts. This module is the main entry point for users
of the Artifacts library.
"""

from __future__ import absolute_import

import artifacts.exceptions
import artifacts.http
import artifacts.util
import requests
from abc import ABCMeta, abstractmethod

DEFAULT_RELEASE_LIMIT = 5


class ArtifactoryClient(object):
    """Interface for getting artifact URLs based on an artifact name and packaging.

    How artifact names, packaging, and descriptors are interpreted is implementation
    specific and typically based on a particular repository layout. For example
    a Maven layout based client would use ``full_name`` for the full group and
    artifact (e.g. 'com.example.project.service'). While a Python layout based
    client would use ``full_name`` as unique name in a flat namespace (e.g
    'my-project').
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_version(self, full_name, packaging, version, descriptor=None):
        """Get the URL to a specific version of the given project, optionally using
        a descriptor to get a particular variant of the version (associated sources vs
        the actual application for example). How the ``full_name`` and ``descriptor``
        are used is implementation dependent.

        :param str full_name: Fully qualified name of the artifact to get the path of.
        :param str packaging: Type of packaging / file format used for the artifact
        :param str version: Version of the artifact to get the path of.
        :param str descriptor: Tag to get a particular variant of a release.
        :return: URL to the artifact with given name and version
        :rtype: str
        """

    @abstractmethod
    def get_latest_version(self, full_name, packaging, descriptor=None):
        """Get the URL to the most recent version of the given project, optionally using
        a descriptor to get a particular variant of the version (associated sources vs the
        actual application for example). How the ``full_name`` and ``descriptor`` are used
        is implementation dependent.

        :param str full_name: Fully qualified name of the artifact to get the path of.
        :param str descriptor: Tag to get a particular variant of a release.
        :param str packaging: Type of packaging / file format used for the artifact
        :return: URL to the artifact with given name
        :rtype: str
        :raises artifacts.exceptions.NoMatchingVersionsError: If no matching artifact could
            be found
        """

    @abstractmethod
    def get_latest_versions(self, full_name, packaging, descriptor=None, limit=DEFAULT_RELEASE_LIMIT):
        """Get the URLs to the most recent versions of the given project, most recent versions
        first, optionally using a descriptor to get a particular variant of the versions
        (associated sources vs the actual application for example). How the ``full_name`` and
        ``descriptor`` are used is implementation dependent.

        :param str full_name: Full qualified name of the artifacts to get the path of.
        :param str descriptor: Tag to get a particular variant of each release
        :param str packaging: Type of packaging / file format used for the artifacts
        :param int limit: Only get the ``limit`` most recent releases.
        :return: URL to each of the most recent artifacts with the given name, ordered
            with most recent releases first.
        :rtype: list
        :raises ValueError: If limit is negative or zero
        :raises artifacts.exceptions.NoMatchingVersionsError: If no matching artifact could be
            found
        """


def new_maven_client(base_url, repo, is_snapshot=False, username=None, password=None):
    """Get a new implementation of :class:`ArtifactoryClient` for use with Maven repository
    layouts, optionally using the provided authentication.

    Most users will simply call this method to get a new Maven client instance. For example:

    >>> client = new_maven_client('https://artifactory.example.com/artifactory', 'libs-release')
    >>> latest = client.get_latest_version('com.example.users.service', 'war')
    'https://artifactory.example.com/artifactory/libs-release/com/example/users/service/1.6.0/service-1.6.0.war'

    :param str base_url: URL to root of the Artifactory installation. Example,
        "https://artifactory.example.com/artifactory".
    :param str repo: Which repository should searches be done against. Example, "libs-release-local"
        or "libs-snapshot-local".
    :param bool is_snapshot: Does the repository to perform searches against contain SNAPSHOT
        (a.k.a. integration) versions? Default is ``False``
    :param str username: Optional username for authentication when making API calls and
        downloading artifacts.
    :param str password: Optional password for authentication when making API calls and
        downloading artifacts.
    :return: New Artifactory client for use with Maven repositories
    :rtype: MavenArtifactoryClient
    """

    session = requests.Session()
    if username is not None and password is not None:
        session.auth = (username, password)

    config = MavenArtifactoryClientConfig()
    config.base_url = base_url
    config.repo = repo
    config.is_snapshot = is_snapshot
    config.http_client = artifacts.http.VersionApiClient(session, base_url, repo)

    return MavenArtifactoryClient(config)


class MavenArtifactoryClientConfig(object):
    """Configuration for construction of a new :class:`MavenArtifactoryClient` instance."""

    def __init__(self):
        #: URL to root of the Artifactory installation. Example,
        #: "https://artifactory.example.com/artifactory".
        self.base_url = None

        #: Which repository should searches be done against. Example, "libs-release-local"
        #: or "libs-snapshot-local".
        self.repo = None

        #: Does the repository we are searching against contain SNAPSHOT (a.k.a. integration)
        #: versions and thus require alternate API calls to determine the latest version? Default
        #: is false
        self.is_snapshot = False

        #: Client for interacting with the Artifactory HTTP API
        self.http_client = None


class MavenArtifactoryClient(ArtifactoryClient):
    """Implementation of a :class:`ArtifactoryClient` for working with Maven repository layouts.

    .. note::

        Searches performed by this client are limited to the repository set when creating the
        client. That means, searches for a release artifact will not work if the repository has
        only integration artifacts.

    This class is thread safe.
    """

    _logger = artifacts.util.get_log()

    def __init__(self, config):
        """Create a new Maven client instance based on the supplied configuration.

        :param MavenArtifactoryClientConfig config: Required configuration for this client
        """
        self._is_snapshot = config.is_snapshot
        self._http_client = config.http_client
        self._artifact_urls = _MavenArtifactUrlGenerator(config.base_url, config.repo)

    def get_version(self, full_name, packaging, version, descriptor=None):
        """Get the URL to a specific version of the given project, optionally using
        a descriptor to get a particular variant of the version (sources, javadocs, etc.).

        The name of the artifact to get a path to should be composed of the group ID
        and artifact ID (in Maven parlance). E.g. "com.example.project.service".

        Packaging should be the type of file used for the artifact, e.g. 'war', 'jar', 'pom',
        etc.

        The descriptor may be used to select javadoc jars, sources jars, or any other
        assemblies created as part of the version of the artifact.

        Example usage:

        >>> client = new_maven_client('https://artifactory.example.com/artifactory', 'libs-release')
        >>> client.get_version('com.example.users.service', '1.4.5', 'jar', descriptor='sources')
        'https://artifactory.example.com/artifactory/libs-release/com/example/users/service/1.4.5/service-1.4.5-sources.jar'

        The example above would return a path object for the sources jar of version 1.4.5
        of some hypothetical user service.

        .. seealso::

            :meth:`ArtifactoryClient.get_release`

        """

        group, artifact = full_name.rsplit('.', 1)
        url = self._artifact_urls.get_version_url(group, artifact, packaging, version, descriptor)
        return url

    def get_latest_version(self, full_name, packaging, descriptor=None):
        """Get the URL to the most recent version of the given project, optionally using
        a descriptor to get a particular variant of the version (sources, javadocs, etc.).

        The name of the artifact to get a path to should be composed of the group ID
        and artifact ID (in Maven parlance). E.g. "com.example.project.service".

        Packaging should be the type of file used for the artifact, e.g. 'war', 'jar', 'pom',
        etc.

        The descriptor may be used to select javadoc jars, sources jars, or any other
        assemblies created as part of the version of the artifact.

        Example usage:

        >>> client = MavenArtifactoryClient(MavenArtifactoryClientConfig())
        >>> client.get_latest_version('com.example.users.service', 'war')
        'https://artifactory.example.com/artifactory/libs-release/com/example/users/service/1.6.0/service-1.6.0.war'

        The example above would return a path object for the war of version 1.6.0 of some
        hypothetical user service.

        .. seealso::

            :meth:`ArtifactoryClient.get_latest_release`

        """
        group, artifact = full_name.rsplit('.', 1)
        try:
            if not self._is_snapshot:
                url = self._get_latest_release_version(group, artifact, packaging, descriptor)
            else:
                url = self._get_latest_snapshot_version(group, artifact, packaging, descriptor)
        except requests.HTTPError as e:
            if e.request is not None and e.request.status_code == requests.codes.not_found:
                raise self._get_wrapped_exception(group, artifact, cause=e)
            raise
        return url

    def _get_latest_release_version(self, group, artifact, packaging, descriptor):
        release_version = self._http_client.get_most_recent_release(group, artifact)
        return self._artifact_urls.get_version_url(group, artifact, packaging, release_version, descriptor)

    def _get_latest_snapshot_version(self, group, artifact, packaging, descriptor):
        snapshot_version = self._http_client.get_most_recent_versions(group, artifact, 1, integration=True)[0]
        return self._artifact_urls.get_version_url(group, artifact, packaging, snapshot_version, descriptor)

    def _get_wrapped_exception(self, group, artifact, cause=None):
        version_type = 'integration' if self._is_snapshot else 'non-integration'
        return artifacts.exceptions.NoMatchingVersionsError(
            "No {version_type} versions of {group}.{name} could be found. It might be the "
            "case that there have not been any {version_type} deployments done yet.".format(
                version_type=version_type,
                group=group,
                name=artifact
            ), cause=cause
        )

    def get_latest_versions(self, full_name, packaging, descriptor=None, limit=DEFAULT_RELEASE_LIMIT):
        """Get the URLs to the most recent versions of the given project, most recent version
        first, optionally using a descriptor to get a particular variant of the versions (sources,
        javadocs, etc.).

        The name of the artifact to get a path to should be composed of the group ID
        and artifact ID (in Maven parlance). E.g. "com.example.project.service".

        Packaging should be the type of file used for the artifacts, e.g. 'war', 'jar', 'pom',
        etc.

        The descriptor may be used to select javadoc jars, sources jars, or any other
        assemblies created as part of the version of the artifact.

        Example usage:

        >>> client = MavenArtifactoryClient(MavenArtifactoryClientConfig())
        >>> client.get_latest_versions('com.example.users.service', 'war', limit=3)
        [
            'https://artifactory.example.com/artifactory/libs-release/com/example/users/service/1.6.0/service-1.6.0.war',
            'https://artifactory.example.com/artifactory/libs-release/com/example/users/service/1.5.4/service-1.5.4.war',
            'https://artifactory.example.com/artifactory/libs-release/com/example/users/service/1.5.3/service-1.5.3.war'
        ]

        The example above would return a list of URLs for the wars of the three most recent
        versions of some hypothetical user service.

        .. seealso::

            :meth:`ArtifactoryClient.get_latest_releases`

        """
        if limit < 1:
            raise ValueError("Releases limit must be positive")

        group, artifact = full_name.rsplit('.', 1)

        try:
            versions = self._http_client.get_most_recent_versions(
                group, artifact, limit, integration=self._is_snapshot)
        except requests.HTTPError as e:
            if e.request is not None and e.request.status_code == requests.codes.not_found:
                raise self._get_wrapped_exception(group, artifact, cause=e)
            raise

        out = []
        for version in versions:
            out.append(self._artifact_urls.get_version_url(group, artifact, packaging, version, descriptor))

        if not out:
            raise self._get_wrapped_exception(group, artifact)
        return out


class _MavenArtifactUrlGenerator(object):
    def __init__(self, base, repo):
        self._base = base
        self._repo = repo

    def get_version_url(self, group, artifact, packaging, version, descriptor):
        group_path = group.replace('.', '/')

        if descriptor is not None:
            artifact_name = "{name}-{version}-{descriptor}.{ext}".format(
                name=artifact,
                version=version,
                descriptor=descriptor,
                ext=packaging
            )
        else:
            artifact_name = "{name}-{version}.{ext}".format(
                name=artifact,
                version=version,
                ext=packaging
            )

        url = '/'.join([
            self._base,
            self._repo,
            group_path,
            artifact,
            version,
            artifact_name
        ])
        return url
