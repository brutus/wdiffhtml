# -*- coding: UTF-8 -*-

"""
Some global constants and a settings object, that stores the template and
it's context along with the filenames…

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from pathlib import Path

from pkg_resources import resource_string


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
  Returns the contonts of o file resource.

  """
  return resource_string('wdiffhtml', 'data/' + name).decode('utf-8')


class Settings(object):

  """
  The class holds the path to the files that should be compared as well as
  the template used for the output along with it's context.

  Context Variables
  -----------------

  `org_filename`
    Display version ot the name of the original file.

  `new_filename`
    Display version ot the name of the changed file.

  `content`
    Will contain the (HTMLified) output from `wdiff` (just a placeholder).

  `css`
    CSS for the document.

  `js`
    JS for the document.

  """

  template = load_from_resource('template.html')

  _context = {
    'content': "",
    'css': load_from_resource('styles.css'),
    'js': load_from_resource('main.js'),
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
