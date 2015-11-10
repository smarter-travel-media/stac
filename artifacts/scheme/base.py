# -*- coding: utf-8 -*-
#
# Artifacts - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artifacts.scheme.base
~~~~~~~~~~~~~~~~~~~~~

Interface for clients that interact with Artifactory.
"""

from __future__ import absolute_import

from abc import ABCMeta, abstractmethod

DEFAULT_RELEASE_LIMIT = 5


class ArtifactoryClient(object):
    """Interface for getting artifact paths based on an artifact name.






    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_release(self, full_name, version, descriptor=None):
        pass

    @abstractmethod
    def get_latest_release(self, full_name, descriptor=None):
        pass

    @abstractmethod
    def get_latest_releases(self, full_name, descriptor=None, limit=DEFAULT_RELEASE_LIMIT):
        pass

