# -*- coding: UTF-8 -*-

"""
Some global constants and a settings object, that stores the template and
it's context along with the filenames…

"""

from __future__ import absolute_import
from __future__ import unicode_literals


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

  template = """<!doctype html>
  <html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="application-name" content="html wdiff">
    <title>html wdiff — {org_filename} vs {new_filename}</title>
    <style>{css}</style>
  </head>
  <body>
  <div id="root">
    <article id="main">
      <header>
        <h1><span>{org_filename}</span> vs <span>{new_filename}</span></h1>
      </header>
      <section id="content">
  <!-- start of diff content -->
  {content}
  <!-- end of diff content -->
      </section>

    </article>
  </div>  <!-- #root -->
  <script>{js}</script>
  </body>
  </html>"""

  _context = {
    'content': "",
    'css': """html,body,#main{margin:0;padding:0}ins,del{text-decoration:none;border:none;outline:none;padding:0 2px}html{font-size:10px;font-size:62.5%;background:#373a3c}body{color:#fff;background:#373a3c;line-height:1.5;font-size:180%;font-family:"liberation sans","noto sans","droid sans","linux biolinum","ubuntu";font-feature-settings:"kern","liga","pnum"}header h1{color:#55595c}header h1 span{color:#fff;font-family:"ubuntu monospace","liberation mono","droid sans mono"}header h1 span:before{color:#55595c;content:"`"}header h1 span:after{color:#55595c;content:"`"}h1{margin:1.5em 0 0.75em;line-height:1.2;font-weight:600;font-size:175%;color:#fff}p{line-height:1.5;margin:0 0 1.5em}p:last-child{margin-bottom:0}ins{background-color:rgba(92,184,92,0.85)}del{background-color:rgba(217,83,79,0.85);opacity:0.75}#root{max-width:800px;margin:0 auto}#content{margin:0 0 1.5em;padding:0.375em 0.75em;color:#373a3c;background:#f7f7f9;border:1px solid #818a91;border-radius:3px}
    """,
    'js': "",
  }

  def __init__(self, org_file, new_file, template=None, **context):
    self.org_file = org_file
    self.new_file = new_file
    if template:
      self.template = template
    self.context = self._context.copy()
    self.context.update(context)
