
class IndentParser(tpg.base.ToyParser,):

    def _init_indent_preprocessor(self):
        self._indent_preprocessor = self.indent_deindent(r"\s", r"#")

    def _init_scanner(self):
        self._lexer = tpg.base._Scanner(
            tpg.base._TokenDef(r"_tok_1", r"\w+"),
            tpg.base._TokenDef(r"indent", r"\020", None, 0),
            tpg.base._TokenDef(r"deindent", r"\021", None, 0),
            tpg.base._TokenDef(r"spaces", r"\s", None, 1),
            tpg.base._TokenDef(r"comment", r"#.*", None, 1),
        )

    def BLOCK(self,):
        """ BLOCK -> (INSTR | indent BLOCK deindent)* """
        __p1 = self._cur_token
        while 1:
            try:
                try:
                    self.INSTR()
                except self.TPGWrongMatch:
                    self._cur_token = __p1
                    self._eat('indent')
                    self.BLOCK()
                    self._eat('deindent')
                __p1 = self._cur_token
            except self.TPGWrongMatch:
                self._cur_token = __p1
                break

    def INSTR(self,):
        """ INSTR -> '\w+' """
        self._eat('_tok_1') # \w+

