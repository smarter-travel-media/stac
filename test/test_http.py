# -*- coding: utf-8 -*-

"""
"""

import mock
import pytest


@pytest.fixture
def session():
    return mock.Mock()


@pytest.fixture
def response():
    return mock.Mock()


class TestVersionApiClient(object):
    def test_get_most_recent_release_no_results(self, session, response):
        from artifacts.exceptions import NoReleaseArtifactsError
        from artifacts.http import VersionApiClient

        response.status_code = 404
        response.url = 'https://www.example.com/artifactory/api/search/latestVersion'
        session.get.return_value = response

        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-release')

        with pytest.raises(NoReleaseArtifactsError):
            http_client.get_most_recent_release('com.example.services', 'mail')

    def test_get_most_recent_release(self, session, response):
        from artifacts.http import VersionApiClient

        response.status_code = 200
        response.text = '4.34.1\n'
        session.get.return_value = response

        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-release')
        version = http_client.get_most_recent_release('com.example.services', 'mail')

        assert '4.34.1' == version

    def test_get_most_recent_versions_invalid_limit(self, session):
        from artifacts.http import VersionApiClient
        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-release')

        with pytest.raises(ValueError):
            http_client.get_most_recent_versions('com.example.services', 'mail', 0)

    def test_get_most_recent_versions_no_results(self, session, response):
        from artifacts.exceptions import NoArtifactVersionsError
        from artifacts.http import VersionApiClient

        response.status_code = 404
        response.url = 'https://www.example.com/artifactory/api/search/versions'
        session.get.return_value = response

        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-release')

        with pytest.raises(NoArtifactVersionsError):
            http_client.get_most_recent_versions('com.example.services', 'mail', 3)

    def test_get_most_recent_versions_no_integration_results(self, session, response):
        from artifacts.exceptions import NoArtifactVersionsError
        from artifacts.http import VersionApiClient

        response.status_code = 200
        response.url = 'https://www.example.com/artifactory/api/search/versions'
        response.json.return_value = {
            'results': [
                {
                    'version': '4.441',
                    'integration': False
                },
                {
                    'version': '4.440',
                    'integration': False
                },
                {
                    'version': '4.435',
                    'integration': False
                }
            ]
        }

        session.get.return_value = response

        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-release')

        with pytest.raises(NoArtifactVersionsError):
            http_client.get_most_recent_versions('com.example.services', 'mail', 2, integration=True)

    def test_get_most_recent_versions_no_non_integration_results(self, session, response):
        from artifacts.exceptions import NoArtifactVersionsError
        from artifacts.http import VersionApiClient

        response.status_code = 200
        response.url = 'https://www.example.com/artifactory/api/search/versions'
        response.json.return_value = {
            'results': [
                {
                    'version': '4.441-SNAPSHOT',
                    'integration': True
                },
                {
                    'version': '4.440-SNAPSHOT',
                    'integration': True
                },
                {
                    'version': '4.439-SNAPSHOT',
                    'integration': True
                }
            ]
        }

        session.get.return_value = response

        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-snapshot')

        with pytest.raises(NoArtifactVersionsError):
            http_client.get_most_recent_versions('com.example.services', 'mail', 2, integration=False)

    def test_get_most_recent_versions(self, session, response):
        from artifacts.http import VersionApiClient

        response.status_code = 200
        response.url = 'https://www.example.com/artifactory/api/search/versions'
        response.json.return_value = {
            'results': [
                {
                    'version': '4.441-SNAPSHOT',
                    'integration': True
                },
                {
                    'version': '4.440-SNAPSHOT',
                    'integration': True
                },
                {
                    'version': '4.439-SNAPSHOT',
                    'integration': True
                }
            ]
        }

        session.get.return_value = response

        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-snapshot')
        versions = http_client.get_most_recent_versions('com.example.services', 'mail', 2, integration=True)

        assert 2 == len(versions)
        assert '4.441-SNAPSHOT' == versions[0]
        assert '4.440-SNAPSHOT' == versions[1]
