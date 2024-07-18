""" CSeq C Sequentialization Framework
	scope-based variable renaming module
"""
"""

	This module performs just defines the prefixes for the variable renaming 
        done by the superclass
"""

from modules import varnames
import pycparser.c_generator


class dr_varnames(varnames.varnames):

	nondetprefix = '__dr_nondet_'  # prefix for uninitialized local variables 
	prefix = '__dr_local_'        # prefix for initialized local variables
	paramprefix = '__dr_param_'   # prefix for function params


	def loadfromstring(self, string, env, fill_only_fields=None):
		self.cgenerator = pycparser.c_generator.CGenerator()
		super(self.__class__, self).loadfromstring(string, env)
		
	def visit_FuncCall(self, n):
		if hasattr(n.name, "name") and n.name.name == "offsetof":
			ans = self.cgenerator.visit(n)
			return "myoffsetof(\""+ans+"\")"
		else:
			return super().visit_FuncCall(n)
