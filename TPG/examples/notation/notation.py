#!/usr/bin/python

# conversion d'expressions infixes/préfixes/postfixes

from TPG import *

exprs = """ # Grammaire des expressions arithmétiques

parser Expression:

START/<e,t> ->
	EXPR_INFIXE/e	{{ t='infixe' }}
|	EXPR_PREFIXE/e	{{ t='prefixe' }}
|	EXPR_POSTFIXE/e	{{ t='postfixe' }}
|	e=None			{{ t='inconnue' }}
.

EXPR_INFIXE/e -> EXPR/e '$' .
EXPR_PREFIXE/e -> EXPR_PRE/e '$' .
EXPR_POSTFIXE/e -> EXPR_POST/e '$' .

lex skip -> '\s+' .

# Expressions infixes

EXPR/e -> TERM/e ( ( '\+'/op | '\-'/op ) TERM/t e=Op<op,1,e,t> )* .
TERM/t -> FACT/t ( ( '\*'/op | '\/'/op ) FACT/f t=Op<op,2,t,f> )* .
FACT/f -> ( '\~'/op | '\#'/op ) FACT/e f=Op<op,3,e> | POW/f .

POW/f -> ATOM/f ( '\^'/op FACT/e f=Op<op,4,f,e> )? .

ATOM/a -> '\w+'/s a=Atom<s> | '\(' EXPR/a '\)' .

# Expressions préfixes

EXPR_PRE/e ->
	'\w+'/s e=Atom<s>
|	'\(' EXPR_PRE/e '\)'
|	OP1/<op,prec> EXPR_PRE/a e=Op<op,prec,a>
|	OP2/<op,prec> EXPR_PRE/a EXPR_PRE/b e=Op<op,prec,a,b>
.

# Expressions postfixes

EXPR_POST/e -> ATOM_POST/a SEXPR_POST<a>/e .

ATOM_POST/a ->
	'\w+'/s a=Atom<s>
|	'\(' EXPR_POST/a '\)'
.

SEXPR_POST<e>/e ->
	OP1/<op,prec> SEXPR_POST<Op<op,prec,e>>/e
|	EXPR_POST/e2 OP2/<op,prec> SEXPR_POST<Op<op,prec,e,e2>>/e
|	.

OP2/<op,prec> ->
	'\+'/op prec=1
|	'\-'/op prec=1
|	'\*'/op prec=2
|	'\/'/op prec=2
|	'\^'/op prec=4
.

OP1/<op,prec> ->
	'\#'/op prec=3
|	'\~'/op prec=3
.

"""

class Op(Node):
	def init(self, op, prec, *args):
		self.op = op
		self.prec = prec
		self.ops = args
		self.arity = len(self.ops)
	def infixe(self):
		if self.arity == 1:
			a = self.ops[0].infixe()
			if self.ops[0].prec < self.prec: a = "(%s)"%a
			return "%s %s"%(self.op,a)
		if self.arity == 2:
			a = self.ops[0].infixe()
			if self.ops[0].prec < self.prec or self.op=="^" and self.ops[0].prec <= self.prec : a = "(%s)"%a
			b = self.ops[1].infixe()
			if self.ops[1].prec <= self.prec: b = "(%s)"%b
			return "%s %s %s"%(a,self.op,b)
		return "???"
	def prefixe(self):
		if self.arity == 1:
			a = self.ops[0].prefixe()
			return "%s %s"%(self.op,a)
		if self.arity == 2:
			a = self.ops[0].prefixe()
			b = self.ops[1].prefixe()
			return "%s %s %s"%(self.op,a,b)
		return "???"
	def postfixe(self):
		if self.arity == 1:
			a = self.ops[0].postfixe()
			return "%s %s"%(a,self.op)
		if self.arity == 2:
			a = self.ops[0].postfixe()
			b = self.ops[1].postfixe()
			return "%s %s %s"%(a,b,self.op)
		return "???"

class Atom(Node):
	def init(self, s):
		self.a = s
		self.prec = 99
	def infixe(self): return self.a
	def prefixe(self): return self.a
	def postfixe(self): return self.a

if __name__ == "__main__":

	exec(TPParser()(exprs))
	parser = Expression()
	while 1:
		e = raw_input(":")
		if e == "": break
		expr, t = parser(e)
		print "Expression", t
		if expr is not None:
			print "\tinfixe   :", expr.infixe()
			print "\tprefixe  :", expr.prefixe()
			print "\tpostfixe :", expr.postfixe()
