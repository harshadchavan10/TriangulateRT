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
	print 'Format : python '+sys.argv[0]+' only !!!'

if(len(sys.argv)!=1):
	printusage()
	exit(1)

########################## SOURCE-PIVOT and PIVOT-SOURCE DICTIONARIES CREATION ############################

def sp():

	print '##########################################\nReading SOURCE-PIVOT reordering table\n##########################################\n\n'

	spdict={}
	psdict={}	 
	f1 = codecs.open("sptable",encoding='utf-8', errors="ignore")
	for line in f1:
		temp = (line.split('|'))
		original = temp[0].strip()
		translation = temp[1].strip()
		reorderingProb = temp[2].strip().split(' ')
		reorderingProb = map(float, reorderingProb)
		
		if original in spdict:
			spdict[original][translation]=reorderingProb
		else:
			spdict[original] = {translation:reorderingProb}

		if translation in psdict:
			psdict[translation][original]=reorderingProb
		else:
			psdict[translation] = {original:reorderingProb}
		
	f1.close()

	print 'Dumping the Source-Pivot Dictionary\n'

	with open("sp-trans", "wb") as myfile1:
		pickle.dump(spdict, myfile1)
	spdict={}
	print 'Dumping the Pivot-Source Dictionary\n'

	with open("ps-trans", "wb") as myfile2:
		pickle.dump(psdict, myfile2)
	psdict={}


########################## PIVOT-TARGET and TARGET-PIVOT DICTIONARIES CREATION ############################

def pt():

	print '##########################################\nReading PIVOT-TARGET reordering table\n##########################################\n\n'
	ptdict={}
	tpdict={}
	f2 = codecs.open("pttable",encoding='utf-8', errors="ignore")
	for line in f2:
		temp = (line.split('|'))
		original = temp[0].strip()
		translation = temp[1].strip()
		reorderingProb = temp[2].strip().split(' ')
		reorderingProb = map(float, reorderingProb)
		
		if original in ptdict:
			ptdict[original][translation]=reorderingProb
		else:
			ptdict[original] = {translation:reorderingProb}

		if translation in tpdict:
			tpdict[translation][original]=reorderingProb
		else:
			tpdict[translation] = {original:reorderingProb}
		
        
	f2.close()

	print 'Dumping the Pivot-Target Dictionary\n'

	with open("pt-trans", "wb") as myfile3:
		pickle.dump(ptdict, myfile3)
	ptdict={}

	print 'Dumping the Target-Pivot Dictionary\n'

	with open("tp-trans", "wb") as myfile4:
		pickle.dump(tpdict, myfile4)
	tpdict={}

########################## SOURCE-TARGET and TARGET-SOURCE DICTIONARIES CREATION ############################

def st():

	print '##########################################\nReading SOURCE-TARGET reordering table\n##########################################\n\n'
	stdict={}
	tsdict={}
	f3 = codecs.open("sttable",encoding='utf-8', errors="ignore")
	for line in f3:
		temp = (line.split('|'))
		original = temp[0].strip()
		translation = temp[1].strip()
		reorderingProb = temp[2].strip().split(' ')
		reorderingProb = map(float, reorderingProb)
               
		if original in stdict:
			stdict[original][translation]=reorderingProb
		else:
			stdict[original] = {translation:reorderingProb}

		if translation in tsdict:
			tsdict[translation][original]=reorderingProb
		else:
			tsdict[translation] = {original:reorderingProb}
		
	f3.close()

	print 'Dumping the Source-Target Dictionary\n'

	with open("st-trans", "wb") as myfile5:
		pickle.dump(stdict, myfile5)
	stdict={}

	print 'Dumping the Target-Source Dictionary\n'

	with open("ts-trans", "wb") as myfile6:
		pickle.dump(tsdict, myfile6)
	tsdict={}


############################################## MAIN CALL ####################################################

sp()
pt()

