# -*- coding: utf-8 -*-

"""
"""

import mock
import pytest
import requests


@pytest.fixture
def version_dao():
    from stac.http import VersionApiDao
    return mock.Mock(spec=VersionApiDao)


@pytest.fixture
def url_generator():
    from stac.client import MavenArtifactUrlGenerator
    return mock.Mock(spec=MavenArtifactUrlGenerator)


class TestMavenArtifactoryClient(object):
    def test_get_version_url(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig

        url_generator.get_url.return_value = ('https://www.example.com/artifactory/libs-release/'
                                              'com/example/services/login/3.9.1/login-3.9.1.jar')

        config = GenericArtifactoryClientConfig()
        config.is_integration = False
        config.http_dao = version_dao
        config.url_generator = url_generator

        client = GenericArtifactoryClient(config)
        url = client.get_version_url('com.example.services.login', 'jar', '3.9.1')
        assert ('https://www.example.com/artifactory/libs-release/'
                'com/example/services/login/3.9.1/login-3.9.1.jar') == url

    def test_get_latest_version_snapshot(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig

        version_dao.get_most_recent_versions.return_value = ['1.3.0-SNAPSHOT']

        config = GenericArtifactoryClientConfig()
        config.is_integration = True
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)
        version = maven_client.get_latest_version('com.example.users.service')
        assert '1.3.0-SNAPSHOT' == version

    def test_get_latest_version_snapshot_no_results(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig
        from stac.exceptions import NoMatchingVersionsError

        request = mock.Mock(spec=requests.Request)
        response = mock.Mock(spec=requests.Response)
        response.status_code = 404
        error = requests.HTTPError("Something bad", request=request, response=response)
        version_dao.get_most_recent_versions.side_effect = error

        config = GenericArtifactoryClientConfig()
        config.is_integration = True
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_version('com.example.users.service')

    def test_get_latest_version_snapshot_only_release_results(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig
        from stac.exceptions import NoMatchingVersionsError

        version_dao.get_most_recent_versions.return_value = []

        config = GenericArtifactoryClientConfig()
        config.is_integration = True
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_version('com.example.users.service')

    def test_get_latest_version_release(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig

        version_dao.get_most_recent_release.return_value = '4.13.4'

        config = GenericArtifactoryClientConfig()
        config.is_integration = False
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)
        version = maven_client.get_latest_version('com.example.users.service')
        assert '4.13.4' == version

    def test_get_latest_version_release_no_results(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig
        from stac.exceptions import NoMatchingVersionsError

        request = mock.Mock(spec=requests.Request)
        response = mock.Mock(spec=requests.Response)
        response.status_code = 404
        error = requests.HTTPError("Something bad", request=request, response=response)
        version_dao.get_most_recent_release.side_effect = error

        config = GenericArtifactoryClientConfig()
        config.is_integration = False
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_version('com.example.users.service')

    def test_get_latest_versions_bad_limit(self):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig

        config = GenericArtifactoryClientConfig()
        maven_client = GenericArtifactoryClient(config)

        with pytest.raises(ValueError):
            maven_client.get_latest_versions('com.example.users.service', 0)

    def test_get_latest_versions_snapshot(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig

        version_dao.get_most_recent_versions.return_value = [
            '1.3.0-SNAPSHOT', '1.2.1-SNAPSHOT', '1.1.0-SNAPSHOT']

        config = GenericArtifactoryClientConfig()
        config.is_integration = True
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)
        versions = maven_client.get_latest_versions('com.example.users.service', limit=3)
        expected = [
            '1.3.0-SNAPSHOT',
            '1.2.1-SNAPSHOT',
            '1.1.0-SNAPSHOT'
        ]

        assert expected == versions

    def test_get_latest_versions_snapshot_no_results(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig
        from stac.exceptions import NoMatchingVersionsError

        request = mock.Mock(spec=requests.Request)
        response = mock.Mock(spec=requests.Response)
        response.status_code = 404
        error = requests.HTTPError("Something bad", request=request, response=response)
        version_dao.get_most_recent_versions.side_effect = error

        config = GenericArtifactoryClientConfig()
        config.is_integration = True
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_versions('com.example.users.service')

    def test_get_latest_versions_snapshot_only_release_results(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig
        from stac.exceptions import NoMatchingVersionsError

        version_dao.get_most_recent_versions.return_value = []

        config = GenericArtifactoryClientConfig()
        config.is_integration = True
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_versions('com.example.users.service')

    def test_get_latest_versions_release(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig

        version_dao.get_most_recent_versions.return_value = ['1.2.1', '1.2.0', '1.1.1']

        config = GenericArtifactoryClientConfig()
        config.is_integration = False
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)
        versions = maven_client.get_latest_versions('com.example.users.service', limit=3)
        expected = [
            '1.2.1',
            '1.2.0',
            '1.1.1'
        ]

        assert expected == versions

    def test_get_latest_versions_release_no_results(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig
        from stac.exceptions import NoMatchingVersionsError

        request = mock.Mock(spec=requests.Request)
        response = mock.Mock(spec=requests.Response)
        response.status_code = 404
        error = requests.HTTPError("Something bad", request=request, response=response)
        version_dao.get_most_recent_versions.side_effect = error

        config = GenericArtifactoryClientConfig()
        config.is_integration = False
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_versions('com.example.users.service')

    def test_get_latest_versions_release_only_snapshot_results(self, version_dao, url_generator):
        from stac.client import GenericArtifactoryClient, GenericArtifactoryClientConfig
        from stac.exceptions import NoMatchingVersionsError

        version_dao.get_most_recent_versions.return_value = []

        config = GenericArtifactoryClientConfig()
        config.is_integration = False
        config.http_dao = version_dao
        config.url_generator = url_generator

        maven_client = GenericArtifactoryClient(config)

        with pytest.raises(NoMatchingVersionsError):
            maven_client.get_latest_versions('com.example.users.service')


class TestMavenArtifactUrlGenerator(object):
    def test_get_version_url_with_descriptor(self):
        from stac.client import MavenArtifactUrlGenerator
        gen = MavenArtifactUrlGenerator('https://corp.example.com/artifactory', 'libs-release-local')
        url = gen.get_url('com.example.services', 'locations', 'jar', '4.5.1', 'sources')

        assert ('https://corp.example.com/artifactory/libs-release-local/' +
                'com/example/services/locations/4.5.1/locations-4.5.1-sources.jar') == url

    def test_get_version_url_without_descriptor(self):
        from stac.client import MavenArtifactUrlGenerator
        gen = MavenArtifactUrlGenerator('https://corp.example.com/artifactory', 'libs-release-local')
        url = gen.get_url('com.example.services', 'locations', 'war', '4.5.1', None)

        assert ('https://corp.example.com/artifactory/libs-release-local/' +
                'com/example/services/locations/4.5.1/locations-4.5.1.war') == url


def test_parse_full_name_group_and_artifact():
    from stac.client import _parse_full_name
    name = 'com.example.services.auth'
    group, artifact = _parse_full_name(name)

    assert 'com.example.services' == group
    assert 'auth' == artifact


def test_parse_full_name_single_name():
    from stac.client import _parse_full_name
    name = 'my-python-lib'
    group, artifact = _parse_full_name(name)

    assert '' == group
    assert 'my-python-lib' == artifact
