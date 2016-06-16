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

import sys,codecs,pickle,time,shelve

def printusage() :
    print 'Enter exactly as follows. \nUsage : '+sys.argv[0]+' <sourcePivotDict> <TargetPivotDict> <pivotTargetDict> <file-name-to-store-results> <section-number-of-dist-source-phrase-file> <triangulation-method> <(optional)-tringulated-phrase-table-Dictionary> \nChoices for Triangulation Method : \n0 - Table Based  \n1 - Count Based (Basic) \n2 - Count Based (Paraphrase)'


def decide(s,p,t):
	ret = [0]
	try:
		if(leftCount[s][p][t] and rightCount[s][p][t]):
			ret[0] = 1
			ret.append([leftCount[s][p][t],rightCount[s][p][t],totLeftCount[s][p][t],totRightCount[s][p][t]])
	except:
		pass	
	
	return ret			

###################################### Functions for core calculations of probabilities ####################################

################################# Count Based Calculations ###########################################3

############### Monotone and Reverse Monotone ###################

def calcMonotoneC(prob1, prob2, valueArray, totValueArray) :
		
	orientation = 0
	sum = 0
	
	for j in range(0,3):
		for i in range(0,3):
			num = valueArray[9*j + 3*i + orientation]
			if (num == 0):
				continue
			else:
				den = totValueArray[3*j + i]						
				coeff = float(num)/den									
				sum = sum + coeff*prob2[j]*prob1[i]				

	return sum

def calcRMonotoneC(prob1, prob2,  valueArray, totValueArray) :
	
	orientation = 0
	sum = 0
	
	for j in range(3,6):
		for i in range(3,6):
			num = valueArray[9*(j-3) + 3*(i-3) + orientation]							
			if (num == 0):										
				continue
			else:
				den = totValueArray[3*(j-3) + (i-3)]						
				coeff = float(num)/den								
				sum = sum + coeff*prob2[j]*prob1[i]				

	return sum

#################### Swap and Reverse Swap #######################

def calcSwapC(prob1, prob2, valueArray, totValueArray) :
	
	orientation = 1
	sum = 0
	
	for j in range(0,3):
		for i in range(0,3):
			num = valueArray[9*j + 3*i + orientation]							
			if (num == 0):										
				continue
			else:
				den = totValueArray[3*j + i]						
				coeff = float(num)/den									
				sum = sum + coeff*prob2[j]*prob1[i]				

	return sum

def calcRSwapC(prob1, prob2, valueArray, totValueArray) :
	
	orientation = 1
	sum = 0
	
	for j in range(3,6):
		for i in range(3,6):
			num = valueArray[9*(j-3) + 3*(i-3) + orientation]	
			if (num == 0):										
				continue
			else:
				den = totValueArray[3*(j-3) + (i-3)]			
				coeff = float(num)/den							
				sum = sum + coeff*prob2[j]*prob1[i]				
	return sum

#################### Discontinuous and Reverse Discontinuous ###################

def calcDisC(prob1, prob2, valueArray, totValueArray) :
	
	orientation = 2
	sum = 0
	
	for j in range(0,3):
		for i in range(0,3):
			num = valueArray[9*j + 3*i + orientation]
			if (num == 0):							
				continue
			else:
				den = totValueArray[3*j + i]		
				coeff = float(num)/den				
				sum = sum + coeff*prob2[j]*prob1[i]		

	return sum

def calcRDisC(prob1, prob2, valueArray, totValueArray) :
	
	orientation = 2
	sum = 0
	
	for j in range(3,6):
		for i in range(3,6):			
			num = valueArray[9*(j-3) + 3*(i-3) + orientation]
			if (num == 0):									
				continue
			else:
				den = totValueArray[3*(j-3) + (i-3)]		
				coeff = float(num)/den						
				sum = sum + coeff*prob2[j]*prob1[i]			

	return sum

######################################### Main code starts ##############################################

if(len(sys.argv) != 7 and len(sys.argv) != 8) :
    printusage()
    exit(1)

spd = sys.argv[1]
tpd = sys.argv[2]
ptd = sys.argv[3]
resultFile = sys.argv[4]
sec = int(sys.argv[5])
method = int(sys.argv[6])
triDictName=''
if(len(sys.argv) == 8):
	triDictName = sys.argv[7]

print 'The method being used is ' + str(method)

####################################### Loading Pre-Made Dictionaries ########################################## 

print 'Loading Source-Pivot Dictionary ...'

with open(spd, "rb") as myFile1:
    spDict = pickle.load(myFile1)

print 'Loading Pivot-Target Dictionary ...'

with open(ptd, "rb") as myFile1:
    ptDict = pickle.load(myFile1)

print 'Loading Target-Pivot Dictionary ...'

with open(tpd, "rb") as myFile2:
    tpDict = pickle.load(myFile2)

###################### Loading Count Dictionaries only in case of Count based or Back off model #####################

if(method == 1):

	print 'Loading Count Dictionaries ...'

	leftCount = shelve.open("finalLeftCountDictShelve")
	rightCount = shelve.open("finalRightCountDictShelve")
	totLeftCount = shelve.open("totalLeftCountDictShelve")
	totRightCount = shelve.open("totalRightCountDictShelve")
	
	print 'Count Dictionaries Loaded'

if(method == 2):

	print 'Loading Count Dictionaries ...'

	leftCount = shelve.open("paraphrasefinalLeftCountDictShelve")
	rightCount = shelve.open("paraphrasefinalRightCountDictShelve")
	totLeftCount = shelve.open("paraphrasetotalLeftCountDictShelve")
	totRightCount = shelve.open("paraphrasetotalRightCountDictShelve")
	
	print 'Count Dictionaries Loaded'

if(len(sys.argv) == 8):
	with open(triDictName, "rb") as f1:
		triDict = pickle.load(f1) 

######################################## Merging Logic Starts ##############################################################
	
######################################## Core Logic ####################################################

file1 = codecs.open(resultFile, "w", "utf-8")

totalSrc = str(len(triDict))

count = 0

refArray = [0,0,0,0,0,0,0,0,0]

ctrTableP = 0
ctrTableA = 0
ctrCount = 0
ctrprint = 0
ctrPrune = 0
ctrComb = 0

strttime = time.time()

sources = triDict.keys()
for s in sources:

	try:
		if(spDict[s]): 	

			targets = triDict[s].keys()
			for t in targets:

				try:
					if(tpDict[t]):

						pivPaths = 0
						pivots = spDict[s].keys()
						for p in pivots:

							try:
								if(tpDict[t][p]):
		
									ctrComb += 1
									pivPaths += 1
									finalProb = [0,0,0,0,0,0]

									inSrc = s
									inSrc = inSrc.encode('utf8')
									inPiv = p
									inTar = t
							
									try:					
										prob1 = spDict[s][p]
										prob2 = ptDict[p][t]
							
										############### Table Based Calculations ##################

										if(method == 0):												
											finalProb[0] = finalProb[0] + prob1[0]*prob2[0] + (prob1[1]*prob2[1])/2 + (prob1[1]*prob2[2])/2 + (prob1[2]*prob2[1])/3 + (prob1[2]*prob2[2])/3
											finalProb[1] = finalProb[1] + (prob1[0]*prob2[1])/2 + (prob1[0]*prob2[2])/2 + (prob1[1]*prob2[0]) + (prob1[2]*prob2[1])/3 + (prob1[2]*prob2[2])/3
											finalProb[2] = finalProb[2] + (prob1[0]*prob2[1])/2 + (prob1[0]*prob2[2])/2 + (prob1[1]*prob2[1])/2 + (prob1[1]*prob2[2])/2 + (prob1[2]*prob2[0]) + (prob1[2]*prob2[1])/3 + (prob1[2]*prob2[2])/3
											finalProb[3] = finalProb[3] + prob1[3]*prob2[3] + (prob2[4]*prob1[4])/2 + (prob2[4]*prob1[5])/2 + (prob2[5]*prob1[4])/3 + (prob2[5]*prob1[5])/3
											finalProb[4] = finalProb[4] + (prob1[3]*prob2[4])/2 + (prob1[3]*prob2[5])/2 + (prob1[4]*prob2[3]) + (prob1[5]*prob2[4])/3 + (prob1[5]*prob2[5])/3
											finalProb[5] = finalProb[5] + (prob1[3]*prob2[4])/2 + (prob1[3]*prob2[5])/2 + (prob1[4]*prob2[4])/2 + (prob1[4]*prob2[5])/2 + (prob1[5]*prob2[3]) + (prob1[5]*prob2[4])/3 + (prob1[5]*prob2[5])/3

										############### Count Based Calculations ##################										
										
										elif(method == 1 or method == 2):
											present = decide(inSrc,inPiv,inTar)
											if (present[0] == 1):

												valueArrayLeft = present[1][0]
												valueArrayRight = present[1][1]
												totValueArrayLeft = present[1][2]
												totValueArrayRight = present[1][3]																	

												if (totValueArrayLeft == refArray):
													finalProb[0] = finalProb[0] + prob1[0]*prob2[0] + (prob1[1]*prob2[1])/2 + (prob1[1]*prob2[2])/2 + (prob1[2]*prob2[1])/3 + (prob1[2]*prob2[2])/3
													finalProb[1] = finalProb[1] + (prob1[0]*prob2[1])/2 + (prob1[0]*prob2[2])/2 + (prob1[1]*prob2[0]) + (prob1[2]*prob2[1])/3 + (prob1[2]*prob2[2])/3
													finalProb[2] = finalProb[2] + (prob1[0]*prob2[1])/2 + (prob1[0]*prob2[2])/2 + (prob1[1]*prob2[1])/2 + (prob1[1]*prob2[2])/2 + (prob1[2]*prob2[0]) + (prob1[2]*prob2[1])/3 + (prob1[2]*prob2[2])/3
													ctrTableP = ctrTableP + 0.5
												else :
													finalProb[0] = finalProb[0] + calcMonotoneC(prob1,prob2,valueArrayLeft,totValueArrayLeft)
													finalProb[1] = finalProb[1] + calcSwapC(prob1,prob2,valueArrayLeft,totValueArrayLeft)
													finalProb[2] = finalProb[2] + calcDisC(prob1,prob2,valueArrayLeft,totValueArrayLeft)
													ctrCount = ctrCount + 0.5

												if (totValueArrayRight == refArray):
													finalProb[3] = finalProb[3] + prob1[3]*prob2[3] + (prob2[4]*prob1[4])/2 + (prob2[4]*prob1[5])/2 + (prob2[5]*prob1[4])/3 + (prob2[5]*prob1[5])/3
													finalProb[4] = finalProb[4] + (prob1[3]*prob2[4])/2 + (prob1[3]*prob2[5])/2 + (prob1[4]*prob2[3]) + (prob1[5]*prob2[4])/3 + (prob1[5]*prob2[5])/3
													finalProb[5] = finalProb[5] + (prob1[3]*prob2[4])/2 + (prob1[3]*prob2[5])/2 + (prob1[4]*prob2[4])/2 + (prob1[4]*prob2[5])/2 + (prob1[5]*prob2[3]) + (prob1[5]*prob2[4])/3 + (prob1[5]*prob2[5])/3
													ctrTableP = ctrTableP + 0.5
												else :
													finalProb[3] = finalProb[3] + calcRMonotoneC(prob1,prob2,valueArrayRight,totValueArrayRight)
													finalProb[4] = finalProb[4] + calcRSwapC(prob1,prob2,valueArrayRight,totValueArrayRight)
													finalProb[5] = finalProb[5] + calcRDisC(prob1,prob2,valueArrayRight,totValueArrayRight)
													ctrCount = ctrCount + 0.5
											else:
												finalProb[0] = finalProb[0] + prob1[0]*prob2[0] + (prob1[1]*prob2[1])/2 + (prob1[1]*prob2[2])/2 + (prob1[2]*prob2[1])/3 + (prob1[2]*prob2[2])/3
												finalProb[1] = finalProb[1] + (prob1[0]*prob2[1])/2 + (prob1[0]*prob2[2])/2 + (prob1[1]*prob2[0]) + (prob1[2]*prob2[1])/3 + (prob1[2]*prob2[2])/3
												finalProb[2] = finalProb[2] + (prob1[0]*prob2[1])/2 + (prob1[0]*prob2[2])/2 + (prob1[1]*prob2[1])/2 + (prob1[1]*prob2[2])/2 + (prob1[2]*prob2[0]) + (prob1[2]*prob2[1])/3 + (prob1[2]*prob2[2])/3
												finalProb[3] = finalProb[3] + prob1[3]*prob2[3] + (prob2[4]*prob1[4])/2 + (prob2[4]*prob1[5])/2 + (prob2[5]*prob1[4])/3 + (prob2[5]*prob1[5])/3
												finalProb[4] = finalProb[4] + (prob1[3]*prob2[4])/2 + (prob1[3]*prob2[5])/2 + (prob1[4]*prob2[3]) + (prob1[5]*prob2[4])/3 + (prob1[5]*prob2[5])/3
												finalProb[5] = finalProb[5] + (prob1[3]*prob2[4])/2 + (prob1[3]*prob2[5])/2 + (prob1[4]*prob2[4])/2 + (prob1[4]*prob2[5])/2 + (prob1[5]*prob2[3]) + (prob1[5]*prob2[4])/3 + (prob1[5]*prob2[5])/3	
												ctrTableA = ctrTableA + 1
							
									except Exception as e:
										print str(ctrprint)
										ctrprint +=1
										sys.exit()
										pass

							except:
								continue
		
						outString = ''+ s.strip()+ ' ||| ' + t.strip()+' |||'

						for i in range(0,6):
							if (pivPaths>0) :
								finalProb[i] = finalProb[i]/pivPaths
							outString = outString+ ' '+ str(finalProb[i])

						outString = outString+'\n'
						file1.write(outString)

				except:
					continue
	except:
		continue

	count = count + 1
	if(count%500 == 0):
		print 'Source phrase No. :'+str(count)+'/'+totalSrc+' time: '+str(time.time()-strttime)+': '+s
		if (method == 1 or method == 2):			
			print 'TableA : ' + str(ctrTableA) + '\t TableP : ' + str(ctrTableP) + '\t Count : ' + str(ctrCount)
		strttime = time.time()

		
print '\nReordering is completed started writing to the file --> reordering-table\n'

print '\nTotal source-target combinations generated : ' + str(ctrComb)

print '\nTriangulated Table has ' + str(len(triDict)) + ' entries'

file1.close()

if(method == 1 or method == 2):
	leftCount.close()
	rightCount.close()
	totLeftCount.close()
	totRightCount.close()


if (method == 1 or method == 2):
	print '\n##################### Process Statistics ######################'
	print '\n Total Count Based Calculations : ' + str(ctrCount)
	print '\n Total Table Based Calculations Due to s-p-t combination absent in Count Dictionary : ' + str(ctrTableA)
	print '\n Total Table Based Calculations Due to s-p-t combination present but all 27 values 0 : ' + str(ctrTableP)
	perc = (float(ctrTableP+ctrTableA)/(ctrTableP+ctrTableA+ctrCount))*100
	print '\n Percentage Backoff : ' + str(perc) + '%'

