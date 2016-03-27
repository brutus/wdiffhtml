# -*- coding: UTF-8 -*-

"""
Uses `wdiff`_ to generate a word based *diff* from plain text files.

The results are modified to use HTML `<ins>` and `<del>` tags and can be
wrapped in a full HTML document.


.. _wdiff: https://www.gnu.org/software/wdiff/

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .utils import (
  generate_wdiff,
  wrap_content,
)


__all__ = [
  'wdiff',
]


def wdiff(settings, wrap_with_html=False, fold_breaks=False):
  """
  Returns the results of `wdiff` in a HTML compatible format.

  Needs a :cls:`settings.Settings` object.

  If *wrap_with_html* is set, a full HTML document is returned.

  If *fold_breaks* is set, linebreaks are *not* replaced with `<br />` tags.

  """
  diff = generate_wdiff(settings.org_file, settings.new_file)
  if wrap_with_html:
    return wrap_content(diff, settings, fold_breaks)
  else:
    return diff
