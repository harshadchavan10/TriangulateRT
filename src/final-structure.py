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


# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys,codecs,pickle,time,shelve,re

def printusage():
	print 'Format : python '+sys.argv[0]+' <source-corpus> <pivot-corpus> <target-corpus>'

if(len(sys.argv)!=4):
	printusage()
	exit(1)


scorpus = sys.argv[1]
pcorpus = sys.argv[2]
tcorpus = sys.argv[3]

itcorpus = tcorpus + '.validPhraseDict'
pstrans = pcorpus + '.toSource.validTrans'
tptrans = tcorpus + '.toPivot.validTrans'


#####################################  LOAD FILES ###################################

print '<<< Loading '+itcorpus+' dictionary >>>\n'	
starttime = time.time()
with open(itcorpus, "rb") as f1:
	validt = pickle.load(f1)
print 'The dictionary loaded in '+str(time.time()-starttime)+'\n'

#############

print '<<< Loading '+pstrans+' dictionary >>>\n'	
starttime = time.time()
with open(pstrans, "rb") as f2:
	psTrans = pickle.load(f2)
print 'The dictionary loaded in '+str(time.time()-starttime)+'\n'

#############

print '<<< Loading '+tptrans+' dictionary >>>\n'	
starttime = time.time()
with open(tptrans, "rb") as f3:
	tpTrans = pickle.load(f3)
print 'The dictionary loaded in '+str(time.time()-starttime)+'\n'


#################################### CALCULATE FINAL STRUCTURE ################################

final = {}
start = time.time()
for row, validdict in validt.iteritems():

	starttime = time.time()
	validlist = list(set(validdict.keys()))
	ttop = {}
	for valid in validlist:
		
		ptrans = {}
		try:
			ptrans = tpTrans[valid][row]
		except:
			continue

		pivottranslist = list(set(ptrans.keys()))
		ptos = {}
		for pivot in pivottranslist:
			
			try:
				ptos[pivot] = psTrans[pivot][row]
			except:
				pass
		
		if(len(ptos) > 0):
			ttop[valid] = ptos

	if(len(ttop) > 0):
		final[row] = ttop
	if((row % 500) == 0):
		print 'Final Structure for Line '+str(row)+' prepared in '+str(time.time()-starttime)+' s'

print '\n\nTotal execution time (without loadtime) : '+str(time.time()-start)+' s'
print '\nDumping final structre (t>p>s all possinle translation) in the finalStruct dictionary !!'
with open('finalStruct', "wb") as f4:
	pickle.dump(final, f4)





