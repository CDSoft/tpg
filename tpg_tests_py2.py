#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import unittest

import tpg

print("*"*70)
print("*")
print("* Unit tests for %(__name__)s %(__version__)s (%(__date__)s)"%tpg.__dict__)
print("*")
print("* Platform : %s"%sys.platform.replace('\n', ' '))
print("* Version  : %s"%sys.version.replace('\n', ' '))
print("*")
print("* Please report bug to %(__author__)s (%(__email__)s)"%tpg.__dict__)
print("* for further detail read %(__url__)s"%tpg.__dict__)
print("*")
print("*"*70)

for PARSER, VERBOSE in ( (tpg.Parser, None),
                         (tpg.VerboseParser, 0),
                         (tpg.VerboseParser, 1),
                         (tpg.VerboseParser, 2),
                       ):
    for LEXER in tpg.TPGParser.Options.option_dict['lexer'][0]:

        print("*"*70)
        if VERBOSE is None:
            print("* %s %s"%(PARSER.__name__, LEXER))
        else:
            print("* %s verbose=%s %s"%(PARSER.__name__, VERBOSE, LEXER))
        print("*"*70)

        class UnicodeTestCase(unittest.TestCase):

            class Parser(PARSER):
                __doc__ = ur"""
                    set lexer = %(LEXER)s
                    set lexer_unicode = True

                    token single_quote '[‘’]' ;
                    token double_quote '["“”]' ;
                    token word '\w+' ;

                    START/x -> double_quote word/x double_quote
                             | single_quote word/x single_quote
                             | '`' word/x '´'
                             ;
                """%tpg.Py()

            def testExpr(self):
                p = self.Parser()
                self.assertEquals(p(u'"woah"'), "woah")
                self.assertEquals(p(u"“woah”"), "woah")
                self.assertEquals(p(u"‘woah’"), "woah")
                self.assertEquals(p(u"`woah´"), "woah")

        try:
            unittest.main()
        except SystemExit:
            if tpg.exc().args[0]:
                raise

