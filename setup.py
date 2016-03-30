#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys

from codecs import open
from setuptools import setup


def get_path(filename):
  """
  Returns the absolute path to *filename* (a directory).

  """
  return os.path.abspath(os.path.dirname(filename))


def get_meta(path=None):
  """
  Returns a tuple of `__version__` and `__doc__` form the modul.

  If *path* is set, it is temporarily added to `sys.path`.

  """
  if path:
    sys.path.insert(1, path)
  from wdiffhtml import __version__, __doc__
  if path:
    del(sys.path[0])
  return __version__, __doc__


def get_short_description(text):
  """
  Returns the first paragraph from *text*.

  """
  return [p.strip() for p in text.strip().split('\n\n')][0]


def get_long_description(filename):
  """
  Returns the contents of *filename* (UTF-8).

  """
  with open(filename, encoding='utf-8') as f:
    return f.read()


VERSION, DOC = get_meta()


setup(
  name='wdiffhtml',
  version=VERSION,
  packages=['wdiffhtml'],
  package_data={
    'wdiffhtml': [
      'data/template.jinja',
      'data/styles.css',
      'data/main.js',
      'data/secondary.js',
    ]
  },
  install_requires=[
    'setuptools',
    'jinja2',
    'appdirs',
  ],
  description=get_short_description(DOC),
  long_description=get_long_description('README.md'),
  keywords='',
  url='https://github.com/brutus/wdiffhtml',
  author='Brutus [DMC]',
  author_email='brutus.dmc@googlemail.com',
  license='GNU GPLv3',
  classifiers=[
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Topic :: Text Processing',
    'Topic :: Utilities',
  ],
  entry_points={
    'console_scripts': [
      'wdiffhtml=wdiffhtml.cli:main',
    ],
  },
)
