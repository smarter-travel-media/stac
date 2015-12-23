Changelog
=========

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
