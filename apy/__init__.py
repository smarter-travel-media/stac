# -*- coding: utf-8 -*-

"""
"""

from __future__ import print_function, division

from abc import ABCMeta, abstractmethod


class ArtifactoryClient(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_release(self, artifact, group):
        pass

    @abstractmethod
    def get_latest_releases(self, artifact, group, limit=None):
        pass
