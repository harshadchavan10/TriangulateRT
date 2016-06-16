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

####################################### CALCULATIONS ####################################

def calc_adjacents(corpus, dictname, sdictleft, sdictright):

	print '##########################################\n'
	print 'Loading the dictionary containg valid phrases from the '+corpus+' corpus'
	print '##########################################\n'
	starttime = time.time()
	with open(dictname, "rb") as myFile1:
		validDict = pickle.load(myFile1)
	print '\nThe dictionary loaded in '+str(time.time()-starttime)+'\n'

	iprevphrases = {}
	ipostphrases = {}

	for key,dictionary in validDict.iteritems():
	
		prevspace = {}
		postspace = {}

		starttime = time.time()

		for phrase,limit in dictionary.iteritems():

			try:
				prevspace[limit[0]-1].append(phrase)
			except:
				prevspace[limit[0]-1] = [phrase]

	
			try:
				postspace[limit[1]+1].append(phrase)
			except:
				postspace[limit[1]+1] = [phrase]

		prevphrases = {}
		postphrases = {}
		for phrase,limit in dictionary.iteritems():
		
			try:
				prevphrases[phrase] = postspace[limit[0]-1]
			except:
				prevphrases[phrase] = []

			try:
				postphrases[phrase] = prevspace[limit[1]+1]
			except:
				postphrases[phrase] = []

		iprevphrases[key] = prevphrases
		ipostphrases[key] = postphrases

		if((key % 500) == 0):
			print 'All the adjacent phrases for each phrase in Row : '+str(key)+' are calculated in '+str(time.time()-starttime)+' s'
		
		if(key == 1):
			print dictionary
			print '\n\n'
			print postspace
			print '\n\n'
			print prevphrases
			print '\n\n'
		
	print 'Dumping left adjacent phrases to '+sdictleft+'\n'
	with open(sdictleft, "wb") as myfile1:
		pickle.dump(iprevphrases, myfile1)

	print 'Dumping right adjacent phrases to '+sdictright+'\n'
	with open(sdictright, "wb") as myfile2:
		pickle.dump(ipostphrases, myfile2)
	

####################################### FINDING NAMES FOR NEW DICTIONARIES ####################################

sdict = scorpus + '.validPhraseDict'
pdict = pcorpus + '.validPhraseDict'
tdict = tcorpus + '.validPhraseDict'

sdictleft = scorpus+'.leftPhrases'
sdictright = scorpus+'.rightPhrases'

pdictleft = pcorpus+'.leftPhrases'
pdictright = pcorpus+'.rightPhrases'

tdictleft = tcorpus+'.leftPhrases'
tdictright = tcorpus+'.rightPhrases'


####################################### CALLING METHOD FOR VARIOUS CORPUS #####################################

calc_adjacents('source', sdict, sdictleft, sdictright)
calc_adjacents('pivot', pdict, pdictleft, pdictright)
calc_adjacents('target', tdict, tdictleft, tdictright)

