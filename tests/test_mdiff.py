# -*- coding: UTF-8 -*-

from unittest import TestCase
from collections import namedtuple

from testfixtures import TempDirectory

from wdiffhtml.utils import generate_wdiff


Case = namedtuple('Case', 'org, new, exp, exp_folded exp_nohtml')


class TestWdiff(TestCase):

  CASES = (
    Case(
      'Just ä test.',
      'Just änöther test.',
      'Just <del>ä</del> <ins>änöther</ins> test.',
      'Just <del>ä</del> <ins>änöther</ins> test.',
      'Just [-ä-] {+änöther+} test.',
    ),
    Case(
      'Just a test\nover more lines.',
      'Just another test\nover lines and stuff.',
      'Just <del>a</del> <ins>another</ins> test\nover <del>more lines.</del> <ins>lines and stuff.</ins>',
      'Just <del>a</del> <ins>another</ins> test\nover <del>more lines.</del> <ins>lines and stuff.</ins>',
      'Just [-a-] {+another+} test\nover [-more lines.-] {+lines and stuff.+}',
    ),
    Case(
      'A test sentence with multiple lines\nand stuff.',
      'A test sentence with changes\nover multiple lines\nand stuff.',
      'A test sentence with <ins>changes</ins>\n<ins>over</ins> multiple lines\nand stuff.',
      'A test sentence with <ins>changes\nover</ins> multiple lines\nand stuff.',
      'A test sentence with {+changes+}\n{+over+} multiple lines\nand stuff.',
    ),
  )

  def test_plain(self):
    for case in self.CASES:
      with TempDirectory() as tempd:
        org_file = tempd.write('org', case.org.encode())
        new_file = tempd.write('new', case.new.encode())
        res = generate_wdiff(
          org_file, new_file, fold_tags=False, html=True
        )
        self.assertEqual(res, case.exp)

  def test_nofolded(self):
    for case in self.CASES:
      with TempDirectory() as tempd:
        org_file = tempd.write('org', case.org.encode())
        new_file = tempd.write('new', case.new.encode())
        res = generate_wdiff(
          org_file, new_file, fold_tags=True, html=True
        )
        self.assertEqual(res, case.exp_folded)

  def test_nohtml(self):
    for case in self.CASES:
      with TempDirectory() as tempd:
        org_file = tempd.write('org', case.org.encode())
        new_file = tempd.write('new', case.new.encode())
        res = generate_wdiff(
          org_file, new_file, fold_tags=False, html=False
        )
        self.assertEqual(res, case.exp_nohtml)
