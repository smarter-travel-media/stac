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

"""

from abc import ABCMeta, abstractmethod

DEFAULT_RELEASE_LIMIT = 5


class ArtifactoryClient(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_release(self, full_name, version):
        pass

    @abstractmethod
    def get_latest_release(self, full_name):
        pass

    @abstractmethod
    def get_latest_releases(self, full_name, limit=DEFAULT_RELEASE_LIMIT):
        pass



