""" Base class for TPG generated parsers


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

import re

class _TokenDef:
	""" Token definition for the scanner """

	ident_pat = re.compile(r'^\w+$')

	def __init__(self, tok, regex=None, action=None, separator=0):
		if regex is None: regex = tok
		if self.ident_pat.match(regex): regex += r'\b'	# match 'if\b' instead of 'if'
		if action is None: action = lambda x:x			# default action if identity
		elif not callable(action): action = lambda x,y=action:y	# action must be callable
		self.tok = tok							# token name
		self.regex = '(?P<%s>%s)'%(tok, regex)	# token regexp
		self.action = action					# token modifier
		self.separator = separator				# is this a separator ?

	def __str__(self):
		return "token %s: %s %s;"%(self.tok, self.regex, self.action)

class _Token:
	""" Token instanciated while scanning """

	def __init__(self, tok, text, val, lineno, start, end):
		self.tok = tok			# token type
		self.text = text		# matched text
		self.val = val			# value (ie action(text))
		self.lineno = lineno	# token line number
		self.start = start		# token start index
		self.end = end			# token end index

	def __str__(self):
		return "%d:%s[%s]"%(self.lineno, self.tok, self.val)

class _Eof:
	""" EOF token """

	def __init__(self, lineno='EOF'):
		self.lineno = lineno
		self.text = 'EOF'
		self.val = 'EOF'

	def __str__(self):
		return "%s:Eof"%self.lineno

class _Scanner:
	""" Lexical scanner """

	def __init__(self, *tokens):
		regex = []				# regex list
		actions = {}			# dict token->action
		separator = {}			# set of separators
		for token in tokens:
			regex.append(token.regex)
			actions[token.tok] = token.action
			separator[token.tok] = token.separator
		self.regex = re.compile('|'.join(regex))	# regex is the choice between all tokens
		self.actions = actions
		self.separator = separator

	def tokens(self, input):
		""" Scan input and return a list of _Token instances """
		self.input = input
		i = 0				# start of the next token
		l = len(input)
		lineno = 1			# current token line number
		toks = []			# token list
		while i<l:												# while not EOF
			token = self.regex.match(input,i)					# get next token
			if not token:										# if none raise LexicalError
				last = toks and toks[-1] or _Eof(lineno)
				raise LexicalError(last)
			j = token.end()										# end of the current token
			for (t,v) in token.groupdict().items():				# search the matched token
				if v is not None and self.actions.has_key(t):
					tok = t										# get its type
					text = token.group()						# get matched text
					val = self.actions[tok](text)				# compute its value
					break
			if not self.separator[tok]:								# if the matched token is a real token
				toks.append(_Token(tok, text, val, lineno, i, j))	# store it
			lineno += input.count('\n', i, j)					# update lineno
			i = j												# go to the start of the next token
		return toks

class ToyParser:
	""" Base class for every TPG parsers """

	class TPGWrongMatch(Exception):
		def __init__(self, last):
			self.last = last

	def __init__(self):
		self._init_scanner()

	def _eat(self, token):
		""" Eat one token """
		try:
			t = self._tokens[self._cur_token]	# get current token
		except IndexError:						# if EOF
			self.WrongMatch()					# raise TPGWrongMatch to backtrack
		if t.tok == token:						# if current is an expected token
			self._cur_token += 1				# go to the next one
			return t.val						# and return its value
		else:
			self.WrongMatch()					# else backtrack

	def WrongMatch(self):
		""" Backtracking """
		try:
			raise self.TPGWrongMatch(self._tokens[self._cur_token])
		except IndexError:
			raise self.TPGWrongMatch(_Eof())

	def check(self, cond):
		""" Check a condition while parsing """
		if not cond:			# if condition is false
			self.WrongMatch()	# backtrack

	def __call__(self, input, *args):
		""" Parse the axiom of the grammar (if any) """
		return self.parse('START', input, *args)

	def parse(self, symbol, input, *args):
		""" Parse an input start at a given symbol """
		try:
			self._tokens = self._lexer.tokens(input)	# scan tokens
			self._cur_token = 0							# start at the first token
			ret = getattr(self, symbol)(*args)			# call the symbol
			if self._cur_token < len(self._tokens):		# if there are unparsed tokens
				self.WrongMatch()						# raise an error
			return ret									# otherwise return the result
		except self.TPGWrongMatch, e:					# convert an internal TPG error
			raise SyntaxError(e.last)					# into a SyntaxError

	def _mark(self):
		""" Get a mark for the current token """
		return self._cur_token

	def _extract(self, a, b):
		""" Extract text between 2 marks """
		if not self._tokens: return ""
		if a<len(self._tokens):
			start = self._tokens[a].start
		else:
			start = self._tokens[-1].end
		if b>0:
			end = self._tokens[b-1].end
		else:
			end = self._tokens[0].start
		return self._lexer.input[start:end]

	def lineno(self, mark=None):
		""" Get the line number of a mark (or the current token if none) """
		if mark is None: mark = self._cur_token
		if not self._tokens: return 0
		if mark<len(self._tokens):
			return self._tokens[mark].lineno
		else:
			return self._tokens[-1].lineno
	
class LexicalError(Exception):
	def __init__(self, last):
		self.last = last
	def __str__(self):
		if self.last:
			return "%s: Lexical error near %s"%(self.last.lineno, self.last.text)
		else:
			return "1: Lexical error"

class SyntaxError(Exception):
	def __init__(self, last):
		self.last = last
	def __str__(self):
		if self.last:
			return "%s: Syntax error near %s"%(self.last.lineno, self.last.text)
		else:
			return "1: Syntax error"

