#!/usr/bin/env python

#........[ TOY PARSER GENERATOR ].........................!
#                                                        ! !
# Warning: This file was automatically generated by TPG ! | !
# Do not edit this file unless you know what you do.   !  |  !
#                                                     !   @   !
#....................................................!!!!!!!!!!!
#
# For further information about TPG you can visit
# http://christophe.delord.free.fr/en/tpg

import tpg.base

import math
import operator
import string
class Calc(tpg.base.ToyParser,dict):

	def _init_scanner(self):
		self._lexer = tpg.base._Scanner(
			tpg.base._TokenDef(r"_kw_vars", r"vars"),
			tpg.base._TokenDef(r"_tok_1", r"="),
			tpg.base._TokenDef(r"_tok_2", r"\("),
			tpg.base._TokenDef(r"_tok_3", r"\)"),
			tpg.base._TokenDef(r"_tok_4", r","),
			tpg.base._TokenDef(r"space", r"\s+", None, 1),
			tpg.base._TokenDef(r"pow_op", r"\^|\*\*", self.make_op, 0),
			tpg.base._TokenDef(r"add_op", r"[+-]", self.make_op, 0),
			tpg.base._TokenDef(r"mul_op", r"[*/%]", self.make_op, 0),
			tpg.base._TokenDef(r"funct1", r"(cos|sin|tan|acos|asin|atan|sqr|sqrt|abs)\b", self.make_op, 0),
			tpg.base._TokenDef(r"funct2", r"(norm)\b", self.make_op, 0),
			tpg.base._TokenDef(r"real", r"(\d+\.\d*|\d*\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+", string.atof, 0),
			tpg.base._TokenDef(r"integer", r"\d+", string.atol, 0),
			tpg.base._TokenDef(r"VarId", r"[a-zA-Z_]\w*", None, 0),
		)

	
	def mem(self):
		vars = self.items()
		vars.sort()
		memory = [ "%s = %s"%(var, val) for (var, val) in vars ]
		return "\n\t" + "\n\t".join(memory)
	
	def make_op(self, op):
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
	def START(self,):
		""" START -> 'vars' | VarId '=' Expr | Expr """
		__p1 = self._cur_token
		try:
			self._eat('_kw_vars') # vars
			e = self.mem()
		except self.TPGWrongMatch:
			self._cur_token = __p1
			try:
				v = self._eat('VarId')
				self._eat('_tok_1') # =
				e = self.Expr()
				self[v] = e
			except self.TPGWrongMatch:
				self._cur_token = __p1
				e = self.Expr()
		return e

	def Var(self,):
		""" Var -> VarId """
		v = self._eat('VarId')
		return self.get(v,0)

	def Expr(self,):
		""" Expr -> Term (add_op Term)* """
		e = self.Term()
		__p1 = self._cur_token
		while 1:
			try:
				op = self._eat('add_op')
				t = self.Term()
				e = op(e,t)
				__p1 = self._cur_token
			except self.TPGWrongMatch:
				self._cur_token = __p1
				break
		return e

	def Term(self,):
		""" Term -> Fact (mul_op Fact)* """
		t = self.Fact()
		__p1 = self._cur_token
		while 1:
			try:
				op = self._eat('mul_op')
				f = self.Fact()
				t = op(t,f)
				__p1 = self._cur_token
			except self.TPGWrongMatch:
				self._cur_token = __p1
				break
		return t

	def Fact(self,):
		""" Fact -> add_op Fact | Pow """
		__p1 = self._cur_token
		try:
			op = self._eat('add_op')
			f = self.Fact()
			f = op(0,f)
		except self.TPGWrongMatch:
			self._cur_token = __p1
			f = self.Pow()
		return f

	def Pow(self,):
		""" Pow -> Atom (pow_op Fact)? """
		f = self.Atom()
		__p1 = self._cur_token
		try:
			op = self._eat('pow_op')
			e = self.Fact()
			f = op(f,e)
		except self.TPGWrongMatch:
			self._cur_token = __p1
		return f

	def Atom(self,):
		""" Atom -> real | integer | Function | Var | '\(' Expr '\)' """
		__p1 = self._cur_token
		try:
			try:
				a = self._eat('real')
			except self.TPGWrongMatch:
				self._cur_token = __p1
				a = self._eat('integer')
		except self.TPGWrongMatch:
			self._cur_token = __p1
			try:
				a = self.Function()
			except self.TPGWrongMatch:
				self._cur_token = __p1
				try:
					a = self.Var()
				except self.TPGWrongMatch:
					self._cur_token = __p1
					self._eat('_tok_2') # \(
					a = self.Expr()
					self._eat('_tok_3') # \)
		return a

	def Function(self,):
		""" Function -> funct1 '\(' Expr '\)' | funct2 '\(' Expr ',' Expr '\)' """
		__p1 = self._cur_token
		try:
			f = self._eat('funct1')
			self._eat('_tok_2') # \(
			x = self.Expr()
			self._eat('_tok_3') # \)
			y = f(x)
		except self.TPGWrongMatch:
			self._cur_token = __p1
			f = self._eat('funct2')
			self._eat('_tok_2') # \(
			x1 = self.Expr()
			self._eat('_tok_4') # ,
			x2 = self.Expr()
			self._eat('_tok_3') # \)
			y = f(x1,x2)
		return y


print "Calc (TPG example)"
calc = Calc()
while 1:
	l = raw_input("\n:")
	if l:
		try:
			print calc(l)
		except Exception, e:
			print e
	else:
		break