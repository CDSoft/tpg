

class List(list):
    add = list.append
class Foo(tpg.base.ToyParser,):

    def LIST(self,):
        """ LIST -> ITEM """
        l = List()
        a = self.ITEM()
        l.add(a)
        return l

