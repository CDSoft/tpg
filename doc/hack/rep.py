
class Repetitions(tpg.base.ToyParser,):

	def ZERO_or_ONE(self,):
		""" ZERO_or_ONE -> A? """
		__p1 = self._cur_token
		try:
			self.A()
		except self.TPGWrongMatch:
			self._cur_token = __p1

	def ZERO_or_MORE(self,):
		""" ZERO_or_MORE -> A* """
		__p1 = self._cur_token
		while 1:
			try:
				self.A()
				__p1 = self._cur_token
			except self.TPGWrongMatch:
				self._cur_token = __p1
				break

	def ONE_or_MORE(self,):
		""" ONE_or_MORE -> A+ """
		__p1 = self._cur_token
		__n1 = 0
		while 1:
			try:
				self.A()
				__n1 += 1
				__p1 = self._cur_token
			except self.TPGWrongMatch:
				if __n1 >= 1:
					self._cur_token = __p1
					break
				else:
					self.WrongMatch()