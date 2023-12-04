import os
import sys
import re
from functools import reduce
from math import prod

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_04_1.txt"), "r").readlines()
'''
lines = ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"
        ,"Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"
        ,"Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1"
        ,"Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83"
        ,"Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36"
        ,"Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"]
#'''

counter=[1] * len(lines)

def code1(id,line):
    tb=line.split(":")
    nb=tb[1].split("|")
    win=list(filter(lambda x: x!="",nb[0].split(" ")))
    card=list(filter(lambda x: x!="",nb[1].split(" ")))
    t=sum(1 for v in win if v in card)
    if t>0:
        for j in range(1,t+1):
            if id+j<len(counter):
                counter[id+j] += counter[id]
    r=int(pow(2,t-1))
    return r

#clean return at ends of lines
for i in range(len(lines)): lines[i]=lines[i].removesuffix("\n")

print("Part 1: "+str(sum(code1(id, line) for id,line in enumerate(lines))))
print("Part 2: "+str(sum(counter)))

