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

f1 = codecs.open("finalLeftCount",encoding='utf-8', errors="ignore")
count = 0
gt = 0

for line in f1:
    temp = (line.split('|'))
    counts = sum(map(int, temp[3].strip().split(' ')))
    if(counts > 0):
        gt += 1
    count += 1

print "LEFT COUNTS\n################################"
print "Total lines in file : " + str(count)
print "Total rows with non-zero counts : " + str(gt)
print "Percentage of non-zero count rows : " + str(float(gt)/count*100)


f1 = codecs.open("finalRightCount",encoding='utf-8', errors="ignore")
count = 0
gt = 0

for line in f1:
    temp = (line.split('|'))
    counts = sum(map(int, temp[3].strip().split(' ')))
    if(counts > 0):
        gt += 1
    count += 1

print "RIGHT COUNTS\n################################"
print "Total lines in file : " + str(count)
print "Total rows with non-zero counts : " + str(gt)
print "Percentage of non-zero count rows : " + str(float(gt)/count*100)

