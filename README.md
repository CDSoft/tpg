Abstract
========

> Toy Parser Generator is a lexical and syntactic parser generator for Python. This generator was born from a simple statement: YACC is too complex to use in simple cases (calculators, configuration files, small programming languages, ...).
>
> TPG can very simply write parsers that are useful for most every day needs (even if it can't make your coffee). With a very clear and simple syntax, you can write an attributed grammar that is translated into a recursive descendant parser. TPG generated code is very closed to the original grammar. This means that the parser works *like* the grammar. A grammar rule can be seen as a method of the parser class, symbols as method calls, attributes as method parameters and semantic values as return values. You can also add Python code directly into grammar rules and build abstract syntax trees while parsing.
>
> The first application of TPG is TPG itself. The first (not released) version of TPG has been written by hand then was used to generate next versions. Now TPG can generate itself.
>
> For an up-to-date documentation, please read [tpg.pdf](doc/tpg.pdf).
>
> Please let me know if you use TPG in one of your projects. I will add you in the list of projects using TPG.

Contact
=======

The author can be contacted on GitHub as well as at <http://cdelord.fr/tpg>.

Prerequisites
=============

[Python 2.2](http://www.python.org/) or newer is required. TPG works with both Python 2 and 3.

How it works
============

Lexical scanner
---------------

The lexical scanner uses Python regular expressions. The text is split before being parsed by the grammar rules.

Syntactic parser
----------------

TPG isn't based on predictive algorithms with tables like LL(k). The main idea was instead to try every possible choices and to accept the first choice that match the input. So when a choice point is reached - say `A|B|C` - the parser will first try to recognize `A`. If this fails it will try `B` and if necessary `C`. So contrary to LL(k) parsers the order of the branches of choice points is very important for TPG. In fact this method has been inspired from Prolog DGC parsers. But remember that when a choice has been done, even if their are more possible choices, it can't be undone (in Prolog it can). The text to be parsed has to be stored in a string in memory (backtracking is simpler this way). During the parsing, the current position is stored in internal TPG variables for all terminal and non-terminal symbols.

So we can say that TPG uses a sort of very limited backtracking.

This algorithm is easily implementable. Any rule is translated into a class method without having to compute a prediction table. The main drawbacks of this method is that you have to be careful when you write your grammar (as in Prolog).

Example
=======

This page presents a well known example: a calculator.

More detailed examples are given in the [documentation of TPG](doc/tpg.pdf).

``` python
#!/usr/bin/env python

import math
import operator
import string
import tpg

if tpg.__python__ == 3:
    operator.div = operator.truediv
    raw_input = input

def make_op(op):
    return {
        '+'   : operator.add,
        '-'   : operator.sub,
        '*'   : operator.mul,
        '/'   : operator.div,
        '%'   : operator.mod,
        '^'   : lambda x,y:x**y,
        '**'  : lambda x,y:x**y,
        'cos' : math.cos,
        'sin' : math.sin,
        'tan' : math.tan,
        'acos': math.acos,
        'asin': math.asin,
        'atan': math.atan,
        'sqr' : lambda x:x*x,
        'sqrt': math.sqrt,
        'abs' : abs,
        'norm': lambda x,y:math.sqrt(x*x+y*y),
    }[op]

class Calc(tpg.Parser, dict):
    r"""
        separator space '\s+' ;

        token pow_op    '\^|\*\*'                                               $ make_op
        token add_op    '[+-]'                                                  $ make_op
        token mul_op    '[*/%]'                                                 $ make_op
        token funct1    '(cos|sin|tan|acos|asin|atan|sqr|sqrt|abs)\b'           $ make_op
        token funct2    '(norm)\b'                                              $ make_op
        token real      '(\d+\.\d*|\d*\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+'    $ float
        token integer   '\d+'                                                   $ int
        token VarId     '[a-zA-Z_]\w*'                                          ;

        START/e ->
                'vars'                  $ e=self.mem()
            |   VarId/v '=' Expr/e      $ self[v]=e
            |   Expr/e
        ;

        Var/$self.get(v,0)$ -> VarId/v ;

        Expr/e -> Term/e ( add_op/op Term/t     $ e=op(e,t)
                         )*
        ;

        Term/t -> Fact/t ( mul_op/op Fact/f     $ t=op(t,f)
                         )*
        ;

        Fact/f ->
                add_op/op Fact/f                $ f=op(0,f)
            |   Pow/f
        ;

        Pow/f -> Atom/f ( pow_op/op Fact/e      $ f=op(f,e)
                        )?
        ;

        Atom/a ->
                real/a
            |   integer/a
            |   Function/a
            |   Var/a
            |   '\(' Expr/a '\)'
        ;

        Function/y ->
                funct1/f '\(' Expr/x '\)'               $ y = f(x)
            |   funct2/f '\(' Expr/x1 ',' Expr/x2 '\)'  $ y = f(x1,x2)
        ;

    """

    def mem(self):
        vars = sorted(self.items())
        memory = [ "%s = %s"%(var, val) for (var, val) in vars ]
        return "\n\t" + "\n\t".join(memory)

print("Calc (TPG example)")
calc = Calc()
while 1:
    l = raw_input("\n:")
    if l:
        try:
            print(calc(l))
        except Exception:
            print(tpg.exc())
    else:
        break
```

Documentation
=============

The documentation is available online in [PDF](doc/tpg.pdf) format.

Installation
============

Linux / Unix / Sources
----------------------

Extract and run `python setup.py install`.

Windows
-------

The Windows installer is not available anymore because of a virus infection. I will now only distribute source packages.

Projects using TPG
==================

[TPG](http://cdelord.fr/index.html)  
Toy Parser Generator (itself ;-)

[Tentakel](http://tentakel.biskalar.de/)  
distributed command execution

[Xoot](http://xoot.org/)  
shorthand to XSLT

[EZgnupy](http://cyrille.boullier.free.fr/python/projects/ezgnupy/index.php)  
a front-end for gnuplot written in python

[Ize](http://maxrepo.info/taxonomy/term/3,6/all)  
python module providing a set of function decorators

[Rugg](http://rugg.sf.net/)  
Flexible file system and hard drive crash testing

[Osh](http://geophile.com/osh/)  
An Open-Source Python-Based Object-Oriented Shell

Links
=====

-   [Python](http://www.python.org/)
-   [Parser-SIG](http://www.python.org/sigs/parser-sig/)
-   See also [Simple Parser](http://github.com/CDSoft/sp)

