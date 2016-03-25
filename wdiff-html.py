#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Uses `wdiff`_ to generate a word based *diff* from plain text files.

The results are modified to use HTML `<ins>` and `<del>` tags and can be
wrapped in a full HTML document.


.. _wdiff: https://www.gnu.org/software/wdiff/

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import sys
import subprocess as sub

from argparse import ArgumentParser
from pathlib import Path


__version__ = '0.2.0'
__license__ = 'GNU General Public License v3 or above - '\
              'http://www.opensource.org/licenses/gpl-3.0.html'


CMD_WDIFF = 'wdiff'


OPTIONS = [
  '--start-delete', '<del>',
  '--end-delete', '</del>',
  '--start-insert', '<ins>',
  '--end-insert', '</ins>',
]

OPTIONS_LINEBREAK = [
  '-n',
]

TEMPLATE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="application-name" content="HTML wdiff">
  <title>HTML wdiff — {org_file} vs {new_file}</title>
  <style>{css}</style>
</head>
<body>
<div id="root">
  <article id="main">
    <header>
      <h1><span>{org_file}</span> vs <span>{new_file}</span></h1>
    </header>
    <section id="content">
{content}
    </section>
  </article>
</div>
</body>
</html>"""

CSS = """html,body,#main{margin:0;padding:0}ins,del{text-decoration:none;border:none;outline:none;padding:0 2px}html{font-size:10px;font-size:62.5%;background:#373a3c}body{color:#fff;background:#373a3c;line-height:1.5;font-size:180%;font-family:"Liberation Sans","Noto Sans","Droid Sans","Linux Biolinum","Ubuntu";font-feature-settings:"kern","liga","pnum"}header h1{color:#55595c}header h1 span{color:#fff;font-family:"Ubuntu Monospace","Liberation Mono","Droid Sans Mono"}header h1 span:before{color:#55595c;content:"`"}header h1 span:after{color:#55595c;content:"`"}h1{margin:1.5em 0 0.75em;line-height:1.2;font-weight:600;font-size:175%;color:#fff}p{line-height:1.5;margin:0 0 1.5em}p:last-child{margin-bottom:0}ins{background-color:rgba(92,184,92,0.85)}del{background-color:rgba(217,83,79,0.85);opacity:0.75}#root{max-width:800px;margin:0 auto}#content{margin:0 0 1.5em;padding:0.375em 0.75em;color:#373a3c;background:#f7f7f9;border:1px solid #818a91;border-radius:3px}
"""


class WdiffNotFoundError(Exception):

  """
  This exception is raised, if the `wdiff` command is not found.

  """

  RET_CODE = 2

  ERR_MESSAGE = 'the `{}` command can\'t be found'.format(CMD_WDIFF)

  def __init__(self):
    self.args = [self.ERR_MESSAGE]


def parse_commandline(argv):
  """
  Returns the arguments parsed from *argv* as a namespace.

  """
  ap = ArgumentParser(
    description=__doc__.split('\n\n')[0],
    epilog=__doc__.split('\n\n')[-2],
  )
  ap.add_argument(
    'org_file', metavar='FILENAME',
    help="original file"
  )
  ap.add_argument(
    'new_file', metavar='FILENAME',
    help="changed file"
  )
  ap.add_argument(
    '-f', '--fold-breaks', action='store_true',
    help="fold linebreaks"
  )
  ap.add_argument(
    '-w', '--wrap-html', action='store_true',
    help="wrap the diff with HTML"
  )
  return ap.parse_args(argv)


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
    raise WdiffNotFoundError()


def generate_wdiff(org_file, new_file):
  """
  Returns the results from the `wdiff` command as a string.

  HTML `<ins>` and `<del>` tags will be used instead of the default markings.

  Raises:

    subrocess.CalledProcessError: on any `wdiff` process errors

  """
  check_for_wdiff()
  cmd = [CMD_WDIFF]
  cmd.extend(OPTIONS)
  cmd.extend([org_file, new_file])
  proc = sub.Popen(cmd, stdout=sub.PIPE)
  diff, _ = proc.communicate()
  return diff.decode('utf-8')


def build_para(content, fold_breaks=False):
  """
  Returns *content* wrapped in P tags.

  All linebreaks (`\\n`) are replaced with `<br />` tags, unless
  *fold_breaks* is set.

  """
  lines = [line.strip() for line in content.split('\n')]
  if not fold_breaks:
    for line_number in range(len(lines) - 1):
      lines[line_number] = "{}<br />".format(lines[line_number])
  return "<p>{}</p>".format('\n'.join(lines))


def wrap_paragraphs(content, fold_breaks=False):
  """
  Returns *content* with paragraphs wrapped in P tags.

  """
  paras = [
    build_para(para.strip(), fold_breaks) for para in content.split('\n\n')
  ]
  return '\n'.join(paras)


def wrap_content(org_file, new_file, content):
  """
  Returns *content* wrapped in a HTML structure as a string.

  """
  context = {
    'org_file': Path(org_file).name,
    'new_file': Path(new_file).name,
    'content': content,
    'css': CSS,
  }
  return TEMPLATE.format(**context)


def wdiff(org_file, new_file, wrap_with_html=False, fold_breaks=False):
  """
  Returns the results of `wdiff` in a HTML compatible format.

  If *wrap_with_html* is set, a full HTML document is returned.

  """
  diff = generate_wdiff(org_file, new_file)
  if wrap_with_html:
    paras = wrap_paragraphs(diff, fold_breaks)
    return wrap_content(org_file, new_file, paras)
  else:
    return diff


def main(argv=None):
  args = parse_commandline(argv)
  try:
    results = wdiff(
      args.org_file, args.new_file, args.wrap_html, args.fold_breaks
    )
    print(results)
    return 0
  except WdiffNotFoundError as err:
    print("ERROR: {}.".format(err), file=sys.stderr)
    return err.RET_CODE
  except sub.CalledProcessError as err:
    print("ERROR: {}.".format(err), file=sys.stderr)
    return 3


if __name__ == '__main__':
  sys.exit(main())
