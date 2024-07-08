""" CSeq function inlining module
     
"""
VERSION = 'inliner-0.1-2016.08.16'
# VERSION = 'inliner-0.0-2014.10.19'
# VERSION = 'inliner-0.0-2014.07.15'
# VERSION = 'inliner-0.0-2014.12.24'    # CSeq-1.0beta
# VERSION = 'inliner-0.0-2014.10.31'    # CSeq-Lazy-0.6: newseq-0.6a, newseq-0.6c, SVCOMP15
# VERSION = 'inliner-0.0-2014.10.28'
# VERSION = 'inliner-0.0-2014.03.14'
# VERSION = 'inliner-0.0-2014.03.06 (CSeq-Lazy-0.2)'
# VERSION = 'inliner-0.0-2014.02.27'
# VERSION = 'inliner-0.0-2014.02.25'
# VERSION = 'inliner-0.0-2013.12.02'
# VERSION = 'inliner-0.0-2013.10.24-Gennaro-Omar'


import copy, re, sys
import pycparser.c_parser, pycparser.c_ast, pycparser.c_generator
from pycparser import c_ast
import core.common, core.module, core.parser, core.utils
from modules import inliner


# import sys #DEB

class dr_inliner(inliner.inliner):
    def visit_Return(self, n):
        if len(self.indexStack) > 0:
            if self.Parser.funcIsVoid[self.currentFunction[-1]]:
                return 'goto __exit_%s_%s;' % (self.functionStack[-1], self.indexStack[-1])  # void
            else:
                return '__cs_retval_%s_%s = %s; goto __exit_%s_%s;' % (
                self.functionStack[-1], self.indexStack[-1], self.visit(n.expr), self.functionStack[-1],
                self.indexStack[-1])  # non-void

        if self.currentFunction[-1] in self.Parser.threadName:
            args = self.visit(n.expr) if n.expr else '0'
            self._inliner__exit_args[self.currentFunction[-1]] = args
            if n.expr and type(n.expr) is not c_ast.Constant:
                return '_cs_return_val_helperdr(%s); goto __exit_%s; ' % (args, self.currentFunction[-1])
            else:
                return 'goto __exit_%s; ' % (self.currentFunction[-1])
        elif self.currentFunction[-1] == 'main':
            args = self.visit(n.expr) if n.expr else '0'
            self._inliner__exit_args[self.currentFunction[-1]] = '0'
            if n.expr and type(n.expr) is not c_ast.Constant:
                return '_cs_return_val_helperdr(%s); goto __exit_main; ' % (args,)
            else:
                return 'goto __exit_main; '

        s = 'return'
        if n.expr: s += ' ' + self.visit(n.expr)
        return s + ';'
