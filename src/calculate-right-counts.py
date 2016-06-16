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

################################ MERGE TWO DICTIONARIES ##############################################

def mergedicts(dict1, dict2):
	key2 = dict2.keys()[0]
	if key2 in dict1.keys():
		if type(dict1[key2]) is list:
			dict1[key2] = map(sum, zip(dict1[key2], dict2[key2]))
		else:
			tmp = mergedicts(dict1[key2], dict2[key2])
			dict1[key2] = tmp
	else:
		return dict(dict1.items() + dict2.items())
	return dict1



################################ LOAD DICTIONARIES #########################################################

def loadfiles(name):
	print '<<< Right: Loading '+name+' dictionary >>>'	
	starttime = time.time()
	dictionary = {}
	with open(name, "rb") as f1:
		dictionary = pickle.load(f1)
	print 'Right: The dictionary loaded in '+str(time.time()-starttime)+' sec length = '+str(len(dictionary))+'\n'
	return dictionary



##################### FUNCTION TO GENERATE ALL POSSIBLE PHRASE AND ITS ADJACENT ############################

def calc_count(pst, tst, tpt, sleft, sright, pleft, pright, tright, fstruct, sd, pd):

	count = 0
	rows = fstruct.keys()
	for row in rows:

		starttime = time.time()
		
		targets = fstruct[row].keys()
		for target in targets:

			pivots = fstruct[row][target].keys()
			trgrights = list(set(tright[row][target]))

			if(len(trgrights) > 0):
				for pivot in pivots:	
		
					sources = fstruct[row][target][pivot].keys()
					pivrights = list(set(pright[row][pivot]))

					if(len(pivrights) > 0):
						for source in sources:
		
							templist = 27*[0]
							##########################################################################

							for trg in trgrights:
				
								try:
									pivs = tpt[trg][row].keys()
									if(len(pivs) > 0):
										for piv in pivs:
	
											for pl in pivrights:

												try:
													srcs = pst[pl][row].keys()
													if(len(srcs) > 0):
														for src in srcs:
	
															try:
																tsrcs = tst[trg][row].keys()
																if(len(tsrcs) > 0):
																	for tsrc in tsrcs:

																		count = count + 1
																		
																		# CHECK TARGET TO PIVOT ORIENTATION
																		if piv in pleft[row][pivot]:
																			h = 9  # swap
																		elif piv in pright[row][pivot]:
																			h = 0  # monotone
																		else:
																			if(((pd[row][piv][0] > pd[row][pivot][0]) and (pd[row][piv][0] < pd[row][pivot][1])) or ((pd[row][piv][1] > pd[row][pivot][0]) and (pd[row][piv][1] < pd[row][pivot][1]))):
																				continue
																			else:
																				h = 18  # discontineous


																		# CHECK PIVOT TO SOURCE ORIENTATION
																		if src in sleft[row][source]:
																			d = 3  # swap
																		elif src in sright[row][source]:
																			d = 0  # monotone
																		else:
																			if(((sd[row][src][0] > sd[row][source][0]) and (sd[row][src][0] < sd[row][source][1])) or ((sd[row][src][1] > sd[row][source][0]) and (sd[row][src][1] < sd[row][source][1]))):
																				continue
																			else:
																				d = 6  # discontineous


																		# CHECK TARGET TO SOURCE ORIENTATION 
																		if tsrc in sleft[row][source]:
																			u = 1  # swap
																		elif tsrc in sright[row][source]:
																			u = 0  # monotone
																		else:
																			if(((sd[row][tsrc][0] > sd[row][source][0]) and (sd[row][tsrc][0] < sd[row][source][1])) or ((sd[row][tsrc][1] > sd[row][source][0]) and (sd[row][tsrc][1] < sd[row][source][1]))):
																				continue
																			else:
																				u = 2  # discontineous


																		# UPDATE RESPECTIVE COUNT
																		index = h+d+u
																		templist[index] = templist[index]+1
																		

															except:
																pass
												except:
													pass
								except: 
									pass
				
							############################################################################
							fstruct[row][target][pivot][source] = templist

		if((row % 500) == 0):
			print 'Right: Row '+str(row)+' processed at '+str(time.time()-starttime)+' secs'


	###################################### CREATE finalCount DICTIONARY  ######################################################

	sptlist = []
	allsrc = []

	rows = fstruct.keys()
	starttime = time.time()
	for row in rows:

		targets = fstruct[row].keys()
		for target in targets:

				pivots = fstruct[row][target].keys()
				for pivot in pivots:

				        sources = fstruct[row][target][pivot].keys()
				        for source in sources:
					
							obj = source + u'~~~' + pivot + u'~~~' + target
							sptlist.append(obj)
							allsrc.append(source)

	print 'Right: Combinations extracted in ' + str(time.time()-starttime) + ' secs\n'

	allsrcl = list(set(allsrc))
	sptl = list(set(sptlist))
	data =  [x.split(u'~~~') for x in sptl]

	print 'Right: ' + str(len(data)) + ' distinct src-piv-tgt combinations, '+ str(len(allsrcl)) + ' distinct source phrases'

	print '\nRight: Generated the list'

	spdict = {}
	stdict = {}
	ptdict = {}

	starttime = time.time()

	for l in data:

		try:
			spdict[l[0]][l[1]] = {}
		except:
			spdict[l[0]] = {l[1]: {}}

		try:
			stdict[l[0]][l[2]] = True
		except:
			stdict[l[0]] = {l[2]: True}

		try:
			ptdict[l[1]][l[2]] = 27*[0]
		except:
			ptdict[l[1]] = {l[2]: 27*[0]}

	print '\nRight: Intermediate dictionaries are created successfully'
	print 'Right: ' + str(len(spdict)) + ' : source phrases in spdict' 
	print 'Right: ' + str(len(stdict)) + ' : source phrases in stdict'
	print 'Right: ' + str(len(ptdict)) + ' : pivot phrases in spdict'

	tot = 0
	sources = spdict.keys()
	for source in sources:

			pivots = spdict[source].keys()
			for pivot in pivots:
			
				tmplist = list(set(ptdict[pivot]).intersection(stdict[source].keys()))
				tmpdict = {x:27*[0] for x in tmplist}
				spdict[source][pivot] = tmpdict
				tot += len(tmpdict)


	finalCount = spdict
	print 'Right: ' + str(len(finalCount)) + ' : source phrases in finalCount' 
	print 'Right: ' + str(tot) + ' : combinations in finalCount' 
	print '\nRight: Generated finalCount structure in ' + str(time.time()-starttime) + ' secs'

	rows = fstruct.keys()
	starttime = time.time()
	for row in rows:

		targets = fstruct[row].keys()
		for target in targets:

				pivots = fstruct[row][target].keys()
				for pivot in pivots:

				        sources = fstruct[row][target][pivot].keys()
				        for source in sources:
					
							finalCount[source][pivot][target] = map(sum, zip(finalCount[source][pivot][target], fstruct[row][target][pivot][source]))

	print 'Right: finalCounts updated in ' + str(time.time()-starttime) + ' secs'

	print '\nRight: Dumping dictionary containing counts in final format (source-phrase > pivot-phrase > target-phrase > [count-list])\n'
	with open('finalRightCountDict', "wb") as f2:
		pickle.dump(finalCount, f2)

	########################## Writing to file ##################################	
	
	file1 = codecs.open('finalRightCount', "w", "utf-8")
	sources = finalCount.keys()
	for source in sources:

		pivots = finalCount[source].keys()
		if(len(pivots) > 0):
			for pivot in pivots:

				targets = finalCount[source][pivot].keys()
				if(len(targets) > 0):
					for target in targets:

						string = ''+source+' | '+pivot+' | '+target+' |'
						for elem in finalCount[source][pivot][target]:
	
							string = string+' '+str(elem)
	
						string = string + '\n'
						file1.write(string)

	file1.close()
	
	del fstruct
	del finalCount



################################ MAIN CALL #################################################################

pstrans = pcorpus + '.toSource.validTrans'
tstrans = tcorpus + '.toSource.validTrans'
tptrans = tcorpus + '.toPivot.validTrans'

sl = scorpus+'.leftPhrases'
sr = scorpus+'.rightPhrases'
pl = pcorpus+'.leftPhrases'
pr = pcorpus+'.rightPhrases'
tr = tcorpus+'.rightPhrases'

finalstruct = 'finalStruct'
sdict = scorpus + '.validPhraseDict'
pdict = pcorpus + '.validPhraseDict'


pst = loadfiles(pstrans)
tst = loadfiles(tstrans)
tpt = loadfiles(tptrans)
sleft = loadfiles(sl)
sright = loadfiles(sr)
pleft = loadfiles(pl)
pright = loadfiles(pr)
tright = loadfiles(tr)
fstruct = loadfiles(finalstruct)
sd = loadfiles(sdict)
pd = loadfiles(pdict)

### NOt necessary
fs = fstruct


start = time.time()

calc_count(pst, tst, tpt, sleft, sright, pleft, pright, tright, fstruct, sd, pd)

print 'Right: Counts calculated for the given corpuses in '+str((time.time()-start))+' sec'


