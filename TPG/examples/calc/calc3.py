#!/usr/bin/env python2.2

import tpg
from string import atoi, atof, atol
from math import sqrt, cos, sin, tan, acos, asin, atan
class Calc(tpg.ToyParser,dict):

	def __init__(self):
		self._init_scanner(
			(r"vars", r"vars"),
			(r"_tok_1", r"="),
			(r"_tok_2", r"\("),
			(r"_tok_3", r"\)"),
			(r"_tok_4", r","),
			(r"space", r"(\s|\n)+", None, 1),
			(r"pow_op", r"\^|\*\*", self.make_op, 0),
			(r"add_op", r"[+-]", self.make_op, 0),
			(r"mul_op", r"[*/%]", self.make_op, 0),
			(r"funct1", r"(cos|sin|tan|acos|asin|atan|sqr|sqrt|abs)\b", self.make_op, 0),
			(r"funct2", r"(norm)\b", self.make_op, 0),
			(r"real", r"(\d+\.\d*|\d*\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+", atof, 0),
			(r"integer", r"\d+", atol, 0),
			(r"VarId", r"[a-zA-Z_]\w*", None, 0),
		)

	
	def mem(self):
		vars = self.items()
		vars.sort()
		return "\n\t" + "\n\t".join([ "%s = %s"%(var, val) for (var, val) in vars ])
	
	def make_op(self, op):
		return {
			'+'   : (lambda x,y:x+y),
			'-'   : (lambda x,y:x-y),
			'*'   : (lambda x,y:x*y),
			'/'   : (lambda x,y:x/y),
			'^'   : (lambda x,y:x**y),
			'**'  : (lambda x,y:x**y),
			'cos' : cos,
			'sin' : sin,
			'tan' : tan,
			'acos': acos,
			'asin': asin,
			'atan': atan,
			'sqr' : (lambda x:x*x),
			'sqrt': sqrt,
			'abs' : abs,
			'norm': (lambda x,y:sqrt(x*x+y*y)),
		}[op]
	def START(self,):
		""" START -> 'vars'  | VarId '=' Expr  | Expr """
		__p1 = self._cur_token
		try:
			try:
				self._eat('vars')
				e = self.mem()
			except tpg.TPGWrongMatch:
				self._cur_token = __p1
				v = self._eat('VarId')
				self._eat('_tok_1') # =
				e = self.Expr()
				self[v] = e
		except tpg.TPGWrongMatch:
			self._cur_token = __p1
			e = self.Expr()
		return e

	def Var(self,):
		""" Var -> VarId """
		v = self._eat('VarId')
		return self.get(v,0)

	def Expr(self,):
		""" Expr -> Term (add_op Term )* """
		e = self.Term()
		__p1 = self._cur_token
		while 1:
			try:
				op = self._eat('add_op')
				t = self.Term()
				e = op(e,t)
				__p1 = self._cur_token
			except tpg.TPGWrongMatch:
				self._cur_token = __p1
				break
		return e

	def Term(self,):
		""" Term -> Fact (mul_op Fact )* """
		t = self.Fact()
		__p1 = self._cur_token
		while 1:
			try:
				op = self._eat('mul_op')
				f = self.Fact()
				t = op(t,f)
				__p1 = self._cur_token
			except tpg.TPGWrongMatch:
				self._cur_token = __p1
				break
		return t

	def Fact(self,):
		""" Fact -> add_op Fact  | Pow """
		__p1 = self._cur_token
		try:
			op = self._eat('add_op')
			f = self.Fact()
			f = op(0,f)
		except tpg.TPGWrongMatch:
			self._cur_token = __p1
			f = self.Pow()
		return f

	def Pow(self,):
		""" Pow -> Atom (pow_op Fact )? """
		f = self.Atom()
		__p1 = self._cur_token
		try:
			op = self._eat('pow_op')
			e = self.Fact()
			f = op(f,e)
		except tpg.TPGWrongMatch:
			self._cur_token = __p1
		return f

	def Atom(self,):
		""" Atom -> real | integer | Function | Var | '\(' Expr '\)' """
		__p1 = self._cur_token
		try:
			try:
				try:
					try:
						a = self._eat('real')
					except tpg.TPGWrongMatch:
						self._cur_token = __p1
						a = self._eat('integer')
				except tpg.TPGWrongMatch:
					self._cur_token = __p1
					a = self.Function()
			except tpg.TPGWrongMatch:
				self._cur_token = __p1
				a = self.Var()
		except tpg.TPGWrongMatch:
			self._cur_token = __p1
			self._eat('_tok_2') # \(
			a = self.Expr()
			self._eat('_tok_3') # \)
		return a

	def Function(self,):
		""" Function -> funct1 '\(' Expr '\)'  | funct2 '\(' Expr ',' Expr '\)'  """
		__p1 = self._cur_token
		try:
			f = self._eat('funct1')
			self._eat('_tok_2') # \(
			x = self.Expr()
			self._eat('_tok_3') # \)
			y = f(x)
		except tpg.TPGWrongMatch:
			self._cur_token = __p1
			f = self._eat('funct2')
			self._eat('_tok_2') # \(
			x1 = self.Expr()
			self._eat('_tok_4') # ,
			x2 = self.Expr()
			self._eat('_tok_3') # \)
			y = f(x,y)
		return y


calc = Calc()
while 1:
	l = raw_input("\n:")
	if l:
		try:
			print calc(l)
		except (tpg.SyntaxError, tpg.LexicalError), e:
			print e
		except ZeroDivisionError:
			print "Zero Division Error"
		except OverflowError:
			print "Overflow Error"
	else:
		break