
class Foo(tpg.base.ToyParser,):

	def _init_scanner(self):
		self._lexer = tpg.base._Scanner(
			tpg.base._TokenDef(r"_tok_1", r"\("),
			tpg.base._TokenDef(r"_tok_2", r"\)"),
			tpg.base._TokenDef(r"integer", r"\d+", int, 0),
			tpg.base._TokenDef(r"arrow", r"->", None, 0),
			tpg.base._TokenDef(r"spaces", r"\s+", None, 1),
		)

	def S(self,):
		""" S -> '\(' integer arrow '\)' """
		self._eat('_tok_1') # \(
		self._eat('integer')
		self._eat('arrow')
		self._eat('_tok_2') # \)