#!/usr/bin/python
# Copyright 2016 dasding
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys

from lib.util import *
from arctool import *

if len(sys.argv) < 2:
	sys.exit()

if sys.argv[1] == "mhx":
	VERSION = 17
elif sys.argv[1] == "mh4":
	VERSION = 19
elif sys.argv[1] == "mh3":
	VERSION = 16



class PseudoArgs():
	def __init__(self):
		self.index = "index"
		self.base_path = "arcfs"
		self.ver = VERSION

enable_log(True)

args = PseudoArgs()

for file in find("romfs", ".arc"):
	indexdir = os.path.join("arcfs\\.arc_index", file)
	args.index = os.path.join(indexdir, "arc_index")
	create(file, args)

	
