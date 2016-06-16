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
    print 'Enter exactly as follows. \nUsage : '+sys.argv[0]+' <name-of-table> <file-toStore-Dictionary> <no-of-lines>' 

########################## Main Code Starts ###############################

if(len(sys.argv) != 4) :
    printusage()
    exit(1)

tableName = sys.argv[1]
tarDictName = sys.argv[2]
tot = sys.argv[3]

tarDict = {}

print 'Processing the Phrase Table ...\n'

ctr = 0

start = time.time()

f1 = codecs.open(tableName,encoding='utf-8', errors="ignore")
for line in f1:
	temp = (line.split('|'))
	src = temp[0].strip()
	tar = temp[1].strip()
	ctr = ctr + 1
	try:
		tarDict[src][tar] = 1
	except:
		tarDict[src] = {tar:1}

	if (ctr % 100000 == 0):
		print 'Processed ' + str(ctr) + ' lines out of ' + str(tot) + ' Time: '+ str(time.time()-start)
		start = time.time()	
f1.close()

with open(tarDictName, "wb") as myfile1:
		pickle.dump(tarDict, myfile1)

print 'Dictionary created with name ' + tarDictName
