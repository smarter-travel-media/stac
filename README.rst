Stac - Smarter Travel Artifactory Client
========================================

.. image:: https://travis-ci.org/smarter-travel-media/stac.svg?branch=master
    :target: https://travis-ci.org/smarter-travel-media/stac

**WARNING - This is alpha software and subject to bugs and/or breaking changes**

Stac is a tiny Artifactory client designed for getting the most recent version (or versions)
of a project from an Artifactory server. The target use case is downloading project artifacts
as part of a deploy process.

Given a few pieces of information, it can generate URLs to the most recent version of an
artifact to be downloaded as part of your deploy process. Currently, only Maven repository
layouts (in Artifactory parlance) are supported.

Installation
------------

To install Stac, simply run:

.. code-block:: bash

    $ pip install stac


Dependencies
------------
* `requests <https://github.com/kennethreitz/requests>`_  by Kenneth Reitz

Usage
-----

Using Stac is easy!

.. code-block:: python

    >>> from stac.api import new_maven_client
    >>> client = new_maven_client('https://www.example.com/artifactory', 'libs-release')
    >>> version = client.get_latest_version('com.example.services.authentication')
    >>> version
    '1.2.3'
    >>> url = client.get_version_url('com.example.services.authentication', 'jar', version)
    >>> url
    'https://www.example.com/artifactory/libs-release/com/example/services/authentication/1.2.3/authentication-1.2.3.jar'

