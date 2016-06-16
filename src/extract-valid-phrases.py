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


def calc_valid_phrases(message, dictname, corpus):

	print '\n'+ message
	spdict = {}
	validPhrases = {}
	starttime = time.time()
	with open(dictname, "rb") as myFile1:
		spdict = pickle.load(myFile1)
	print 'The dictionary loaded in '+str(time.time()-starttime)+'\n'

	print 'Processing the corpus line by line\n'

	f1 = codecs.open(corpus ,encoding='utf-8', errors="ignore")
	linecount = 0


	for line in f1:

		starttime = time.time()
		linecount = linecount + 1
		spacePos = [m.start() for m in re.finditer(' ', line)]
		spacePos.insert(0,0)
		spacePos.append(len(line)-1)

		pos = len(spacePos)
		phrases = {}
		valid = {}

		for length in range(1,pos):
		
			for i in range(0,pos-length):
			
				key = line[spacePos[i]:spacePos[i+length]].strip()
			
				if(i == 0):
					value = [0,spacePos[i+length]-1]
				else:
					value = [spacePos[i]+1,spacePos[i+length]-1]
			
				phrases[key] = value

		keys = spdict.keys()
		for key,value in phrases.iteritems():
			try:
				if(spdict[key]):
					valid[key] = phrases[key]
			except:
				pass
	
		validPhrases[linecount] = valid
		if((linecount % 500) == 0):
			print 'Line Number : '+str(linecount)+' All the valid phrases calculated in '+str(time.time()-starttime)+' s'

	print '\nPhrase calculations completed !!\n'
	dumpname = corpus+'.validPhraseDict'
	print 'Dumping valid phrases in the \"'+corpus+'\" corpus in the dictionary by the name \"'+dumpname+'\" !'
	with open(dumpname, "wb") as myfile1:
		pickle.dump(validPhrases, myfile1)


############################################ MAIN CALL ###################################################

calc_valid_phrases('Loading SOURCE-PIVOT dictionary', "sp-trans", scorpus)
calc_valid_phrases('Loading PIVOT-TARGET dictionary', "pt-trans", pcorpus)
calc_valid_phrases('Loading TARGET-PIVOT dictionary', "tp-trans", tcorpus)


