{{

"""
Toy Parser Generator: A Python parser generator
Copyright (C) 2002 Christophe Delord
 
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

For further information about TPG you can visit
http://christophe.delord.free.fr/en/tpg
"""

from codegen import *

cut = lambda n: lambda s,n=n:s[n:-n]

def cutstr(st):
    if st[0]=="'": st = st.replace('"', r'\"')
    return st[1:-1]

}}

parser TPGParser:

    separator space: "\s+|#.*";

    token string: "\"(\\.|[^\"\\]+)*\"|'(\\.|[^'\\]+)*'" cutstr;
    token code: "\{\{(\}?[^\}]+)*\}\}" cut<2>;
    token obra: "\{";
    token cbra: "\}";
    token retsplit: "//";
    token ret: "/";
    token star2: "\*\*";
    token star: "\*";
    token ident: "\w+";

    kw<name> -> ident/i check {{ i==name }};

    START/parsers.genCode<> -> PARSERS/parsers ;

    PARSERS/parsers ->
        GLOBAL_OPTIONS/opts
        parsers = Parsers<opts>
        ( code/c parsers-Code<c> )*
        (   'parser' ! ident/id ! ( '\(' ! ARGS/ids '\)' | ids = Args<> ) ':' !
            LOCAL_OPTIONS/opts
            p = Parser<id, ids, opts>
            self.current_parser = p
            (   code/c p-Code<c>
            |   TOKEN/t p-t
            |   RULE/r p-r
            |   LEX_RULE/r p-r
            )*
            parsers-p
        |   'main' ':' ! ( code/c parsers-Code<c> )*
        )*
        ;

    GLOBAL_OPTIONS/opts ->
        opts = Options<>
        (   'set' !
            (   kw<'magic'> ! '=' string/val        {{ opts.set('magic', val) }}
            )
        )*
        ;

    LOCAL_OPTIONS/opts ->
        opts = Options<>
        (   'set' !
            (   kw<'CSL'> !                         {{ opts.set('CSL', 1) }}
            |   kw<'indent'> ! '='
                    string/tabs                     {{ opts.set('indent', tabs) }}
                    ( ',' string/regexp             {{ opts.set('noindent', regexp) }}
                    )?
            )
        )*
        ;

    CHECK_CSL<obj> -> check {{ self.current_parser.opts['CSL'] }} | error {{ "%s: Only for CSL lexers"%obj }} ;

    CHECK_NOT_CSL<obj> -> check {{ not self.current_parser.opts['CSL'] }} | error {{ "%s: Only for non CSL lexers"%obj }} ;

    TOKEN/Token<t,e,f,s> ->
        (   'token' s = 0
        |   'separator' s = 1
        ) !
        CHECK_NOT_CSL<'Predefined token'>
        ident/t ':' ! string/e ( OBJECT/f | f = None )
        ';'
        ;

    ARGS/args ->
        args = Args<>
        (   ARG/arg args-arg
            ( ',' ARG/arg args-arg )*
        )?
        ;

    ARG/arg ->
            "\*\*" ! OBJECT/kw arg = ArgDict<kw>
        |   "\*" ! OBJECT/args arg = ArgList<args>
        |   ident/name "=" ! OBJECT/value arg = KeyWordArg<name,value>
        |   OBJECT/arg
        ;

    OBJECT/o ->
            ident/o SOBJECT<Object<o>>/o
        |   string/o SOBJECT<String<o>>/o
        |   '<' OBJECTS/o '>'
        |   code/c check {{c.count('\n')==0}} o = Code<c>
        ;

    SOBJECT<o>/o ->
        (   '\.\.' OBJECT/o2 o=Extraction<o,o2>
        |   '\.' ident/o2 SOBJECT<Composition<o,Object<o2>>>/o
        |   '<' ARGS/as '>' SOBJECT<Application<o,as>>/o
        |   '\[' INDICE/i '\]' SOBJECT<Indexation<o,i>>/o
        |   #
        )
        ;

    OBJECTS/objs ->
        objs = Objects<>
        (   OBJECT/obj objs-obj
            ( ',' OBJECT/obj objs-obj )*
        )?
        ;

    INDICE/i ->
        ( OBJECT/i | i=None )
        ( ':' ( OBJECT/i2 | i2=None) i=Slice<i,i2> )?
        (   check {{i is not None}}
        |   error "Empty index or slice"
        )
        ;

    RULE/Rule<s,e> -> SYMBOL/s '->' ! EXPR/e ';' ;

    LEX_RULE/LexRule<s,e> ->
        'lex' !
        CHECK_CSL<'Lexical rule'>
        (   'separator'/name s=Symbol<name, Args<>, None>
        |   SYMBOL/s
        )
        '->' ! EXPR/e ';'
        ;

    SYMBOL/Symbol<id,as,ret> ->
        ident/id
        ( '<' ARGS/as '>' | as = Args<> )
        (   '/' OBJECT/ret
        |   ret = None
        )
        ;

    EXPR/balance<e> -> CUT_TERM/e ( '\|' ! CUT_TERM/t e = Alternative<e,t> )* ;

    CUT_TERM/e ->
        TERM/e
        (   '!' ! TERM/ce c=Cut<> c-ce
            (   '!' ! TERM/ce c-ce
            )*
            e = Sequence<e,c>
        )?
        ;

    TERM/t -> t = Sequence<> ( FACT/f t-f )* ;

    FACT/f ->
            AST_OP/f
        |   MARK_OP/f
        |   code/c f=Code<c>
        |   ATOM/f ! REP<f>/f
        |   'check' ! OBJECT/cond f=Check<cond>
        |   'error' ! OBJECT/err f=Error<err>
        ;

    AST_OP/op<o1,o2> ->
        OBJECT/o1
        (   '=' op=MakeAST
        |   '-' op=AddAST
        ) !
        OBJECT/o2
        ;

    MARK_OP/Mark<o> -> '@' ! OBJECT/o ;

    ATOM/a ->
        (   SYMBOL/a
        |   INLINE_TOKEN/a
        |   '\(' ! EXPR/a '\)'
        )
        ;

    REP<a>/a ->
        (   (   '\?' ! {{ m, M = 0, 1 }}
            |   '\*' ! {{ m, M = 0, None }}
            |   '\+' ! {{ m, M = 1, None }}
            |   '\{' ! NB<0>/m ( ',' ! NB<None>/M | M=m ) '\}'
            )
            {{
                if M is not None:
                    if m>M: self.error("Invalid repetition")
                elif a.empty():
                    self.error("Infinite repetition of an empty expression")
            }}
            a = Rep<m,M,a>
        )?
        ;

    NB<n>/n -> ident/n ? ;

    INLINE_TOKEN/InlineToken<expr, ret, split> ->
        string/expr
        (   '/' ! OBJECT/ret                                split = None
        |   '//' ! CHECK_CSL<'Split return'>    OBJECT/ret  split = 1
        |   ret = None                                      split = None
        )
        ;

main:

{{

_TPGParser = TPGParser()

def _compile(grammar):
    source = _TPGParser(grammar)
    code = __builtins__['compile'](source, "", 'exec')
    return source, code

def translate(grammar):
    """ Translate a grammar into Python """
    return _compile(grammar)[0]

def compile(grammar):
    """ Compile a grammer into a Python code object """
    return _compile(grammar)[1]

}}
