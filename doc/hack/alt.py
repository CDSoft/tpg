
class Foo(tpg.base.ToyParser,):

	def S(self,):
		""" S -> A | B | C """
		__p1 = self._cur_token
		try:
			try:
				self.A()
			except self.TPGWrongMatch:
				self._cur_token = __p1
				self.B()
		except self.TPGWrongMatch:
			self._cur_token = __p1
			self.C()