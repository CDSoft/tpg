#!/usr/bin/env python
import shutil, os, distutils.sysconfig
base = distutils.sysconfig.get_python_lib()
def _mkdir(path):
	try:
		os.makedirs(path)
	except (OSError,IOError),e:
		print e
def _cp(src,dst):
	try:
		shutil.copyfile(src,dst)
	except (OSError,IOError),e:
		print e
def _chmod(mod,dst):
	try:
		os.chmod(dst,mod)
	except (OSError,IOError),e:
		print e
print '''Installation of TPG version 2.0.5
Author: Christophe Delord
Email : christophe.delord@free.fr
Web   : http://christophe.delord.free.fr/en/tpg/
'''
_cp('tpg.py','%s/tpg.py'%base)
_mkdir('%s/TPG'%base)
_cp('TPG/License.txt','%s/TPG/License.txt'%base)
_cp('TPG/tpg_grammar.g','%s/TPG/tpg_grammar.g'%base)
_mkdir('%s/TPG/examples'%base)
_cp('TPG/examples/readme.txt','%s/TPG/examples/readme.txt'%base)
_mkdir('%s/TPG/examples/calc'%base)
_cp('TPG/examples/calc/calc.g','%s/TPG/examples/calc/calc.g'%base)
_cp('TPG/examples/calc/calc.py','%s/TPG/examples/calc/calc.py'%base)
_cp('TPG/examples/calc/calc2.py','%s/TPG/examples/calc/calc2.py'%base)
_cp('TPG/examples/calc/calc3.g','%s/TPG/examples/calc/calc3.g'%base)
_cp('TPG/examples/calc/calc3.py','%s/TPG/examples/calc/calc3.py'%base)
_mkdir('%s/TPG/examples/notation'%base)
_cp('TPG/examples/notation/notation.py','%s/TPG/examples/notation/notation.py'%base)
