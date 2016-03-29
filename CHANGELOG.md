# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

__wdiff HTML__ was originally a plain Python module (and before that a Perl
script) created in the early 2000s. Version [0.3.0] was made into a package
and uploaded to Github. This change log starts there.


## [0.5.0] — 2016-03-29

- Added support for files in the __users data directory__ (`~/.local/wdiff` on
  Linux). If this directory contains files named like the defaults
  (`template.jinja`, `styles.css`, `main.js`, `secondary.js`), they replace
  the defaults.

- Added support for additional Javascript. `secondary.js` is loaded before
  `main.js` (e.g. for frameworks like Zepto).

- Added Javasacript to controll buttons that show and hide the changes.

- Added [Invoke] tasks to build Javascript from [CoffeeScript] and CSS
  from [SASS].

- Fixed some spelling errors and _docstrings_ and added more argument
  checking.

### [0.5.1] — 2016-03-29

- Fixed `setup.py`

- Uploaded the package to [PyPI].

### [0.5.2] — 2016-03-29

- Added `--version` argument to the CLI.


## [0.4.0] — 2016-03-27

- Added support to define own files as HTML template, CSS and Javascript
  trough command line arguments.

- New: Use Jinja2 instead of plain string templates.


## [0.3.0] — 2016-03-27

- Moved the module to a package and created a `setup.py` script.



[PyPI]: https://pypi.python.org/

[Invoke]: http://pyinvoke.org
[CoffeeScript]: http://coffeescript.org/
[SASS]: http://sass-lang.com/

[0.3.0]: https://github.com/brutus/wdiffhtml/tree/0.3.0
[0.4.0]: https://github.com/brutus/wdiffhtml/tree/0.4.0
[0.5.0]: https://github.com/brutus/wdiffhtml/tree/0.5.0
