import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_11_1.txt"), "r").readlines()

# get stars and count number of stars per rows/cols
starcols={}
starrows={}
stars=[]
gridx,gridy=0,0
for i,l in enumerate(lines):
    gridy=max(gridy,i)
    for j,c in enumerate(l):
        if c=="#":
            stars.append([j,i])
            if not j in starcols: starcols[j]=0
            starcols[j]+=1
            if not i in starrows: starrows[i]=0
            starrows[i]+=1
        gridx=max(gridx,j)

# find gaps to be expanded
emptycols=[i for i in range(gridx) if not i in starcols]
emptyrows=[i for i in range(gridy) if not i in starrows]

print("Stars 1: " + str(stars))

#gap_mul = 1 # Part 1
gap_mul = 1000000-1 # Part 2

# push stars according to the gaps
for s in stars:
    px,py=0,0
    for i in emptycols:
        if i<s[0]: px+=1
    for j in emptyrows:
        if j<s[1]: py+=1
    s[0] += px*gap_mul
    s[1] += py*gap_mul

print("Empty cols: "+str(emptycols))
print("Empty rows: "+str(emptyrows))
print("Stars 2: " + str(stars))

def man_dist(s1, s2):
    return abs(s1[0]-s2[0]) + abs(s1[1]-s2[1])

# naive pair path counter:
dists = [man_dist(s1,s2) for i,s1 in enumerate(stars) if i>0 for j,s2 in enumerate(stars) if j<i]
print("Solution: " + str(sum(dists)))
