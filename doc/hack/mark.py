
class Foo(tpg.base.ToyParser,):

    def S(self,):
        """ S -> A B C """
        self.A()
        x = self._mark()
        self.B()
        self.C()
        y = self._mark()
        t = self._extract(x,y)

