# -*- coding: utf-8 -*-
#
# Artifacts - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artifacts.util
~~~~~~~~~~~~~~

Miscellaneous utility methods for the Artifacts library.
"""

from __future__ import absolute_import

import logging


def get_log():
    """Get the singleton :class:`logging.Logger` instance for the Artifacts library.

    :return: The logger instance for the library
    :rtype: logging.Logger
    """
    return logging.getLogger('artifacts')
