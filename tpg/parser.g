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

}}

parser TPGParser:

	separator space: "\s+|#.*";

	token string: "\"(\\.|[^\"\\]+)*\"|'(\\.|[^'\\]+)*'" cut<1>;
	token code: "\{\{(\}?[^\}]+)*\}\}" cut<2>;
	token obra: "\{";
	token cbra: "\}";
	token retsplit: "//";
	token ret: "/";
	token ident: "\w+";

	START/parsers.genCode<> -> PARSERS/parsers ;

	PARSERS/parsers ->
		OPTIONS/opts
		parsers = Parsers<opts>
		( code/c parsers-Code<c> )*
		(	'parser' ident/id ( '\(' ARGS/ids '\)' | ids = Args<> ) ':'
			p = Parser<id, ids>
			(	code/c p-Code<c>
			|	TOKEN/t p-t
			|	RULE/r p-r
			|	LEX_RULE/r p-r
			)*
			parsers-p
		|	'main' ':' ( code/c parsers-Code<c> )*
		)*
		;

	OPTIONS/opts ->
		opts = Options<>
		self.CSL = 0
		(	'set' ident/opt ( '=' string/val | val = 1 )
			{{ if opt.startswith('no'): opt, val = opt[2:], None }}
			check {{opt in [ 'magic', 'CSL' ]}}
			{{ opts.set(opt,val) }}
			{{ if opt == 'CSL': self.CSL = val }}
		)*
		;

	CHECK_CSL -> check {{ self.CSL }} | error "Only for CSL lexers" ;

	CHECK_NOT_CSL -> check {{ not self.CSL }} | error "Only for non CSL lexers" ;

	TOKEN/Token<t,e,f,s> ->
		(	'token' s = 0
		|	'separator' s = 1
		)
		CHECK_NOT_CSL
		ident/t ':' string/e ( OBJECT/f | f = None )
		';'
		;

	ARGS/objs ->
		objs = Args<>
		(	OBJECT/obj objs-obj
			( ',' OBJECT/obj objs-obj )*
		)?
		;

	OBJECT/o ->
			ident/o SOBJECT<Object<o>>/o
		|	string/o SOBJECT<String<o>>/o
		|	'<' OBJECTS/o '>'
		|	code/c check {{c.count('\n')==0}} o = Code<c>
		;

	SOBJECT<o>/o ->
		(	'\.\.' OBJECT/o2 o=Extraction<o,o2>
		|	'\.' ident/o2 SOBJECT<Composition<o,Object<o2>>>/o
		|	'<' ARGS/as '>' SOBJECT<Application<o,as>>/o
		|	'\[' INDICE/i '\]' SOBJECT<Indexation<o,i>>/o
		|	#
		)
		;

	OBJECTS/objs ->
		objs = Objects<>
		(	OBJECT/obj objs-obj
			( ',' OBJECT/obj objs-obj )*
		)?
		;

	INDICE/i ->
		( OBJECT/i | i=None )
		( ':' ( OBJECT/i2 | i2=None) i=Slice<i,i2> )?
		check {{i is not None}}
		;

	RULE/Rule<s,e> -> SYMBOL/s '->' EXPR/e ';' ;

	LEX_RULE/LexRule<s,e> ->
		'lex'
		CHECK_CSL
		(	'separator'/name s=Symbol<name, Args<>, None>
		|	SYMBOL/s
		)
		'->' EXPR/e ';'
		;

	SYMBOL/Symbol<id,as,ret> ->
		ident/id
		( '<' ARGS/as '>' | as = Args<> )
		(	'/' OBJECT/ret
		|	ret = None
		)
		;

	EXPR/e -> TERM/e ( '\|' TERM/t e = Alternative<e,t> )* ;

	TERM/t -> t = Sequence<> ( FACT/f t-f )* ;

	FACT/f ->
			AST_OP/f
		|	MARK_OP/f
		|	code/c f=Code<c>
		|	ATOM/f REP<f>/f
		|	'check' OBJECT/cond f=Check<cond>
		|	'error' OBJECT/err f=Error<err>
		;

	AST_OP/op<o1,o2> ->
		OBJECT/o1
		(	'=' op=MakeAST
		|	'-' op=AddAST
		)
		OBJECT/o2
		;

	MARK_OP/Mark<o> -> '!' OBJECT/o ;

	ATOM/a ->
		(	SYMBOL/a
		|	INLINE_TOKEN/a
		|	'\(' EXPR/a '\)'
		)
		;

	REP<a>/a ->
		(	'\?'										a = Rep<self,0,1,a>
		|	'\*'										a = Rep<self,0,None,a>
		|	'\+'										a = Rep<self,1,None,a>
		|	'\{' NB<0>/m ( ',' NB<None>/M | M=m ) '\}'	a = Rep<self,m,M,a>
		)?
		;

	NB<n>/n -> ident/n ? ;

	INLINE_TOKEN/InlineToken<expr, ret, split> ->
		string/expr
		(	'/' OBJECT/ret				split = None
		|	'//' CHECK_CSL OBJECT/ret	split = 1
		| 	ret = None					split = None
		)
		;

main:

{{

_TPGParser = TPGParser()

def compile(grammar):
	""" Translate a grammar into Python """
	return _TPGParser(grammar)

}}
