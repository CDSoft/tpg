set magic=/usr/bin/python
set runtime

{{

from string import atoi, atof, atol
from math import sqrt, cos, sin, tan, acos, asin, atan

sqr = lambda x: x*x

}}

parser Calc:

{{
	def init(self):
		self.vars = {}
	def getVar(self, v):
		try:
			return self.vars[v]
		except KeyError:
			return 0
	def setVar(self, v, e):
		self.vars[v] = e
	def mem(self):
		vars = self.vars.items()
		vars.sort()
		return "\n\t" + "\n\t".join( [ "%s = %s"%(var,val) for (var,val) in vars ] )
}}

START/e ->
	'vars' '$' {{ e=self.mem() }}
|	VarId/v '=' Expr/e '$' {{ self.setVar(v,e) }} '$'
|	Expr/e '$'
.

lex skip -> '\s|\n' .

VarId/v -> '[a-zA-Z]\w*'/v .
Var/v -> VarId/v {{ v=self.getVar(v) }} .

Expr/e ->
	Term/e
	(	'\+' Term/t {{ e += t }}
	|	'\-' Term/t {{ e -= t }}
	)*
	.

Term/t ->
	Fact/t
	(	'\*' Fact/f {{ t *= f }}
	|	'\/' Fact/f {{ t /= f }}
	|	'\%' Fact/f {{ t %= f }}
	)*
	.

Fact/a ->
	'\-' '\-' Fact/a
|	'\-' Fact/a {{ a = -a }}
|	'\+' Fact/a
|	Pow/a
.

Pow/f -> Atom/f ( ('\^'|'\*\*') Fact/e {{ f **= e }} )* .

Atom/a ->
	'(\d+\.\d*|\d*\.\d+)([eE][-+]?\d+)?'/f  {{ a = atof(f) }}
|	'\d+[eE][-+]?\d+'/f {{ a = atof(f) }}
|	'\d+'/i {{ a = atol(i) }}
|	Function/a
|	Var/a
|	'\(' Expr/a '\)'
.

Function/f ->
	'cos' '\(' Expr/e '\)' {{ f = cos(e) }}
|	'sin' '\(' Expr/e '\)' {{ f = sin(e) }}
|	'tan' '\(' Expr/e '\)' {{ f = tan(e) }}
|	'acos' '\(' Expr/e '\)' {{ f = acos(e) }}
|	'asin' '\(' Expr/e '\)' {{ f = asin(e) }}
|	'atan' '\(' Expr/e '\)' {{ f = atan(e) }}
|	'sqr' '\(' Expr/e '\)' {{ f = sqr(e) }}
|	'sqrt' '\(' Expr/e '\)' {{ f = sqrt(e) }}
|	( 'abs' '\(' Expr/e '\)' | '\|' Expr/e '\|' ) {{ f = abs(e) }}
|	'norm' '\(' Expr/x ',' Expr/y '\)' {{ f = sqrt(x*x+y*y) }}
.

main:

{{
	calc = Calc()
	while 1:
		l = raw_input("\n:")
		if l:
			try:
				print calc(l)
			except calc.tpg_Error:
				print "erreur de syntaxe\n"
			except ZeroDivisionError:
				print "Division par zéro\n"
			except OverflowError:
				print "Résultat trop grand\n"
		else:
			break
}}
