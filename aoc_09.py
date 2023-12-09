import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_09_1.txt"), "r").readlines()

histo = [[*map(int, l.split())] for l in lines]

def part1(x):
    diffs=[x]
    while any(y!=0 for y in diffs[-1]):
        prev = diffs[-1]
        diffs.append([prev[i+1]-prev[i] for i,v in enumerate(prev) if i<len(prev)-1])
    diffs[len(diffs)-1].append(0)
    for i in range(len(diffs)-2,-1,-1):
        diffs[i].append(diffs[i][-1] + diffs[i+1][-1])
    #print(diffs[0])
    return diffs[0][-1]

def part2(x):
    diffs=[x]
    while any(y!=0 for y in diffs[-1]):
        prev = diffs[-1]
        diffs.append([prev[i+1]-prev[i] for i,v in enumerate(prev) if i<len(prev)-1])
    diffs[len(diffs)-1].insert(0, 0)
    for i in range(len(diffs)-2,-1,-1):
        diffs[i].insert(0, diffs[i][0] - diffs[i+1][0])
    #print(diffs)
    return diffs[0][0]

#print('\n'.join(map(part1, histo)))
print("Part 1: " + str(sum(map(part1, histo))))
print("Part 2: " + str(sum(map(part2, histo))))