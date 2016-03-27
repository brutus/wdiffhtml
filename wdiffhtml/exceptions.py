# -*- coding: UTF-8 -*-

"""
Some exceptions.

"""


class WdiffHtmlError(Exception):
  """Base Exception…"""


class WdiffNotFoundError(WdiffHtmlError):
 """Raised if the `wdiff` command is not found."""


class ContextError(WdiffHtmlError):
  """Raised on missing context variables."""
