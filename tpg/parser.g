
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
			|	RULE/c p-c
			)*
			parsers-p
		|	'main' ':' ( code/c parsers-Code<c> )*
		)*
		;

	OPTIONS/opts ->
		opts = Options<>
		(	'set' ident/opt ( '=' string/val | val = 1 )
			{{ if opt.startswith('no'): opt, val = opt[2:], None }}
			check {{opt in [ 'magic' ]}}
			{{ opts.set(opt,val) }}
		)*
		;

	TOKEN/Token<t,e,f,s> ->
		(	'token' s = 0
		|	'separator' s = 1
		)
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
		;

	AST_OP/op ->
		OBJECT/o1
		(	'=' OBJECT/o2 op = MakeAST<o1,o2>
		|	'-' OBJECT/o2 op = AddAST<o1,o2>
		)
		;

	MARK_OP/op -> '!' OBJECT/o op = Mark<o> ;

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
		|	obra NB<0>/m ( ',' NB<None>/M | M=m ) cbra	a = Rep<self,m,M,a>
		)?
		;

	NB<n>/n -> ( ident/n n=eval<n> )? ;

	INLINE_TOKEN/InlineToken<expr, ret> ->
		string/expr
		( '/' OBJECT/ret | ret = None )
		;

main:

{{

_TPGParser = TPGParser()

def compile(grammar):
	""" Translate a grammar into Python """
	return _TPGParser(grammar)

}}
