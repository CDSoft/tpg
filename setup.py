#!/usr/bin/env python

""" Setup script for Toy Parser Generator

Just run "python setup.py install" to install TPG


Toy Parser Generator: A Python parser generator
Copyright (C) 2002 Christophe Delord
 
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

For further information about TPG you can visit
http://christophe.delord.free.fr/en/tpg

"""

import os
from glob import glob

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

from distutils.core import setup

# Release.py contains version, authors, license, url, keywords, etc.
execfile(os.path.join('tpg','Release.py'))

# Call the setup() routine which does most of the work
setup(name             = name,
      version          = version,
      description      = description,
      long_description = long_description,
      author           = author,
      author_email     = email,
      url              = url,
      license          = license,
      licence          = license, # Spelling error in distutils
      platforms        = platforms,
      keywords         = keywords,
      packages         = ['tpg'], #, 'tpg.base', 'tpg.codegen', 'tpg.parser', 'tpg.Release'],
      scripts          = ['tpg/tpg'],
      #data_files       = [('tpg/examples', glob('tpg/examples/*.[g|py]')),
                          #],
      )

