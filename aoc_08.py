import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_08_1.txt"), "r").readlines()

inst = lines[0].removesuffix("\n")

places = {x[0]:(x[1],x[2]) for x in (re.match("^(\w{3}) = \((\w{3}), (\w{3})\)$", l).groups() for l in lines[2:])}

def part_1():
    cur="AAA"
    instp=0
    instc=len(inst)
    steps=0
    while cur!="ZZZ":
        cur=places[cur][0 if inst[instp]=="L" else 1]
        steps+=1
        instp=(instp+1)%instc

    print("Part 1: " + str(steps))

def part_2():
    starts = [id for id in places.keys() if id.endswith('A')]
    instp=0
    instc=len(inst)
    steps=0
    print(starts)
    # brute force doesn't seems to work
    '''
    while True:
        starts=[places[x][0 if inst[instp]=="L" else 1] for x in starts]
        #print(starts)
        steps+=1
        if all(x.endswith('Z') for x in starts): break
        instp=(instp+1)%instc
    '''
    # lets compute cycle duration of each starts, then combine them
    cycles={}
    while True:
        starts=[places[x][0 if inst[instp]=="L" else 1] for x in starts]
        #print(starts)
        steps+=1
        if all(x.endswith('Z') for x in starts): break
        
        for i,x in enumerate(starts):
            if x.endswith('Z'):
                print(x)
                if i not in cycles: cycles[i] = []
                if not steps in cycles[i]:
                    print("Found new cycle for " + str(i) + " " + str(steps) + " steps")
                    cycles[i].append(steps)
        if len(cycles) == len(starts):
            # found a cycle for everyone, may not be the "best" set of cycles though
            break
        instp=(instp+1)%instc
    #print(starts)
    print("max steps: " + str(steps))
    print(cycles)
    instlen=len(inst)
    wins = {x:[int(j/instlen) for j in v if j%instlen==0] for x,v in cycles.items()}
    part2 = prod(v[0] for x,v in wins.items()) * instlen
    print(wins)
    print("instruction length: "+str(instlen))
    print("Part 2: " + str(part2))

#part_1()
part_2()


#hands = [[v if i%2==0 else int(v) for i,v in enumerate(l.split())] for l in lines]

