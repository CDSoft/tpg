#!/usr/bin/env python
import os, distutils.sysconfig
base = distutils.sysconfig.get_python_lib()
def _rm(name):
	try:
		os.remove(name)
	except (OSError,IOError),e:
		print e
def _rmdir(name):
	try:
		os.removedirs(name)
	except (OSError,IOError),e:
		print e
print '''Uninstallation of TPG version 2.0.3
Author: Christophe Delord
Email : christophe.delord@free.fr
Web   : http://christophe.delord.free.fr/en/tpg/
'''
_rm('%s/tpg.py'%base)
_rm('%s/TPG/License.txt'%base)
_rm('%s/TPG/tpg_grammar.g'%base)
_rm('%s/TPG/examples/readme.txt'%base)
_rm('%s/TPG/examples/calc/calc.g'%base)
_rm('%s/TPG/examples/calc/calc.py'%base)
_rm('%s/TPG/examples/calc/calc2.py'%base)
_rm('%s/TPG/examples/calc/calc3.g'%base)
_rm('%s/TPG/examples/calc/calc3.py'%base)
_rm('%s/TPG/examples/notation/notation.py'%base)
_rmdir('%s/TPG/examples/notation'%base)
_rmdir('%s/TPG/examples/calc'%base)
_rmdir('%s/TPG/examples'%base)
_rmdir('%s/TPG'%base)
_rm('%s/uninstall-TPG-2.0.3.py'%base)
