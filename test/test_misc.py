#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append(u'../ftplugin')

import vim

from orgmode import indent_orgmode, fold_orgmode, ORGMODE

ORGMODE.debug = True

START = True
END = False

class MiscTestCase(unittest.TestCase):
	def setUp(self):
		vim.CMDHISTORY = []
		vim.CMDRESULTS = {}
		vim.EVALHISTORY = []
		vim.EVALRESULTS = {
				u'exists("g:org_debug")': 0,
				u'exists("g:org_debug")': 0,
				u'exists("*repeat#set()")': 0,
				u"v:count": 0,
				u'b:changedtick': 0,
				u"v:lnum": 0}
		vim.current.buffer = """
* Überschrift 1
Text 1

Bla bla
** Überschrift 1.1
Text 2

Bla Bla bla
** Überschrift 1.2
Text 3

**** Überschrift 1.2.1.falsch

Bla Bla bla bla
*** Überschrift 1.2.1
* Überschrift 2
* Überschrift 3
  asdf sdf
""".split('\n')

	def test_indent_noheading(self):
		# test first heading
		vim.current.window.cursor = (1, 0)
		vim.EVALRESULTS[u'v:lnum'] = 1
		indent_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 0)

	def test_indent_heading(self):
		# test first heading
		vim.current.window.cursor = (2, 0)
		vim.EVALRESULTS[u'v:lnum'] = 2
		indent_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 0)

	def test_indent_heading_middle(self):
		# test first heading
		vim.current.window.cursor = (3, 0)
		vim.EVALRESULTS[u'v:lnum'] = 3
		indent_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:indent_level = 2')

	def test_indent_heading_middle2(self):
		# test first heading
		vim.current.window.cursor = (4, 0)
		vim.EVALRESULTS[u'v:lnum'] = 4
		indent_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:indent_level = 2')

	def test_indent_heading_end(self):
		# test first heading
		vim.current.window.cursor = (5, 0)
		vim.EVALRESULTS[u'v:lnum'] = 5
		indent_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:indent_level = 2')

	def test_fold_heading_start(self):
		# test first heading
		vim.current.window.cursor = (2, 0)
		vim.EVALRESULTS[u'v:lnum'] = 2
		fold_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:fold_expr = ">1"')

	def test_fold_heading_middle(self):
		# test first heading
		vim.current.window.cursor = (3, 0)
		vim.EVALRESULTS[u'v:lnum'] = 3
		fold_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:fold_expr = 1')

	def test_fold_heading_end(self):
		# test first heading
		vim.current.window.cursor = (5, 0)
		vim.EVALRESULTS[u'v:lnum'] = 5
		fold_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:fold_expr = 1')

	def test_fold_heading_end_of_last_child(self):
		# test first heading
		vim.current.window.cursor = (16, 0)
		vim.EVALRESULTS[u'v:lnum'] = 16
		fold_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		# which is also end of the parent heading <1
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:fold_expr = ">3"')

	def test_fold_heading_end_of_last_child_next_heading(self):
		# test first heading
		vim.current.window.cursor = (17, 0)
		vim.EVALRESULTS[u'v:lnum'] = 17
		fold_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:fold_expr = ">1"')

	def test_fold_middle_subheading(self):
		# test first heading
		vim.current.window.cursor = (13, 0)
		vim.EVALRESULTS[u'v:lnum'] = 13
		fold_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:fold_expr = ">4"')

	def test_fold_middle_subheading2(self):
		# test first heading
		vim.current.window.cursor = (14, 0)
		vim.EVALRESULTS[u'v:lnum'] = 14
		fold_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:fold_expr = 4')

	def test_fold_middle_subheading3(self):
		# test first heading
		vim.current.window.cursor = (15, 0)
		vim.EVALRESULTS[u'v:lnum'] = 15
		fold_orgmode()
		self.assertEqual(len(vim.CMDHISTORY), 1)
		self.assertEqual(vim.CMDHISTORY[-1], 'let b:fold_expr = 4')

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(MiscTestCase)