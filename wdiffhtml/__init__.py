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

__version__ = '0.5.3'

__author__ = 'Brutus [DMC] <brutus.dmc@googlemail.com>'
__license__ = (
  'GNU General Public License v3 or above - ',
  'http://www.opensource.org/licenses/gpl-3.0.html',
)


def wdiff(settings, wrap_with_html=False, fold_breaks=False):
  """
  Returns the results of `wdiff` in a HTML compatible format.

  Needs a :cls:`settings.Settings` object.

  If *wrap_with_html* is set, the *diff* is returned in a full HTML document
  structure.

  If *fold_breaks* is set, line breaks **are not** replaced with
  `<br />` tags.

  """
  diff = generate_wdiff(settings.org_file, settings.new_file, fold_breaks)
  if wrap_with_html:
    return wrap_content(diff, settings, fold_breaks)
  else:
    return diff
