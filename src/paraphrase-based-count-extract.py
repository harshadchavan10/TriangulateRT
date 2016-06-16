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

def printusage():
	print 'Format : python '+sys.argv[0]+' <Left/Right>'

if(len(sys.argv)!=2):
	printusage()
	exit(1)

direction = sys.argv[1]


def loadfiles(name):
	print direction + ': ' + '<<< Loading '+name+' dictionary >>>'	
	starttime = time.time()
	dictionary = {}
	with open(name, "rb") as f1:
		dictionary = pickle.load(f1)
	print 'The dictionary loaded in '+str(time.time()-starttime)+' sec length = '+str(len(dictionary))+'\n\t\t-------------------------'
	return dictionary


def extractParaphrases(phrases, d1, d2, revd1, revd2):
	
	dictionary = {}
	d1k = d1.keys()
	d2k = d2.keys()
	cnt = 0

	for p in phrases:
		
		paraphrasel = []
	   
		try: 
			l1 = d1[p].keys()
			for p1 in l1:
				try:
					paraphrasel.extend(revd1[p1].keys()) 
				except:
					pass
		except:
			pass
		
		try:
			l2 = d2[p].keys()
			for p2 in l2:
				try:
					paraphrasel.extend(revd2[p1].keys()) 
				except:
					pass
		except:
			pass

		dictionary[p] = {x:True for x in list(set(paraphrasel))}
		cnt += 1
		
	return dictionary


def updateCounts(name, sp, ps, st, ts, pt, tp):
	
	finalCount = loadfiles(name)

	
	srcp = {}
	pivp = {}
	tgtp = {}
	total = 0   
	nonzero = 0
	refarray = 27*[0]
	
	sources = finalCount.keys()
	for source in sources:
		
		pivots = finalCount[source].keys()
		for pivot in pivots:
			
			targets = finalCount[source][pivot].keys()
			for target in targets:
				
				total +=1
				
				if(finalCount[source][pivot][target] == refarray):
					srcp[source] = True
					pivp[pivot] = True
					tgtp[target] = True
					finalCount[source][pivot][target] = [finalCount[source][pivot][target], False]
				else:
					nonzero += 1
					finalCount[source][pivot][target] = [finalCount[source][pivot][target], True]
							
	print direction + ': ' + "ORIGINAL COUNTS - " + name + "\n################################"
	print direction + ': ' + "Total lines in file : " + str(total)
	print direction + ': ' + "Total rows with non-zero counts : " + str(nonzero)
	print direction + ': ' + "Percentage of non-zero count rows : " + str(float(nonzero)/total*100)
	
	updated = 0
	allzero = total - nonzero

	srcl = srcp.keys()
	pivl = pivp.keys()
	tgtl = tgtp.keys()
	
	print direction + ': ' + "Paraphrase extraction is started for " + str(len(srcl)) + " Source pharses " + str(len(pivl)) + " Pivot pharses " + str(len(tgtl)) + " Target pharses " 

	sourceParaphrase = extractParaphrases(srcl, sp, st, ps, ts)
	print direction + ': ' + "Source Paraphrase extraction completed for " + name  

	pivotParaphrase = extractParaphrases(pivl, ps, pt, sp, tp)
	print direction + ': ' + "Pivot Paraphrase extraction completed for " + name 
	
	targetParaphrase = extractParaphrases(tgtl, ts, tp, st, pt)
	print direction + ': ' + "Target Paraphrase extraction completed for " + name

	del sp
	del st
	del pt
	del ps
	del ts
	del tp 

	### Extract counts using paraphrases #####
	
	cnt=0
	
	start = time.time()
	for source in srcl:
		
		pivots = finalCount[source].keys()
		for pivot in pivots:
			try:
				if(pivp[pivot]):
	
					targets = finalCount[source][pivot].keys()
					for target in targets:
		
						if(not finalCount[source][pivot][target][1]):
			
							flag = False
							srcs = sourceParaphrase[source].keys()
							for src in srcs:

								try:
									if(finalCount[src]):

										pivs = finalCount[src].keys()
										for piv in pivs:
											
											try:
												if(pivotParaphrase[pivot][piv]):

													tgts = finalCount[src][piv].keys()
													for tgt in tgts:

														try:
															if(targetParaphrase[target][tgt] and finalCount[src][piv][tgt][1]):
												
																flag = True
																finalCount[source][pivot][target][0] = map(sum, zip(finalCount[source][pivot][target][0], finalCount[src][piv][tgt][0]))
												
														except:
															continue
											except:
												continue
								except:
									continue
		
							if(flag):
								updated += 1
							cnt += 1
							if(cnt % 500 == 0):
								print direction + ': ' + str(cnt) + ' / '+ str(allzero) +' All zero combinations are processed, updated entries : ' + str(updated) + ', time : ' + str(time.time()-start)
								start = time.time()
			except:
				continue

	print direction + ': ' + "UPDATED COUNTS - " + name + "\n################################"
	print direction + ': ' + "Total lines in file : " + str(total)
	print direction + ': ' + "Counts extacted through paraphrasing for " + str(updated) + "/" + str(total-nonzero) + " all 27 0's rows."
	print direction + ': ' + "Thus, Total rows with non-zero counts : " + str(nonzero+updated)
	print direction + ': ' + "Percentage of non-zero count rows : " + str(float(nonzero+updated)/total*100) + '\n'
																							
	print direction + ': ' + 'Dumping dictionary containing counts in final format (source-phrase > pivot-phrase > target-phrase > [count-list])\n'
	with open('paraphrase' + name, "wb") as f2:
		pickle.dump(finalCount, f2)
	


if __name__ == '__main__':
	
	sp = loadfiles('sp-trans')
	ps = loadfiles('ps-trans')
	st = loadfiles('st-trans')
	ts = loadfiles('ts-trans')
	pt = loadfiles('pt-trans')
	tp = loadfiles('tp-trans')

	srcl = updateCounts('final'+direction+'CountDict', sp, ps, st, ts, pt, tp)

