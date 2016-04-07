# -*- coding: UTF-8 -*-

"""
Some exceptions.

"""

from __future__ import absolute_import
from __future__ import unicode_literals


class WdiffHtmlError(Exception):
  """Base Exception…"""


class WdiffNotFoundError(WdiffHtmlError):
 """Raised if the `wdiff` command is not found."""


class ContextError(WdiffHtmlError):
  """Raised on missing context variables."""
