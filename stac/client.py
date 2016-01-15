# -*- coding: utf-8 -*-
#
# Stac - Smarter Travel Artifactory Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
stac.client
~~~~~~~~~~~

Interface for clients that interact with Artifactory and implementations of it
for various repository layouts. This module is the main entry point for users of
the Stac library.
"""

from __future__ import absolute_import
from abc import ABCMeta, abstractmethod
import requests
import stac.exceptions
import stac.http
import stac.util

DEFAULT_VERSION_LIMIT = 5


class ArtifactoryClient(object):
    """Interface for getting URLs and versions of artifacts.

    How artifact names, packaging, and descriptors are interpreted is implementation
    specific and typically based on a particular repository layout. For example
    a Maven layout based client would use ``full_name`` for the full group and
    artifact (e.g. 'com.example.project.service'). While a Python layout based
    client would use ``full_name`` as unique name in a flat namespace (e.g
    'my-project').
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_version_url(self, full_name, packaging, version, descriptor=None):
        pass

    @abstractmethod
    def get_latest_version(self, full_name):
        pass

    @abstractmethod
    def get_latest_versions(self, full_name, limit=DEFAULT_VERSION_LIMIT):
        pass


class ArtifactUrlGenerator(object):
    """Interface for generating the URL to download a particular version of an
    artifact.

    Implementations will typically be specific to a particular repository layout
    in Artifactory. I.e. there may be one URL generator for Maven repositories,
    another one for Python packages, and another for NPM modules.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_url(self, group, artifact, packaging, version, descriptor):
        pass


def new_maven_client(base_url, repo, is_snapshot=False, username=None, password=None):
    """Get a new implementation of :class:`ArtifactoryClient` for use with Maven repository
    layouts, optionally using the provided authentication.

    Most users will simply call this method to get a new Maven client instance. For example:

    >>> client = new_maven_client('https://www.example.com/artifactory', 'libs-release')
    >>> latest = client.get_latest_version('com.example.users.service', 'war')
    '1.6.0'

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
    :rtype: GenericArtifactoryClient
    """

    session = requests.Session()
    if username is not None and password is not None:
        session.auth = (username, password)

    config = GenericArtifactoryClientConfig()
    config.is_integration = is_snapshot
    config.http_dao = stac.http.VersionApiDao(session, base_url, repo)
    config.url_generator = MavenArtifactUrlGenerator(base_url, repo)

    return GenericArtifactoryClient(config)


# pylint: disable=too-few-public-methods
class GenericArtifactoryClientConfig(object):
    """Configuration for construction of a new :class:`GenericArtifactoryClient` instance."""

    def __init__(self):
        #: Does the repository we are searching against contain SNAPSHOT (a.k.a. integration)
        #: versions and thus require alternate API calls to determine the latest version? Default
        #: is false.
        self.is_integration = False

        #: DAO for interacting with the Artifactory HTTP API.
        self.http_dao = None

        #: URL generator for determining the URL to download an artifact.
        self.url_generator = None


class GenericArtifactoryClient(ArtifactoryClient):
    """Artifactory client for use with multiple different repository layouts.

    Different :class:`ArtifactUrlGenerator` implementations can be used with this
    client to support different repository layouts. The logic within this client
    should be relatively layout agnostic.

    This class is thread safe.
    """

    _logger = stac.util.get_log()

    def __init__(self, config):
        """Create a new generic client instance based on the supplied configuration.

        :param GenericArtifactoryClientConfig config: Required configuration for this client
        """
        self._is_integration = config.is_integration
        self._dao = config.http_dao
        self._urls = config.url_generator

    def get_version_url(self, full_name, packaging, version, descriptor=None):
        """Get the URL to a specific version of the given project, optionally using
        a descriptor to get a particular variant of the version (sources, javadocs, etc.).

        The name of the artifact should be composed of the group ID and artifact ID
        (if available). E.g. "com.example.project.service". Depending on the repository
        layout, the ``full_name`` might only be the artifact name.

        Packaging should be the type of file used for the artifact, e.g. 'war', 'jar', 'pom',
        etc.

        The descriptor may be used to select javadoc jars, sources jars, or any other
        assemblies created as part of the version of the artifact.

        Example usage:

        >>> client = new_maven_client('https://www.example.com/artifactory', 'libs-release')
        >>> client.get_version_url('com.example.users.service', '1.4.5', 'jar', descriptor='sources')
        'https://www.example.com/artifactory/libs-release/com/example/users/service/1.4.5/service-1.4.5-sources.jar'

        The example above would return a path object for the sources jar of version 1.4.5
        of some hypothetical user service.

        This method does not make any network requests.

        :param str full_name: Fully qualified name of the artifact to get the path of.
        :param str packaging: Type of packaging / file format used for the artifact
        :param str version: Version of the artifact to get the path of.
        :param str descriptor: Tag to get a particular variant of a release.
        :return: URL to the artifact with given name and version
        :rtype: str
        """
        group, artifact = _parse_full_name(full_name)
        return self._urls.get_url(group, artifact, packaging, version, descriptor)

    def get_latest_version(self, full_name):
        """Get the most recent version of the given project.

        The name of the artifact should be composed of the group ID and artifact ID
        (if available). E.g. "com.example.project.service". Depending on the repository
        layout, the ``full_name`` might only be the artifact name.

        Example usage:

        >>> client = new_maven_client('https://www.example.com/artifactory', 'libs-release')
        >>> client.get_latest_version('com.example.users.service')
        '1.5.0'

        The example above returns the latest version of a hypothetical user service, 1.5.0.

        This method makes a single network request.

        :param str full_name: Fully qualified name of the artifact to get the version of.
        :return: Version number of the latest version of the artifact
        :rtype: str
        :raises stac.exceptions.NoMatchingVersionsError: If no matching artifact could
            be found
        """
        group, artifact = _parse_full_name(full_name)
        try:
            if not self._is_integration:
                version = self._get_latest_release_version(group, artifact)
            else:
                version = self._get_latest_snapshot_version(group, artifact)
        except requests.HTTPError as e:
            # pylint: disable=no-member
            if e.response is not None and e.response.status_code == requests.codes.not_found:
                raise self._get_wrapped_exception(group, artifact, cause=e)
            raise
        return version

    def get_latest_versions(self, full_name, limit=DEFAULT_VERSION_LIMIT):
        """Get the most recent versions of the given project, ordered most recent to least
        recent.

        The name of the artifact should be composed of the group ID and artifact ID
        (if available). E.g. "com.example.project.service". Depending on the repository
        layout, the ``full_name`` might only be the artifact name.

        Example usage:

        >>> client = new_maven_client('https://www.example.com/artifactory', 'libs-release')
        >>> client.get_latest_versions('com.example.auth.service', limit=3)
        ['1.6.0', '1.5.4', '1.5.3']

        The example above would return a list of the three most recent versions of some hypothetical
        authentication service.

        This method makes a single network request.

        :param str full_name: Full qualified name of the artifacts to get the versions of.
        :param int limit: Only get the ``limit`` most recent versions.
        :return: Most recent versions of the artifact with the given name, ordered with most
            recent first.
        :rtype: list
        :raises ValueError: If limit is negative or zero
        :raises stac.exceptions.NoMatchingVersionsError: If no matching artifact could be
            found
        """
        if limit < 1:
            raise ValueError("Releases limit must be positive")

        group, artifact = _parse_full_name(full_name)

        try:
            versions = self._dao.get_most_recent_versions(
                group, artifact, limit, integration=self._is_integration)
        except requests.HTTPError as e:
            # pylint: disable=no-member
            if e.response is not None and e.response.status_code == requests.codes.not_found:
                raise self._get_wrapped_exception(group, artifact, cause=e)
            raise

        if not versions:
            raise self._get_wrapped_exception(group, artifact)
        return versions

    def _get_latest_release_version(self, group, artifact):
        return self._dao.get_most_recent_release(group, artifact)

    def _get_latest_snapshot_version(self, group, artifact):
        snapshot_versions = self._dao.get_most_recent_versions(group, artifact, 1, integration=True)
        if not snapshot_versions:
            raise self._get_wrapped_exception(group, artifact)
        return snapshot_versions[0]

    def _get_wrapped_exception(self, group, artifact, cause=None):
        version_type = 'integration' if self._is_integration else 'non-integration'
        return stac.exceptions.NoMatchingVersionsError(
            "No {version_type} versions of {group}.{name} could be found. It might be the "
            "case that there have not been any {version_type} deployments done yet.".format(
                version_type=version_type,
                group=group,
                name=artifact
            ), cause=cause
        )


class MavenArtifactUrlGenerator(ArtifactUrlGenerator):
    """URL generator for use with Maven repositories."""

    def __init__(self, base, repo):
        """Create a new Maven URL generator, setting the Artifactory base URL and
        repository.

        :param str base: Base URL to the Artifactory installation.
        :param str repo: Name of the repository
        """
        self._base = base
        self._repo = repo

    # pylint: disable=missing-docstring,too-many-arguments
    def get_url(self, group, artifact, packaging, version, descriptor):
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

        return '/'.join([
            self._base,
            self._repo,
            group_path,
            artifact,
            version,
            artifact_name
        ])


def _parse_full_name(full_name):
    parts = full_name.rsplit('.', 1)
    if len(parts) == 1:
        group, artifact = '', parts[0]
    else:
        group, artifact = parts[0], parts[1]
    return group, artifact
