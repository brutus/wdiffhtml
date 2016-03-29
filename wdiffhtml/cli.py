#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Some function for CLI use…

These are also used by the start-skript - ``wdiffhtml`` - which is
created if this this package is installed.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import sys
import subprocess as sub

from argparse import (
  ArgumentParser,
  FileType,
)
from datetime import datetime

from . import (
  wdiff,
  __version__ as version,
  __doc__ as docstring,
)
from .settings import (
  Settings,
)
from .exceptions import (
  WdiffNotFoundError,
  ContextError,
)


__all__ = [
  'parse_commandline',
  'main',
]


def parse_commandline(argv):
  """
  Returns the arguments parsed from *argv* as a namespace.

  """
  ap = ArgumentParser(
    prog='wdiffhtml',
    description=docstring.split('\n\n')[0],
    epilog=docstring.split('\n\n')[-2],
  )
  ap.add_argument(
    '--version', action='version', version='wdiffhtml v{}'.format(version),
    help="shows version and exits"
  )
  ap.add_argument(
    'org_file', metavar='FILENAME',
    help="original file"
  )
  ap.add_argument(
    'new_file', metavar='FILENAME',
    help="changed file"
  )
  g_html = ap.add_argument_group(
    'Wrapper',
    "Without these settings, only the `wdiff` output is returned (with INS "
    "and DEL tags). Here are some options to wrap the output in a HTML "
    "document."
  )
  g_html.add_argument(
    '-w', '--wrap-with-html', action='store_true',
    help="wrap the diff with a HTML document"
  )
  g_html.add_argument(
    '-f', '--fold-breaks', action='store_true',
    help="fold line breaks (no BR tags in paragraphs)"
  )
  g_context = ap.add_argument_group(
    'Context',
    "With these options you can add additional information to the HTML "
    "output (means these only work alongside the `--wrap-with-html` option)."
  )
  g_context.add_argument(
    '-r', '--revision', metavar='STRING',
    help="add a revision tag or version number to the output"
  )
  x_stamp = g_context.add_mutually_exclusive_group()
  x_stamp.add_argument(
    '-d', '--datestamp', action='store_true',
    help="add a date to the output (UTC now)"
  )
  x_stamp.add_argument(
    '-D', '--timestamp', action='store_true',
    help="add date and time to the output (UTC now)"
  )
  g_files = ap.add_argument_group(
    'Files',
    "Instead of using the default templates, you can use your own files. "
    "These only work alongside the `--wrap-with-html` option"
  )
  g_files.add_argument(
    '-t', '--template', type=FileType('r'), metavar='FILE',
    help="load the Jinja2 template from this file"
  )
  g_files.add_argument(
    '-c', '--css', type=FileType('r'), metavar='FILE',
    help="load CSS from this file"
  )
  g_files.add_argument(
    '-j', '--js', type=FileType('r'), metavar='FILE',
    help="load Javascript from this file"
  )
  g_files.add_argument(
    '-J', '--js2', type=FileType('r'), metavar='FILE',
    help="load another Javascript from this file (like Zepto)"
  )
  # parse args
  args = ap.parse_args(argv)
  # check for wrapper
  if not args.wrap_with_html:
    # check context arguments and file arguments
    for group in (g_context, g_files):
      args_to_check = [opt.dest for opt in group._group_actions]
      if any([getattr(args, attr) for attr in args_to_check]):
        msg = "the options require that `--wrap-with-html` is used"
        ap.error(msg)
  return args


def get_context(args):
  """
  Returns a context from the namespace *args* (command line arguments).

  """
  context = {}
  if args.revision:
    context['version'] = args.revision
  if args.datestamp:
    context['timestamp'] = "{:%Y-%m-%d}".format(datetime.utcnow())
  if args.timestamp:
    context['timestamp'] = "{:%Y-%m-%d %H:%M}".format(datetime.utcnow())
  if args.template:
    context['template'] = args.template.read()
  if args.css:
    context['css'] = args.css.read()
  if args.js:
    context['js'] = args.js.read()
  return context


def main(argv=None):
  """
  Calls :func:`wdiff` and prints the results to STDERR.

  Parses the options for :meth:`wdiff` with :func:`parse_commandline`. If
  *argv* is supplied, it is used as command line, else the actual one is used.

  Return Codes
  ------------

  0: okay
  1: error with arguments
  2: `wdiff` not found
  3: error running `wdiff`

  """
  args = parse_commandline(argv)
  try:
    context = get_context(args)
    settings = Settings(args.org_file, args.new_file, **context)
    results = wdiff(settings, args.wrap_with_html, args.fold_breaks)
    print(results)
    return 0
  except ContextError as err:
    print("ERROR: {}.".format(err), file=sys.stderr)
    return 1
  except WdiffNotFoundError as err:
    print("ERROR: {}.".format(err), file=sys.stderr)
    return 2
  except sub.CalledProcessError as err:
    print("ERROR: {}.".format(err), file=sys.stderr)
    return 3


if __name__ == '__main__':
  sys.exit(main())
