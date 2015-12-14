# -*- coding: utf-8 -*-

"""Integration tests that make live requests to a public Artifactory instance."""

ARTIFACTORY_INSTANCE = 'https://oss.jfrog.org/artifactory'
SNAPSHOT_REPO = 'oss-snapshot-local'


def test_get_latest_snapshot_version():
    """Integration test to make sure we can get the latest snapshot (library and sources)
    jars for an ST project that we've uploaded to the OSS instance of Artifactory that JFrog
    runs.
    """
    from artificium.api import new_maven_client
    client = new_maven_client(ARTIFACTORY_INSTANCE, SNAPSHOT_REPO, is_snapshot=True)

    latest_jar = client.get_latest_version('com.smartertravel.metrics.aop.st-metrics', 'jar')
    print(latest_jar)

    assert latest_jar.startswith(
        ARTIFACTORY_INSTANCE + '/' + SNAPSHOT_REPO + '/com/smartertravel/metrics/aop/st-metrics')
    assert latest_jar.endswith('.jar')

    latest_sources = client.get_latest_version('com.smartertravel.metrics.aop.st-metrics', 'jar', descriptor='sources')
    print(latest_sources)

    assert latest_sources.startswith(
        ARTIFACTORY_INSTANCE + '/' + SNAPSHOT_REPO + '/com/smartertravel/metrics/aop/st-metrics')
    assert latest_sources.endswith('-sources.jar')


def test_get_latest_snapshot_versions():
    """Integration test to make sure we can get the latest snapshots (library and sources)
    jars for an ST project that we've uploaded to the OSS instance of Artifactory that JFrog
    runs.
    """
    from artificium.api import new_maven_client
    client = new_maven_client(ARTIFACTORY_INSTANCE, SNAPSHOT_REPO, is_snapshot=True)

    latest_jars = client.get_latest_versions('com.smartertravel.metrics.aop.st-metrics', 'jar')
    print(latest_jars)

    assert isinstance(latest_jars, list), "Expected list result from latest versions jar call"
    assert 1 <= len(latest_jars)

    latest_sources = client.get_latest_versions('com.smartertravel.metrics.aop.st-metrics', 'jar', descriptor='sources')
    print(latest_sources)

    assert isinstance(latest_sources, list), "Expected list result from latest versions sources call"
    assert 1 <= len(latest_sources)
