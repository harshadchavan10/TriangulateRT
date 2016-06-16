# Copyright Deepak Patil and Harshad Chavan 2016 - present
#
# This file is part of TriangulateRT.
#
# TriangulateRT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# TriangulateRT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# coding: utf-8
#!/usr/bin/python

import sys,codecs,pickle,time,shelve,re

def loadfiles(name):
	print '<<< Loading '+name+' dictionary >>>'
	starttime = time.time()
	dictionary = {}
	with open(name, "rb") as f1:
		dictionary = pickle.load(f1)
	print 'The dictionary loaded in '+str(time.time()-starttime)+' sec length = '+str(len(dictionary))+'\n\t\t-------------------------'
	return dictionary


def calc_paraphrase_nonzero(name):
	finalCount = loadfiles(name)

	total=0
	nonzero = 0
	refarray = 27*[0]

	sources = finalCount.keys()
	for source in sources:

		pivots = finalCount[source].keys()
		for pivot in pivots:

			targets = finalCount[source][pivot].keys()
			for target in targets:

				total +=1

				if(sum(finalCount[source][pivot][target][0]) == 0):
					pass
				else:
					nonzero += 1

	print name + ': ' + "ORIGINAL COUNTS - " + name + "\n################################"
	print name + ': ' + "Total lines in file : " + str(total)
	print name + ': ' + "Total rows with non-zero counts : " + str(nonzero)
	print name + ': ' + "Percentage of non-zero count rows : " + str(float(nonzero)/total*100)


calc_paraphrase_nonzero('paraphrasefinalLeftCountDict')
calc_paraphrase_nonzero('paraphrasefinalRightCountDict')
