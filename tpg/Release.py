""" Release data for Toy Parser Generator """

name = 'TPG'

version = '2.1.4'

date = '2002-10-20'

description = "A Python parser generator"

long_description = """\
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
"""

license = 'LGPL'

author = 'Christophe Delord'

email = 'christophe.delord@free.fr'

url = 'http://christophe.delord.free.fr/en/tpg/'

platforms = [ 'Linux', 'Unix', 'Mac OSX', 'Windows XP/2000/NT', 'Windows 95/98/ME' ]

keywords = [ 'Parsing', 'Parser', 'Generator', 'Python' ]

