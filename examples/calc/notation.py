#!/usr/bin/env python

# Infix/prefix/postfix expression conversion

import tpg

class Op:
	""" Binary operator """
	def __init__(self, op, a, b, prec):
		self.op = op			# operator ("+", "-", "*", "/", "^")
		self.prec = prec		# precedence of the operator
		self.a, self.b = a, b	# operands
	def infix(self):
		a = self.a.infix()
		if self.a.prec < self.prec: a = "(%s)"%a
		b = self.b.infix()
		if self.b.prec <= self.prec: b = "(%s)"%b
		return "%s %s %s"%(a, self.op, b)
	def prefix(self):
		a = self.a.prefix()
		b = self.b.prefix()
		return "%s %s %s"%(self.op, a, b)
	def postfix(self):
		a = self.a.postfix()
		b = self.b.postfix()
		return "%s %s %s"%(a, b, self.op)

class Atom:
	""" Atomic expression """
	def __init__(self, s):
		self.a = s
		self.prec = 99
	def infix(self): return self.a
	def prefix(self): return self.a
	def postfix(self): return self.a

exec(tpg.compile(r"""

# Grammar for arithmetic expressions

parser ExpressionParser:

separator space: '\s+';
token ident: '\w+';

START/<e,t> ->
	EXPR/e		t='infix'		'\n'
|	EXPR_PRE/e	t='prefix'		'\n'
|	EXPR_POST/e	t='postfix'		'\n'
;

# Infix expressions

EXPR/e -> TERM/e ( '[+-]'/op TERM/t e=Op<op,e,t,1> )* ;
TERM/t -> FACT/t ( '[*/]'/op FACT/f t=Op<op,t,f,2> )* ;
FACT/f -> ATOM/f ( '\^'/op FACT/e f=Op<op,f,e,3> )? ;

ATOM/a -> ident/s a=Atom<s> | '\(' EXPR/a '\)' ;

# Prefix expressions

EXPR_PRE/e ->
	ident/s e=Atom<s>
|	'\(' EXPR_PRE/e '\)'
|	OP/<op,prec> EXPR_PRE/a EXPR_PRE/b e=Op<op,a,b,prec>
;

# Postfix expressions

EXPR_POST/e -> ATOM_POST/a SEXPR_POST<a>/e ;

ATOM_POST/a ->
	ident/s a=Atom<s>
|	'\(' EXPR_POST/a '\)'
;

SEXPR_POST<e>/e ->
	EXPR_POST/e2 OP/<op,prec> SEXPR_POST<Op<op,e,e2,prec>>/e
|	;

OP/<op,prec> ->
	'[+-]'/op prec=1
|	'[*/]'/op prec=2
|	'\^'/op   prec=3
;

"""))

parser = ExpressionParser()
while 1:
	e = raw_input(":")
	if e == "": break
	try:
		expr, t = parser(e+"\n")
	except (tpg.LexicalError, tpg.SyntaxError), e:
		print e
	else:
		print e, "is a", t, "expression"
		print "\tinfix   :", expr.infix()
		print "\tprefix  :", expr.prefix()
		print "\tpostfix :", expr.postfix()
