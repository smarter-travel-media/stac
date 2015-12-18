API
===

This section of the documentation covers the public interfaces of Stac.

.. note::

    When using the library, always make sure to access classes and functions through
    the :mod:`stac.api` module, not each individual module.



Clients
-------

The classes and functions in the :mod:`stac.client` module make up the main interface to
the Stac library. Unless you're doing something non-typical, this is probably all you need
to worry about.

.. autoclass:: stac.client.ArtifactoryClient
    :inherited-members:

.. autoclass:: stac.client.MavenArtifactoryClient
    :inherited-members:
    :special-members: __init__

.. autoclass:: stac.client.MavenArtifactoryClientConfig
    :inherited-members:

.. autofunction:: stac.client.new_maven_client

HTTP Dao
--------

If you need to customize how the Stac library interacts with Artifactory over HTTP, the
:mod:`stac.http` module probably has what you're looking for.

.. autoclass:: stac.http.VersionApiDao
    :inherited-members:
    :special-members: __init__

Exceptions
----------

.. autoclass:: stac.exceptions.StacError
.. autoclass:: stac.exceptions.NoMatchingVersionsError
