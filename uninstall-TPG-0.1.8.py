#!/usr/bin/env python
import os, distutils.core
base = '%s/Lib/site-packages'%distutils.core.sys.prefix
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
print '''Uninstallation of TPG version 0.1.8
Author: Christophe Delord
Email : christophe.delord@free.fr
Web   : http://christophe.delord.free.fr/en/tpg/
'''
_rm('%s/TPG.py'%base)
_rm('%s/TPG/License.txt'%base)
_rm('%s/TPG/tp.g'%base)
_rm('%s/TPG/examples/README.txt'%base)
_rm('%s/TPG/examples/calc/calc.g'%base)
_rm('%s/TPG/examples/calc/calc.py'%base)
_rm('%s/TPG/examples/dos2unix/dos2unix.g'%base)
_rm('%s/TPG/examples/graph/graph.py'%base)
_rm('%s/TPG/examples/graph/gr'%base)
_rm('%s/TPG/examples/graph/gr3d'%base)
_rm('%s/TPG/examples/graph/revol'%base)
_rm('%s/TPG/examples/graph/surf'%base)
_rm('%s/TPG/examples/graph/tore'%base)
_rm('%s/TPG/examples/notation/notation.py'%base)
_rm('%s/TPG/examples/tpg/tp.g'%base)
_rmdir('%s/TPG/examples/tpg'%base)
_rmdir('%s/TPG/examples/notation'%base)
_rmdir('%s/TPG/examples/graph'%base)
_rmdir('%s/TPG/examples/dos2unix'%base)
_rmdir('%s/TPG/examples/calc'%base)
_rmdir('%s/TPG/examples'%base)
_rmdir('%s/TPG'%base)
_rm('%s/uninstall-TPG-0.1.8.py'%base)
