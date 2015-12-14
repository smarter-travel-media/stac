# -*- coding: utf-8 -*-
#
# Stac - Smarter Travel Artifactory Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
stac.util
~~~~~~~~~

Miscellaneous utility methods for the Stac library.
"""

from __future__ import absolute_import

import logging


def get_log():
    """Get the singleton :class:`logging.Logger` instance for the Stac library.

    :return: The logger instance for the library
    :rtype: logging.Logger
    """
    return logging.getLogger('artifacts')
