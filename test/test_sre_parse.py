#!/usr/bin/env python

import tpg

class P(tpg.Parser):
    r"""
        token x '\w+' ;

        START/t -> '\(' x/t '\)' ;

        BAD_CODE ->
            $ if x:
            $   print x
            $ else:
            $   pass
        ;
    """

p = P()

print p('(toto)')
