# Toy Parser Generator: A Python parser generator
# Copyright (C) 2001-2016 Christophe Delord
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For further information about TPG you can visit
# http://cdsoft.fr/tpg

all: tpg.py README doc/tpg.pdf

tpg.py: setup.py tpg tpg.pyg
	python3 setup.py sdist

README: README.md
	cp $< $@

doc/tpg.pdf: $(wildcard doc/*.tex)
	python3 setup.py sdist

test:
	python2 tpg_tests_py2.py
	python2 tpg_tests.py
	python3 tpg_tests.py
