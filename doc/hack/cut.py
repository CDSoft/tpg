
class Foo(tpg.base.ToyParser,):

	def S(self,):
		""" S -> A1 B1 C1 | A2 B2 C2 """
		__p1 = self._cur_token
		try:
			self.A1()
			try:
				self.B1()
				self.C1()
			except self.TPGWrongMatch, e:
				self.ParserError(e.last)
		except self.TPGWrongMatch:
			self._cur_token = __p1
			self.A2()
			try:
				self.B2()
				self.C2()
			except self.TPGWrongMatch, e:
				self.ParserError(e.last)