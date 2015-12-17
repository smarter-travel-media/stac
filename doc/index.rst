.. artifacts documentation master file, created by
   sphinx-quickstart on Thu Oct 22 12:23:36 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Stac - Smarter Travel Artifactory Client
========================================

**WARNING - This is super pre-alpha-barely-works software right now**

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
    >>> client.get_latest_version('com.example.services.auth', 'jar')
    'https://www.example.com/artifactory/libs-release/com/example/services/auth/1.2.3/auth-1.2.3.jar'



Contents
--------

.. toctree::
   :maxdepth: 2

   usage
   api
   changes



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

