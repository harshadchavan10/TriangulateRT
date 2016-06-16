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


############################ FUNCTION TO GET DISTINCT PHRASES #######################################

def calc_dist(corpus, dictname, corpusname):

	print '###########################################################'
	print 'Loading valid phrase dictionary of the '+corpus+' corpus'
	print '###########################################################'
	starttime = time.time()
	with open(dictname, "rb") as f:
		valids = pickle.load(f)
	print 'The dictionary loaded in '+str(time.time()-starttime)+'\n'

	distinct = {}
	print 'Processing the dictionary (line by line wrt corpus)\n'

	for key, valid in valids.iteritems():

		starttime = time.time()		
		phrases = valid.keys()
		for phrase in phrases:

			try:
				distinct[phrase].append(key)
			except:
				distinct[phrase] = [key]
		if((key % 500) == 0):
			print 'Row '+str(key)+' processed in time : '+str(time.time()-starttime)+' s'
    
	return distinct
	
	
################################### FUNCTION TO CALCULATE VALID TRANSLATIONS ####################################

def calc_valid_trans(message, distinct, transdict, validPhrases, filename, value):
	
	print '\n\nFinding '+message+' language valid translation of the phrases !!\n'
	
	print '<<< Loading '+transdict+' dictionary >>>\n'	
	starttime = time.time()
	with open(transdict, "rb") as f1:
		trans = pickle.load(f1)
	print 'The dictionary loaded in '+str(time.time()-starttime)+'\n'

	print '<<< Loading '+validPhrases+' dictionary >>>\n'	
	starttime = time.time()
	with open(validPhrases, "rb") as f3:
		valids = pickle.load(f3)
	print 'The dictionary loaded in '+str(time.time()-starttime)+'\n'

	validtrans = {}
	length = str(len(distinct))
	count = 0

	for phrase, rowlist in distinct.iteritems():

		starttime = time.time()		
		rowtrans = {}
		count = count +1
		for row in rowlist:
			
			tempdict = {}
			validlist = valids[row]
			for p in validlist:
				
				try: 
					if(trans[phrase][p]):
						tempdict[p] = value
				except:
					pass
			if(len(tempdict) > 0):
				rowtrans[row] = tempdict
	
		if(len(rowtrans) > 0):		
			validtrans[phrase] = rowtrans
		if((count % 500) == 0):
			print 'Phrase '+str(count)+'/'+length+' processed in : '+str(time.time()-starttime)+' s'


	print 'Dumping valid '+message+' translations of distinct phrases in the '+filename+' dictionary !!'
	with open(filename, "wb") as f2:
		pickle.dump(validtrans, f2)

	del trans
	del valids
	del validtrans


############################ MAIN CALL ##################################

iscorpus = scorpus + '.validPhraseDict'
ipcorpus = pcorpus + '.validPhraseDict'
itcorpus = tcorpus + '.validPhraseDict'

pstrans = pcorpus + '.toSource.validTrans'
tstrans = tcorpus + '.toSource.validTrans'
tptrans = tcorpus + '.toPivot.validTrans'

val1 = {}
val2 = 27*[0] 
val3 = 0


distinct = calc_dist('PIVOT', ipcorpus, pcorpus)

calc_valid_trans('PIVOT TO SOURCE', distinct, 'ps-trans', iscorpus, pstrans, val2)

distinct = calc_dist('TARGET', itcorpus, tcorpus)


calc_valid_trans('TARGET TO PIVOT', distinct, 'tp-trans', ipcorpus, tptrans, val1)

calc_valid_trans('TARGET TO SOURCE', distinct, 'ts-trans', iscorpus, tstrans, val3)

