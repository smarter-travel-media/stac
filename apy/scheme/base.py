# -*- coding: utf-8 -*-

"""
"""

from abc import ABCMeta, abstractmethod

DEFAULT_RELEASE_LIMIT = 5


class ArtifactoryClient(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_release(self, group, artifact, version):
        pass

    @abstractmethod
    def get_latest_release(self, group, artifact):
        pass

    @abstractmethod
    def get_latest_releases(self, group, artifact, limit=DEFAULT_RELEASE_LIMIT):
        pass
