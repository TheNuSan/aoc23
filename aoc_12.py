import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_12_0.txt"), "r").readlines()

def solve(pos, dam):
    leeway=len(pos) - (sum(dam)+len(dam)-1)
    if leeway<0:
        print("Error leeway computation")
        return 0
    if leeway==0:
        print(str(pos) + " " + str(1))
        return 1
    
    places=len(dam)+1
    
    #print(pos)
    #print(dam)
    #print(str(leeway) + " " + str(len(pos)) + " " + str(places))

    # we can then redistribute the leeway points in every place before, between or after the damage groups
    def combi(start, length, points):
        ret=[]
        for i in range(start,length):
            if points>1:
                ret += [[i]+(j if type(j) == list else [j]) for j in combi(i,length, points-1)]
            else:
                ret.append(i)
        #print(" - " + str(start) + " "+str(points) + " " + str(ret))
        return ret
    
    counter=0
    lst=combi(0,places,leeway)
    #print(lst)
    for c in lst:
        st=""
        for j in range(places):
            pc= c.count(j) if type(c) == list else (1 if c==j else 0)
            st+=''.join(['.' for x in range(pc)])
            if j>0 and j<places-1:
                st+="."
            if j<len(dam):
                st+=''.join(['#' for x in range(dam[j])])
        if len(st) != len(pos):
            print("Error len of pos")
            return
        valid=True
        for i,c in enumerate(pos):
            if c!="?" and c!=st[i]:
                valid=False
                break
        if valid:
            counter+=1
            #print(("VALID : " if valid else "INVALID : ") + str(st))
    print(str(pos) + " " + str(counter))
    return counter

def part1(l):
    p=l.split()
    pos=p[0]
    dam=[int(x) for x in p[1].split(",")]
    return solve(pos, dam)

print("Part 1: "+str(sum(map(part1, lines))))

# let's test brute force part 2
def part2(l):
    p=l.split()
    pos=p[0]
    dam=[int(x) for x in p[1].split(",")]
    mult=5
    pos2="?".join(pos for i in range(mult))
    dam2=[]
    for i in range(mult):
        dam2 += dam
    print(pos2 + " " + str(dam2))
    return solve(pos2, dam2)

# no
print("Part 2: "+str(sum(map(part2, lines))))