# -*- coding: UTF-8 -*-

"""
Some taskt to generate CSS and Javascript from the data files.

"""

import os

from functools import wraps
from pathlib import Path

from invoke import (
  Collection,
  task,
  run,
)


DATA_DIR = str(Path(__file__).parent / 'wdiffhtml' / 'data')

CMD_SASS = 'sass --style {style} styles.sass > styles.css'

CMD_COFFEE = 'coffee --compile --bare --map --no-header main.coffee'


def change_dir(directory):
  """
  Wraps a function to run in a given directory.

  """
  def cd_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      org_path = Path.cwd()
      os.chdir(directory)
      return func(*args, **kwargs)
      os.chdir(org_path)
    return wrapper
  return cd_decorator


@task
@change_dir(DATA_DIR)
def build_css(minimize=True):
  """
  Builds CSS from SASS.

  """
  print('Build CSS')
  args = {}
  args['style'] = 'compressed' if minimize else 'nested'
  cmd = CMD_SASS.format(**args)
  run(cmd)


@task
@change_dir(DATA_DIR)
def build_js():
  """
  Builds Javascript from CoffeeScript.

  """
  print('Build Javascript')
  args = {}
  cmd = CMD_COFFEE.format(**args)
  run(cmd)


@task(build_css, build_js)
def build_all():
  """
  Runs all build tasks.

  """
  pass


ns_build = Collection('build')
ns_build.add_task(build_all, name='all', default=True)
ns_build.add_task(build_css, name='css')
ns_build.add_task(build_js, name='js')

ns = Collection()
ns.add_collection(ns_build)
