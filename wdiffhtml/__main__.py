#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Make the `wdiffhtml` package run-able.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import sys

from .cli import main


if __name__ == '__main__':
  sys.exit(main())
