

class Couple:
	def __init__(self, a, b):
		self.a = a
		self.b = b
class Foo(tpg.base.ToyParser,):

	def COUPLE1(self,):
		""" COUPLE1 ->  """
		c = Couple(a,b)
		return c

	def COUPLE2(self,):
		""" COUPLE2 ->  """
		return Couple(a,b)