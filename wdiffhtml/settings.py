# -*- coding: UTF-8 -*-

"""
Some global constants and a settings object, that stores the template and
it's context along with the filenames for the diff…

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from pathlib import Path

from pkg_resources import resource_string

from appdirs import user_data_dir


__all__ = [
  'Settings',
]


CMD_WDIFF = 'wdiff'

OPTIONS_LINEBREAK = [
  '-n',
]

OPTIONS_OUTPUT = [
  '--start-delete', '<del>',
  '--end-delete', '</del>',
  '--start-insert', '<ins>',
  '--end-insert', '</ins>',
]


def load_from_resource(name):
  """
  Returns the contents of a file resource.

  If the resource exists in the users data directory, it is used instead
  of the default resource.

  """
  filepath = Path(user_data_dir('wdiffhtml')) / name
  if filepath.exists():
    with filepath.open() as fh:
      return fh.read()
  else:
    return resource_string('wdiffhtml', 'data/' + name).decode('utf-8')


class Settings(object):

  """
  The class holds the path to the files that should be compared as well as
  the template used for the output along with it's context.

  Context Variables
  -----------------

  `org_filename`
    Display version of the name of the original file.

  `new_filename`
    Display version of the name of the changed file.

  `content`
    Will contain the (HTMLified) output from `wdiff` (just a placeholder).

  `css`
    CSS for the document.

  `js`
    JS for the document.

  `js`
    Secondary JS for the document (loaded before the first, for frameworks…).

  `timestamp`
    :cls:`datetime.datetime` of the diff (optional).

  `version`
    revision or version of the diff (optional).

  """

  template = load_from_resource('template.jinja')

  _context = {
    'content': "",
    'css': load_from_resource('styles.css'),
    'js': load_from_resource('main.js'),
    'js2': load_from_resource('secondary.js'),
  }

  def __init__(self, org_file, new_file, template=None, **context):
    self.org_file = org_file
    self.new_file = new_file
    if template:
      self.template = template
    self.context = self._context.copy()
    self.context['org_filename'] = Path(org_file).name
    self.context['new_filename'] = Path(new_file).name
    self.context.update(context)
