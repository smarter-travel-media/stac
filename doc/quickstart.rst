Quickstart
==========

The following examples will walk through some simple uses of the :class:`stac.client.ArtifactoryClient`
implementation for Maven repository layouts (:class:`stac.client.GenericArtifactoryClient` paired with
:class:`stac.client.MavenArtifactUrlGenerator`). Since this client is focused on deploy related use cases,
the examples below will as well.

Get a Specific Version
----------------------

If you already know what version you want to download / deploy, Stac can turn that version number
into a URL for you based on the name of your project and repository.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-release')
    war = client.get_version('com.example.services.users', 'war', '1.2.4')
    print(war) # 'https://www.example.com/artifactory/libs-release/com/example/services/users/1.2.4/users-1.2.4.war'

In the example above, the ``war`` variable will be the full URL to download version 1.2.4 of some
hypothetical users service.

Get the Latest Release Version
------------------------------

If you want to get the most recent release version of a project, Stac can determine that based on the
name of your project and repository.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-release')

    version = client.get_latest_version('com.example.services.auth')
    print(version) # '1.3.0'

    jar = client.get_version_url('com.example.services.auth', 'jar', version)
    print(jar) # 'https://www.example.com/artifactory/libs-release/com/example/services/auth/1.3.0/auth-1.3.0.jar'

In the example above, ``version`` will be the string ``1.3.0`` and the ``jar`` variable will be the full
URL to download version 1.3.0 (the most recent release) of some hypothetical authentication service. If
there haven't been any releases of this service an exception will be raised.

Get the Latest Snapshot Version
-------------------------------

Maybe you want to determine the most recent snapshot version of your project (potentially to deploy it to your
continuous integration server). Stac can also help you out with this. However, you need to explicitly tell
the client that you are looking for snapshot, or integration, versions.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-snapshot', is_snapshot=True)

    version = client.get_latest_version('com.example.services.locations')
    print(version) # '4.1.0-SNAPSHOT'

    jar = client.get_version_url('com.example.services.locations', 'jar', version)
    print(jar) # 'https://www.example.com/artifactory/libs-snapshot/com/example/services/locations/4.1.0-SNAPSHOT/locations-4.1.0-SNAPSHOT.jar'

In the example above, ``version`` will be the string ``4.1.0-SNAPSHOT`` and the ``jar`` variable will be
the full URL to download version 4.1.0 (the most recent snapshot / integration version) of some hypothetical
location service. If there haven't been any snapshot versions of this service created, an exception will be
raised.

Get the Latest N Release Versions
---------------------------------

If you need to get more than a single most recent release version, the process is outlined below (spoiler:
it's pretty much the same as getting the single most recent release version).

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-release')

    versions = client.get_latest_versions('com.example.services.auth', limit=3)
    print(versions)
    # [
    #   '1.3.0',
    #   '1.2.8',
    #   '1.2.3'
    # ]

    jars = [client.get_version_url('com.example.services.auth', 'jar', version) for version in versions]
    print(jars)
    # [
    #   'https://www.example.com/artifactory/libs-release/com/example/services/auth/1.3.0/auth-1.3.0.jar',
    #   'https://www.example.com/artifactory/libs-release/com/example/services/auth/1.2.8/auth-1.2.8.jar',
    #   'https://www.example.com/artifactory/libs-release/com/example/services/auth/1.2.3/auth-1.2.3.jar'
    # ]

As you can see, the ``versions`` variable will contain the version numbers of the three most recent releases
and the ``jars`` variable is the the full URL to each of the respective releases, ordered with the most recent
version first.

Get the Latest N Snapshot Versions
----------------------------------

If you need to get more than a single most recent snapshot version, the process is outlined below (you might
have guessed: it's pretty much the same as getting the single most recent snapshot version). This differs
from getting the most recent N release versions because you must tell the client you are explicitly looking
for snapshot versions.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-snapshot', is_snapshot=True)

    versions = client.get_latest_versions('com.example.services.locations', limit=3)
    print(versions)
    # [
    #   '4.1.0-SNAPSHOT',
    #   '4.0.0-SNAPSHOT',
    #   '3.12.0-SNAPSHOT'
    # ]

    jars = [client.get_version_url('com.example.services.locations', 'jar', version) for version in versions]
    print(jars)
    # [
    #   'https://www.example.com/artifactory/libs-snapshot/com/example/services/locations/4.1.0-SNAPSHOT/locations-4.1.0-SNAPSHOT.jar',
    #   'https://www.example.com/artifactory/libs-snapshot/com/example/services/locations/4.0.0-SNAPSHOT/locations-4.0.0-SNAPSHOT.jar',
    #   'https://www.example.com/artifactory/libs-snapshot/com/example/services/locations/3.12.0-SNAPSHOT/locations-3.12.0-SNAPSHOT.jar'
    # ]

As you can see, the  ``versions`` variable will contain the versions numbers of the three most recent snapshots and
the ``jars`` variable is the to each of the respective releases, ordered with the most recent version.
