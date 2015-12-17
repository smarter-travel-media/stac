Advanced Usage
==============

Some more advanced or non-typical usages of Stac will be outlined below.

Use HTTP Authentication
-----------------------

You might have noticed we aren't using authentication to access the Artifactory API anywhere in the
:doc:`quickstart` section. If you've set up your Artifactory API (and the artifacts contained within it) to require
authentication, this is fairly easy to work with in Stac.

.. code-block:: python

    import stac.api

    client = stac.api.new_maven_client(
        'https://internal.example.com/artifactory', 'libs-release', username="deploy", password="authIs4wesom3!")
    jar = client.get_latest_version('com.example.services.ads', 'jar')
    print(jar) # 'https://internal.example.com/artifactory/libs-release/com/example/services/ads/5.4.1/ads-5.4.1.jar'


Use a Custom HTTP Session
-------------------------

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
---------------------

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
