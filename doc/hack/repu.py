
class Repetitions(tpg.base.ToyParser,):

    def USER_DEFINED(self,):
        """ USER_DEFINED -> A{2,5} """
        __p1 = self._cur_token
        __n1 = 0
        while __n1<5:
            try:
                self.A()
                __n1 += 1
                __p1 = self._cur_token
            except self.TPGWrongMatch:
                if __n1 >= 2:
                    self._cur_token = __p1
                    break
                else:
                    self.WrongMatch()

