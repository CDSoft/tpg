"""
Toy Parser Generator - A Python parser generator

Toy Parser Generator is a lexical and syntactic parser generator
for Python. This generator was born from a simple statement: YACC
is to complex to use in simple cases (calculators, configuration
files, small programming languages, ...).

TPG can very simply write parsers that are usefull for most every
day needs (even if it can't make your coffee). With a very clear
and simple syntax, you can write an attributed grammar that is
translated into a recursive descendant parser. TPG generated code
is very closed to the original grammar. This means that the parser
works "like" the grammar. A grammar rule can be seen as a method
of the parser class, symbols as method calls, attributes as method
parameters and semantic values as return values. You can also add
Python code directly into grammar rules and build abstract syntax
trees while parsing.

The first application of TPG is TPG itself. The first (not released)
version of TPG has been written by hand then was used to generate
next versions. Now TPG can generate itself.

Note: Python 2.2 or newer is required!

All you need to use TPG is to import tpg
and use these three objects:

tpg.compile(grammar):
	This function takes a grammar in a string and produces
	a parser in Python (also in a string).
	You can use exec to actually build it.

tpg.LexicalError:
	This exception is raised when the lexer fails

tpg.SyntaxError:
	This exception


For further information about TPG, please visit
http://christophe.delord.free.fr
or contact the author at
mailto:christophe.delord@free.fr

Feel free to contact the author for any request.

Happy TPG'ing

Christophe Delord.
"""

# Release data

import Release
__version__ = Release.version
__date__    = Release.date
__author__  = "%s <%s>"%(Release.author, Release.email)
__url__     = Release.url
__licence__ = Release.license

# Modules
#
#	base.py   : basic parser and lexer
#	parser.py : TPG grammar parser (generated from parser.g)
#	codegen.py: python code generator
#	Release.py: release data

from parser import compile
from base import LexicalError, SyntaxError
