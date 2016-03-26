# -*- coding: UTF-8 -*-

"""
Some settings…

Template Variables
------------------

`org_file`
  Name of the original file.

`new_file`
  Name of the changed file.

`content`
  Will contain the (HTMLified) output from `wdiff`.

`css`
  CSS for the document.

`js`
  JS for the document.

"""


__all__ = [
  'CMD_WDIFF',
  'OPTIONS_LINEBREAK',
  'OPTIONS_OUTPUT',
  'TEMPLATE',
  'CSS',
  'JS',
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
<!-- START OF DIFF CONTENT -->
{content}
<!-- END OF DIFF CONTENT -->
    </section>
    <footer>
      <p><kbd>HTML wdiff</kbd></p>
    </footer>
  </article>
</div>  <!-- #root -->
<script>{js}</script>
</body>
</html>"""

CSS = """html,body,#main{margin:0;padding:0}ins,del{text-decoration:none;border:none;outline:none;padding:0 2px}html{font-size:10px;font-size:62.5%;background:#373a3c}body{color:#fff;background:#373a3c;line-height:1.5;font-size:180%;font-family:"Liberation Sans","Noto Sans","Droid Sans","Linux Biolinum","Ubuntu";font-feature-settings:"kern","liga","pnum"}header h1{color:#55595c}header h1 span{color:#fff;font-family:"Ubuntu Monospace","Liberation Mono","Droid Sans Mono"}header h1 span:before{color:#55595c;content:"`"}header h1 span:after{color:#55595c;content:"`"}h1{margin:1.5em 0 0.75em;line-height:1.2;font-weight:600;font-size:175%;color:#fff}p{line-height:1.5;margin:0 0 1.5em}p:last-child{margin-bottom:0}ins{background-color:rgba(92,184,92,0.85)}del{background-color:rgba(217,83,79,0.85);opacity:0.75}#root{max-width:800px;margin:0 auto}#content{margin:0 0 1.5em;padding:0.375em 0.75em;color:#373a3c;background:#f7f7f9;border:1px solid #818a91;border-radius:3px}
"""

JS = ""
