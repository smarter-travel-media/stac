Changelog
=========

1.0.1 - 2016-03-09
------------------
* Change :class:`stac.exceptions.NoMatchingVersionsError` to be a subclass of the base
  :class:`stac.exceptions.StacError` exception.
* Change :func:`stac.util.get_logger` to get the ``stac`` named logger.

1.0.0 - 2016-02-09
------------------
* This is the first stable release of Stac. From this point on, all breaking changes will only
  be made in major version releases. This release is functionally the same as the ``0.3.1`` release.

0.3.1 - 2016-01-25
------------------
* Fix instance where ``GenericArtifactoryClient`` would not correctly handle artifacts without a ``.`` in
  the name.

0.3.0 - 2015-12-24
------------------
* **Breaking change** - Rename ``MavenArtifactoryClient`` to ``GenericArtifactoryClient`` and move all Maven-
  specific logic to a URL generator class that can be injected into it. Users creating the client via
  ``new_maven_client`` shouldn't notice any changes.

0.2.0 - 2015-12-23
------------------
* **Breaking change** - ``get_latest_version`` and ``get_latest_versions`` methods in the client now return
  version numbers only. Callers can use the ``get_version_url`` method to construct artifact URLs if desired.

0.1.1 - 2015-12-22
------------------
* Gracefully handle the case when we are looking for the latest SNAPSHOT version but
  there have not been any integration deploys to a repository. Fixes
  `#1 <https://github.com/smarter-travel-media/stac/issues/1>`_.

0.1.0 - 2015-12-21
------------------
* Initial release
