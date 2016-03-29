# -*- coding: UTF-8 -*-

"""
Some functions to generate HTMLified diffs with `wdiff`.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import subprocess as sub

from jinja2 import Template

from .exceptions import (
  WdiffNotFoundError,
  ContextError,
)
from .settings import (
  CMD_WDIFF,
  OPTIONS_LINEBREAK,
  OPTIONS_OUTPUT,
)


__all__ = [
  'WdiffNotFoundError',
  'check_for_wdiff',
  'generate_wdiff',
  'build_paragraph',
  'wrap_paragraphs',
  'wrap_content',
]


def check_for_wdiff():
  """
  Checks if the `wdiff` command can be found.

  Raises:

    WdiffNotFoundError: if ``wdiff`` is not found.

  """
  cmd = ['which', CMD_WDIFF]
  proc = sub.Popen(cmd, stdout=sub.DEVNULL)
  proc.wait()
  if proc.returncode != 0:
    msg = "the `{}` command can't be found".format(CMD_WDIFF)
    raise WdiffNotFoundError(msg)


def generate_wdiff(org_file, new_file, fold_breaks=False, html=True):
  """
  Returns the results from the `wdiff` command as a string.

  HTML `<ins>` and `<del>` tags will be used instead of the default markings.

  If *fold_breaks* is set, `<ins>` and `<del>` tags are allowed to span
  lines breaks (option `-n` is not used). If *html* is not set, the output
  of `wdiff` is returned as it is.

  Raises:

    subrocess.CalledProcessError: on any `wdiff` process errors

  """
  check_for_wdiff()
  cmd = [CMD_WDIFF]
  if html:
    cmd.extend(OPTIONS_OUTPUT)
  if not fold_breaks:
    cmd.extend(OPTIONS_LINEBREAK)
  cmd.extend([org_file, new_file])
  proc = sub.Popen(cmd, stdout=sub.PIPE)
  diff, _ = proc.communicate()
  return diff.decode('utf-8')


def build_paragraph(content, fold_breaks=False):
  """
  Returns *content* wrapped in `<p>` tags.

  All line breaks (`\\n`) except the last are converted to `<br />` tags,
  unless *fold_breaks* is set.

  """
  lines = list(filter(None, [line.strip() for line in content.split('\n')]))
  if not fold_breaks:
    for line_number in range(len(lines) - 1):
      lines[line_number] = "{}<br />".format(lines[line_number])
  return "<p>{}</p>".format('\n'.join(lines))


def wrap_paragraphs(content, fold_breaks=False):
  """
  Returns *content* with all paragraphs wrapped in `<p>` tags.

  If *fold_breaks* is set, line breaks are converted to `<br />` tags.

  """
  paras = filter(None, [para.strip() for para in content.split('\n\n')])
  paras = [build_paragraph(para, fold_breaks) for para in paras]
  return '\n'.join(paras)


def wrap_content(content, settings, fold_breaks=False):
  """
  Returns *content* wrapped in a HTML structure.

  If *fold_breaks* is set, line breaks are converted to `<br />` tags.

  """
  settings.context['content'] = wrap_paragraphs(content, fold_breaks)
  template = Template(settings.template)
  try:
    return template.render(**settings.context)
  except KeyError as error:
    msg = "missing context setting: {}".format(error)
    raise ContextError(msg)
