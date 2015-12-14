# -*- coding: utf-8 -*-
#
# Artificium - Artifactory Search Client
#
# Copyright 2015 Smarter Travel
#
# Available under the MIT license. See LICENSE for details.
#

"""
artificium.util
~~~~~~~~~~~~~~~

Miscellaneous utility methods for the Artificium library.
"""

from __future__ import absolute_import

import logging


def get_log():
    """Get the singleton :class:`logging.Logger` instance for the Artifacts library.

    :return: The logger instance for the library
    :rtype: logging.Logger
    """
    return logging.getLogger('artifacts')
