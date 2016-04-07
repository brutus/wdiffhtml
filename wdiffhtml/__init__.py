# -*- coding: UTF-8 -*-

"""
Uses `wdiff`_ to generate a word based *diff* from plain text files.

The results are modified to use HTML `<ins>` and `<del>` tags and can be
wrapped in a full HTML document.


Example
-------

We want a wdiff from two files:

>>> oldfile = 'path/to/old_file.txt'
>>> newfile = 'some/new_version.txt'

To generate it from Python use `generate_wdiff`:

>>> diff = generate_wdiff(oldfile, newfile)

And to wrap it with HTML you can use `wrap_content` (which requires a
`Settings` object):

>>> settings = Settings(oldfile, newfile)
>>> html = wrap_content(diff, settings)

You can combine those two trough the `wdiff` function, which also requires a
`Settings` object and accepts some additional arguments.


.. _wdiff: https://www.gnu.org/software/wdiff/

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .settings import Settings
from .utils import (
  generate_wdiff,
  wrap_content,
)


__all__ = [
  'Settings',
  'wdiff',
  'generate_wdiff',
  'wrap_content',
]

__version__ = '0.6.1'

__author__ = 'Brutus [DMC] <brutus.dmc@googlemail.com>'
__license__ = (
  'GNU General Public License v3 or above - ',
  'http://www.opensource.org/licenses/gpl-3.0.html',
)


def wdiff(
  settings, wrap_with_html=False, fold_breaks=False, hard_breaks=False
):
  """
  Returns the results of `wdiff` in a HTML compatible format.

  Needs a :cls:`settings.Settings` object.

  If *wrap_with_html* is set, the *diff* is returned in a full HTML document
  structure.

  If *fold_breaks* is set, `<ins>` and `<del>` tags are allowed to span line
  breaks

  If *hard_breaks* is set, line breaks are replaced with `<br />` tags.

  """
  diff = generate_wdiff(settings.org_file, settings.new_file, fold_breaks)
  if wrap_with_html:
    return wrap_content(diff, settings, hard_breaks)
  else:
    return diff
