# -*- coding: utf-8 -*-

"""
"""

import mock
import pytest
import requests


@pytest.fixture
def session():
    return mock.Mock(spec=requests.Session)


@pytest.fixture
def response():
    return mock.Mock(spec=requests.Response)


class TestVersionApiClient(object):
    def test_get_most_recent_release_no_results(self, session, response):
        from artificium.http import VersionApiClient

        response.status_code = 404
        response.url = 'https://www.example.com/artifactory/api/search/latestVersion'
        error = requests.HTTPError("Something bad", request=requests.Request(), response=response)
        response.raise_for_status.side_effect = error
        session.get.return_value = response

        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-release')

        with pytest.raises(requests.HTTPError):
            http_client.get_most_recent_release('com.example.services', 'mail')

    def test_get_most_recent_release(self, session, response):
        from artificium.http import VersionApiClient

        response.status_code = 200
        response.text = '4.34.1\n'
        session.get.return_value = response

        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-release')
        version = http_client.get_most_recent_release('com.example.services', 'mail')

        assert '4.34.1' == version

    def test_get_most_recent_versions_invalid_limit(self, session):
        from artificium.http import VersionApiClient
        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-release')

        with pytest.raises(ValueError):
            http_client.get_most_recent_versions('com.example.services', 'mail', 0)

    def test_get_most_recent_versions_no_results(self, session, response):
        from artificium.http import VersionApiClient

        response.status_code = 404
        response.url = 'https://www.example.com/artifactory/api/search/versions'
        error = requests.HTTPError("Something bad", request=requests.Request(), response=response)
        response.raise_for_status.side_effect = error
        session.get.return_value = response

        http_client = VersionApiClient(session, 'https://www.example.com/artifactory', 'libs-release')

        with pytest.raises(requests.HTTPError):
            http_client.get_most_recent_versions('com.example.services', 'mail', 3)

    def test_get_most_recent_versions_no_integration_results(self, session, response):
        from artificium.http import VersionApiClient

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
        versions = http_client.get_most_recent_versions('com.example.services', 'mail', 2, integration=True)
        assert 0 == len(versions)

    def test_get_most_recent_versions_no_non_integration_results(self, session, response):
        from artificium.http import VersionApiClient

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
        versions = http_client.get_most_recent_versions('com.example.services', 'mail', 2, integration=False)
        assert 0 == len(versions)

    def test_get_most_recent_versions(self, session, response):
        from artificium.http import VersionApiClient

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
