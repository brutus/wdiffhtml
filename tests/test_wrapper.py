# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from unittest import TestCase

from wdiffhtml.utils import (
  build_paragraph,
  wrap_paragraphs,
)


class TestWrapParagraph(TestCase):

  def test_para(self):
    content = """
      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veniam soluta
      impedit dolores quae doloribus nesciunt sequi, accusamus eos incidunt
      ducimus, aspernatur nulla ipsam odio. Vitae quas libero inventore
      doloremque explicabo!
    """
    exp = '<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veniam soluta\nimpedit dolores quae doloribus nesciunt sequi, accusamus eos incidunt\nducimus, aspernatur nulla ipsam odio. Vitae quas libero inventore\ndoloremque explicabo!</p>'
    res = build_paragraph(content, hard_breaks=False)
    self.assertEqual(res, exp)

  def test_hard_breaks(self):
    content = """
      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veniam soluta
      impedit dolores quae doloribus nesciunt sequi, accusamus eos incidunt
      ducimus, aspernatur nulla ipsam odio. Vitae quas libero inventore
      doloremque explicabo!
    """
    exp = '<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veniam soluta<br />\nimpedit dolores quae doloribus nesciunt sequi, accusamus eos incidunt<br />\nducimus, aspernatur nulla ipsam odio. Vitae quas libero inventore<br />\ndoloremque explicabo!</p>'
    res = build_paragraph(content, hard_breaks=True)
    self.assertEqual(res, exp)

  def test_multibreaks(self):
    content = """

      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veniam soluta
      impedit dolores quae doloribus nesciunt sequi, accusamus eos incidunt

      ducimus, aspernatur nulla ipsam odio. Vitae quas libero inventore
      doloremque explicabo!

    """
    exp = '<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veniam soluta\nimpedit dolores quae doloribus nesciunt sequi, accusamus eos incidunt\nducimus, aspernatur nulla ipsam odio. Vitae quas libero inventore\ndoloremque explicabo!</p>'
    res = build_paragraph(content, hard_breaks=False)
    self.assertEqual(res, exp)


class TestWrapParagraphs(TestCase):

  def test_paras(self):
    content = """

      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veniam soluta
      impedit dolores quae doloribus nesciunt sequi.

      Accusamus eos incidunt ducimus, aspernatur nulla ipsam odio.

      Vitae quas libero inventore
      doloremque explicabo!

    """
    exp = (
      '<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veniam soluta\nimpedit dolores quae doloribus nesciunt sequi.</p>\n'
      '<p>Accusamus eos incidunt ducimus, aspernatur nulla ipsam odio.</p>\n'
      '<p>Vitae quas libero inventore\ndoloremque explicabo!</p>'
    )
    res = wrap_paragraphs(content, hard_breaks=False)
    self.assertEqual(res, exp)
