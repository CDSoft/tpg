#!/usr/bin/env python

import sys
import os, os.path
import tpg

force = 0

to_be_removed = [
"""
	def _init_scanner(self):
		self._lexer = tpg.base._Scanner(
		)
""",
"import tpg.base"
]

def comment(l):
	if l[:2] == '#!': return False
	if l[:1] == '#': return True
	return False

def gen(name):
	name_py = name.replace('.g','.py')
	if force or not os.path.isfile(name_py) or os.stat(name_py).st_mtime < os.stat(name).st_mtime:
		print name
		f = open(name)
		grammar = f.read()
		f.close()
		#code = tpg.compile(grammar).replace('\r','')
		code = tpg.compile(grammar)
		code = "".join([ "%s\n"%l for l in code.splitlines() if not comment(l) ])
		for rem in to_be_removed:
			code = code.replace(rem, '')
		code = "\n".join([ l.rstrip() for l in code.splitlines() ])
		while code.find('\n\n\n')>=0:
			code = code.replace('\n\n\n','\n')
		f = open(name.replace('.g','.py'), 'w')
		f.write(code)
		f.close()

for name in os.listdir('.'):
	if name.endswith('.g'):
		gen(name)
