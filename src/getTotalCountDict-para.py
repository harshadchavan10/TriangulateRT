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
    print 'Enter exactly as follows. \nUsage : '+sys.argv[0]+' <name-of-count-dictionary> <file-toStore-TotalCountDictionary>' 

def computeTotal(valueArray):
	total = []
	
	sum = 0
	for i in range(0,len(valueArray)):
		sum = sum + valueArray[i]		
		if(i % 3 == 2):
			total.append(sum)
			sum = 0
	
	return total

########################## Main Code Starts ###############################

if(len(sys.argv) != 3) :
    printusage()
    exit(1)

srcDictName = sys.argv[1]
tarDictName = sys.argv[2]
srcDictTempName = srcDictName + 'Shelve'

######## Loading Count Dictionary ##########

print 'Loading Count Dictionary ...\n'

startLoad = time.time()

with open(srcDictName, "rb") as myFile1:
    srcDict = pickle.load(myFile1)

print 'Loading Time : '+ str(time.time()-startLoad) + ' seconds\n'

############################################# Processing the Dictionary Entry by Entry ######################################

finalDict = shelve.open(tarDictName)
countDict = shelve.open(srcDictTempName)

print 'Processing the Count Dictionary ...\n'

ctr = 0

totalLen = len(srcDict)

startProc = time.time()

start = time.time()

for s,dict1 in srcDict.iteritems():
	
	temp11 = {}
	temp12 = {}
	
	for p,dict2 in dict1.iteritems():

		temp21 = {}
		temp22 = {}
		
		for t,valueArray in dict2.iteritems():
			
			temp21[t] = computeTotal(valueArray[0])	
			temp22[t] = valueArray[0]	
			
		temp11[p] = temp21
		temp12[p] = temp22

	s = s.encode('utf8')
	finalDict[s] = temp11
	countDict[s] = temp12
	ctr = ctr + 1
	if(ctr % 100000 == 0):
		print 'Source phrase No. :'+str(ctr)+'/'+str(totalLen)+' time: '+str(time.time()-start)+': '+s
		start = time.time()				

print 'Total Processing Time : '+str(time.time()-startProc) + ' seconds\n'

print 'Dumping the Total Count Dictionary ...'

finalDict.close()
countDict.close()

print tarDictName+' was created Successfully!!!'
print srcDictTempName+' was created Successfully!!!'
