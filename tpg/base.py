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

_ident_pat = re.compile(r'^\w+$')

class _TokenDef:
	""" Token definition for the scanner """

	def __init__(self, tok, regex=None, action=None, separator=0):
		if regex is None: regex = tok
		if _ident_pat.match(regex): regex += r'\b'		# match 'if\b' instead of 'if'
		if action is None: action = lambda x:x			# default action is identity
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
			if not token:										# if none raise LexerError
				last = toks and toks[-1] or _Eof(lineno)
				raise LexerError(last)
			j = token.end()										# end of the current token
			tok = token.lastgroup								# get the type of the last token
			text = token.group()								# get the matched text
			val = self.actions[tok](text)						# and compute its value
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

	def __init__(self, *args):
		self._init_scanner()
		try:
			self.init(*args)
		except AttributeError:
			pass

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

	def LexerError(self, last): raise LexerError(last)
	def ParserError(self, last): raise ParserError(last)
	def SemanticError(self, last, error=""): raise SemanticError(last, error)

	def check(self, cond):
		""" Check a condition while parsing """
		if not cond:			# if condition is false
			self.WrongMatch()	# backtrack

	def error(self, error):
		""" Raises an exception to abort parsing """
		try:
			raise SemanticError(self._tokens[self._cur_token],error)
		except IndexError:
			raise SemanticError(_Eof(),error)

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
			raise ParserError(e.last)					# into a ParserError

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

class ToyParserCSL(ToyParser):
	""" Base class for CSL parsers (parsers with Context Sensitive Lexer) """

	def __init__(self, *args):
		self._patterns = {}
		try:
			self.init(*args)
		except AttributeError:
			pass

	class _pos:
		def __init__(self, pos=0, line=1, text=None):
			self.pos = pos
			self.line = line
			self.text = text
		def copy(self): return ToyParserCSL._pos(self.pos, self.line, self.text)

	def _eat(self, regexp, split=0):
		""" Eat one token (separator* token) """
		self._lex_separator()
		return self._lex_eat(regexp, save_token=1, split=split)

	def _lex_separator(self):
		""" Skip separators if any (separator*) """
		try:
			separator = self.separator
		except AttributeError:
			return
		while 1:
			try:
				separator()
			except self.TPGWrongMatch:
				break

	def _lex_eat(self, regexp, save_token=0, split=0):
		""" Eat one token """
		try:
			pat = self._patterns[regexp]
		except KeyError:
			if _ident_pat.match(regexp):
				pat = re.compile(regexp+r'\b')
			else:
				pat = re.compile(regexp)
			self._patterns[regexp] = pat
		token = pat.match(self.input, self._cur_token.pos)
		if token:
			self._cur_token.line += self.input.count('\n', self._cur_token.pos, token.end())
			self._cur_token.pos = token.end()
			if save_token:
				self._cur_token.text = token.group()
			if split:
				return token.groups()
			else:
				return token.group()
		self.WrongMatch()

	def WrongMatch(self):
		""" Backtracking """
		if self._cur_token.text is not None:
			last = _Token(None, self._cur_token.text, None, self._cur_token.line, None, None)
		else:
			last = _Eof()
		raise self.TPGWrongMatch(last)

	def setInput(self, input):
		self.input = input
		self._cur_token = self._pos()

	def parse(self, symbol, input, *args):
		""" Parse an input start at a given symbol """
		try:
			self.setInput(input)
			return getattr(self, symbol)(*args)
		except self.TPGWrongMatch, e:
			raise ParserError(e.last)

	def _mark(self):
		""" Get a mark for the current token """
		return self._cur_token

	def _extract(self, a, b):
		""" Extract text between 2 marks """
		return self.input[a.pos:b.pos]

	def lineno(self, mark=None):
		""" Get the line number of a mark (or the current token if none) """
		if mark is None: mark = self._cur_token
		return mark.line

class Error(Exception):
	def __init__(self, last):
		self.last = last
	def __str__(self):
		if self.last:
			return "%s: %s error near %s"%(self.last.lineno, self.type, self.last.text)
		else:
			return "1: %s error"%self.type

class LexerError(Error):
	type = "Lexical"

class ParserError(Error):
	type = "Syntax"

class SemanticError(Error):
	type = "Semantic"
	def __init__(self, last, error):
		Error.__init__(self, last)
		self.error = error
	def __str__(self):
		return "%s (%s)"%(Error.__str__(self), self.error)
