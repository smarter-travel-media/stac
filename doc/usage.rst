Usage Examples
==============

The following examples will walk through some common uses of the :class:`stac.client.ArtifactoryClient`
implementation for Maven repository layouts (:class:`stac.client.MavenArtifactoryClient`). Since this
client is focused on deploy related use cases, the examples below will as well.

Basic Usage
-----------

Basic usage of Stac is pretty, well, basic. Just use the :func:`stac.client.new_maven_client` factory
method to create a client instance and you're good to go. Some common use cases are given below.

Get a Specific Version
~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to get the most recent release version of a project, Stac can determine that based on the
name of your project and repository.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-release')
    jar = client.get_latest_version('com.example.services.auth', 'jar')
    print(jar) # 'https://www.example.com/artifactory/libs-release/com/example/services/auth/1.3.0/auth-1.3.0.jar'

In the example above, the ``jar`` variable will be the full URL to download version 1.3.0 (the most
recent release) of some hypothetical authentication service. If there haven't been any releases of this
service an exception will be raised. See :meth:`stac.client.ArtifactoryClient.get_latest_version` for
more information.

Get the Latest Snapshot Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Maybe you want to determine the most recent snapshot version of your project (potentially to deploy it to your
continuous integration server). Stac can also help you out with this. However, you need to explicitly tell
the client that you are looking for snapshot, or integration, versions.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-snapshot', is_snapshot=True)
    jar = client.get_latest_version('com.example.services.locations', 'jar')
    print(jar) # 'https://www.example.com/artifactory/libs-snapshot/com/example/services/locations/4.1.0-SNAPSHOT/locations-4.1.0-SNAPSHOT.jar'

In the example above, the ``jar`` variable will be the full URL to download version 4.1.0 (the most recent
snapshot / integration version) of some hypothetical location service. If there haven't been any snapshot
versions of this service created, an exception will be raised. See :meth:`stac.client.ArtifactoryClient.get_latest_version`
for more information.

Get the Latest N Release Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to get more than a single most recent release version, the process is outlined below (spoiler:
it's pretty much the same as getting the single most recent release version).

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-release')
    jars = client.get_latest_versions('com.example.services.auth', 'jar', limit=3)
    print(jar)
    # [
    #   'https://www.example.com/artifactory/libs-release/com/example/services/auth/1.3.0/auth-1.3.0.jar',
    #   'https://www.example.com/artifactory/libs-release/com/example/services/auth/1.2.8/auth-1.2.8.jar',
    #   'https://www.example.com/artifactory/libs-release/com/example/services/auth/1.2.3/auth-1.2.3.jar'
    # ]

As you can see, the ``jars`` variable is the most recent three releases (because we only asked for three), ordered
with the most recent version first.

Get the Latest N Snapshot Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to get more than a single most recent snapshot version, the process is outlined below (you might
have guessed: it's pretty much the same as getting the single most recent snapshot version). This differs
from getting the most recent N release versions because you must tell the client you are explicitly looking
for snapshot versions.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-snapshot', is_snapshot=True)
    jars = client.get_latest_versions('com.example.services.locations', 'jar', limit=3)
    print(jar)
    # [
    #   'https://www.example.com/artifactory/libs-snapshot/com/example/services/locations/4.1.0-SNAPSHOT/locations-4.1.0-SNAPSHOT.jar',
    #   'https://www.example.com/artifactory/libs-snapshot/com/example/services/locations/4.0.0-SNAPSHOT/locations-4.0.0-SNAPSHOT.jar',
    #   'https://www.example.com/artifactory/libs-snapshot/com/example/services/locations/3.12.0-SNAPSHOT/locations-3.12.0-SNAPSHOT.jar'
    # ]

As you can see, the ``jars`` variable is the most recent three snapshots (because we only asked for three), ordered
with the most recent version first.

Advanced Usage
--------------

Some more advanced or non-typical usages of Stac will be outlined below.

Use HTTP Authentication
~~~~~~~~~~~~~~~~~~~~~~~

You might have noticed we aren't using authentication to access the Artifactory API anywhere in the
examples above. If you've set up your Artifactory API (and the artifacts contained within it) to require
authentication, this is fairly easy to work with in Stac.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client(
        'https://internal.example.com/artifactory', 'libs-release', username="deploy", password="authIs4wesom3!")
    jar = client.get_latest_version('com.example.services.ads', 'jar')
    print(jar) # 'https://internal.example.com/artifactory/libs-release/com/example/services/ads/5.4.1/ads-5.4.1.jar'


Use a Custom HTTP Session
~~~~~~~~~~~~~~~~~~~~~~~~~

Stac uses the `Requests <http://docs.python-requests.org/en/latest/>`_ library for making HTTP requests (if you
aren't familiar with Requests, check it out, it's awesome). In most cases, Stac will create a new ``requests.Session``
object when a client is created and you really shouldn't need to worry about this detail. However, if you've got
special requirements (maybe you need to disable certificate validation or something) you can supply your own
``requests.Session`` object to the client.

Doing this is a little more involved than just creating a standard client but it's still not *that* bad.

.. code-block:: python

    import requests
    import stac.api

    # Create a custom session object...
    session = requests.Session()
    # And configure it
    session.verify = False

    # Create a custom API DAO that will use our session
    dao = stac.api.VersionApiDao(session, 'https://repo.example.com/artifactory', 'libs-release')

    # Construct the configuration for the client
    client_config = stac.api.MavenArtifactoryClientConfig()
    client_config.base_url = 'https://repo.example.com/artifactory'
    client_config.repo = 'libs-release'
    client_config.dao = dao

    # Create the client instance
    client = stac.api.MavenArtifactoryClient(client_config)

    # Use it as normal
    jar = client.get_latest_version('com.example.services.locations', 'jar')
    print(jar) # 'https://repo.example.com/artifactory/libs-release/com/example/services/locations/4.0.5/locations-4.0.5.jar'


Get Custom Assemblies
~~~~~~~~~~~~~~~~~~~~~

At Smarter Travel, when we build and release an application jar to Artifactory, we also release a few
associated jars at the same time. Source code, documentation, and runtime configuration are typically
built and released at the same time. In Maven terms, these are known as "assemblies". Stac has support
for finding these assemblies by passing the ``descriptor='blah'`` argument to the desired method. An example
is given below.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client('https://www.example.com/artifactory', 'libs-release')

    source_jar = client.get_latest_version('com.example.services.mail', 'jar', descriptor='sources')
    print(source_jar) # 'https://www.example.com/artifactory/libs-release/com/example/services/mail/9.2.1/mail-9.2.1-sources.jar'

    config_jar = client.get_latest_version('com.example.services.mail', 'jar', descriptor='config')
    print(config_jar) # 'https://www.example.com/artifactory/libs-release/com/example/services/mail/9.2.1/mail-9.2.1-config.jar'

As you can see, we were able to find the most recent version of the source code and configuration associated
with a hypothetical mail service.


