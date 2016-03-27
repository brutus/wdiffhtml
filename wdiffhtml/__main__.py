#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Function to make the `wdiffhtml` package run-able.

These are also used by the start-skript - ``wdiffhtml`` - which is
created if this this package is installed.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import sys
import subprocess as sub

from argparse import ArgumentParser
from datetime import datetime

from . import (
  wdiff,
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
    description=docstring.split('\n\n')[0],
    epilog=docstring.split('\n\n')[-2],
  )
  ap.add_argument(
    'org_file', metavar='FILENAME',
    help="original file"
  )
  ap.add_argument(
    'new_file', metavar='FILENAME',
    help="changed file"
  )
  g_html = ap.add_argument_group('Wrapper')
  g_html.add_argument(
    '-f', '--fold-breaks', action='store_true',
    help="fold linebreaks"
  )
  g_html.add_argument(
    '-w', '--wrap-with-html', action='store_true',
    help="wrap the diff with HTML"
  )
  g_context = ap.add_argument_group('Context')
  g_context.add_argument(
    '-v', '--doc-version', metavar='STRING',
    help="add a revision version to the output"
  )
  x_stamp = g_context.add_mutually_exclusive_group()
  x_stamp.add_argument(
    '-d', '--datestamp', action='store_true',
    help="add a date to the output (UTC)"
  )
  x_stamp.add_argument(
    '-D', '--timestamp', action='store_true',
    help="add date and time to the output (UTC)"
  )
  return ap.parse_args(argv)


def main(argv=None):
  """
  Calls :func:`wdiff` and prints the results to STDERR.

  Parses the options for :meth:`wdiff` with :func:`parse_commandline`. If
  *argv* is supplied, it is used as commandline, else the actual one is used.

  Return Codes
  ------------

  0: okay
  1: error with arguments
  2: `wdiff` not found
  3: error running `wdiff`

  """
  args = parse_commandline(argv)
  try:
    context = {}
    if args.doc_version:
      context['version'] = args.doc_version
    if args.timestamp:
      context['timestamp'] = "{:%Y-%m-%d %H:%M}".format(datetime.utcnow())
    if args.datestamp:
      context['timestamp'] = "{:%Y-%m-%d}".format(datetime.utcnow())
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
