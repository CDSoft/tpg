
class Foo(tpg.base.ToyParser,):

    def S(self,):
        """ S -> A B C """
        self.A()
        self.B()
        self.C()

