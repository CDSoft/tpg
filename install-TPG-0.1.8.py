#!/usr/bin/env python
import shutil, os, distutils.core
base = '%s/Lib/site-packages'%distutils.core.sys.prefix
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
print '''Installation of TPG version 0.1.8
Author: Christophe Delord
Email : christophe.delord@free.fr
Web   : http://christophe.delord.free.fr/en/tpg/
'''
_cp('TPG.py','%s/TPG.py'%base)
_mkdir('%s/TPG'%base)
_cp('TPG/License.txt','%s/TPG/License.txt'%base)
_cp('TPG/tp.g','%s/TPG/tp.g'%base)
_mkdir('%s/TPG/examples'%base)
_cp('TPG/examples/README.txt','%s/TPG/examples/README.txt'%base)
_mkdir('%s/TPG/examples/calc'%base)
_cp('TPG/examples/calc/calc.g','%s/TPG/examples/calc/calc.g'%base)
_cp('TPG/examples/calc/calc.py','%s/TPG/examples/calc/calc.py'%base)
_mkdir('%s/TPG/examples/dos2unix'%base)
_cp('TPG/examples/dos2unix/dos2unix.g','%s/TPG/examples/dos2unix/dos2unix.g'%base)
_mkdir('%s/TPG/examples/graph'%base)
_cp('TPG/examples/graph/graph.py','%s/TPG/examples/graph/graph.py'%base)
_cp('TPG/examples/graph/gr','%s/TPG/examples/graph/gr'%base)
_cp('TPG/examples/graph/gr3d','%s/TPG/examples/graph/gr3d'%base)
_cp('TPG/examples/graph/revol','%s/TPG/examples/graph/revol'%base)
_cp('TPG/examples/graph/surf','%s/TPG/examples/graph/surf'%base)
_cp('TPG/examples/graph/tore','%s/TPG/examples/graph/tore'%base)
_mkdir('%s/TPG/examples/notation'%base)
_cp('TPG/examples/notation/notation.py','%s/TPG/examples/notation/notation.py'%base)
_mkdir('%s/TPG/examples/tpg'%base)
_cp('TPG/examples/tpg/tp.g','%s/TPG/examples/tpg/tp.g'%base)
_cp('uninstall-TPG-0.1.8.py','%s/uninstall-TPG-0.1.8.py'%base)
