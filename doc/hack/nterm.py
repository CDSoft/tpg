
class Foo(tpg.base.ToyParser,):

    def S(self,):
        """ S -> NTerm1 NTerm2 NTerm3 NTerm4 """
        self.NTerm1()
        self.NTerm2(arg1,arg2)
        ret_val = self.NTerm3()
        ret_val = self.NTerm4(arg1,arg2)

