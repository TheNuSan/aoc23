import os
import sys
import re
from functools import reduce
from math import prod

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_03_1.txt"), "r").readlines()
'''
lines = ["467..114.."
        ,"...*......"
        ,"..35..633."
        ,"......#..."
        ,"617*......"
        ,".....+.58."
        ,"..592....."
        ,"......755."
        ,"...$.*...."
        ,".664.598.."]
#'''

def issymbol(v):
    return not (v.isdigit() or v==".")

def code1(line, prev, next):
    sm=0
    i=0
    while i<len(line):
        value=0
        vmin=max(0,i-1)
        while i<len(line) and line[i].isdigit():
            value=value*10+int(line[i])
            i+=1
        vmax=min(i,len(line)-1)
        i+=1
        if value>0:
            ispart=False
            if prev and any(issymbol(prev[y]) for y in range(vmin, vmax+1)): ispart=True
            if next and any(issymbol(next[y]) for y in range(vmin, vmax+1)): ispart=True
            if vmin>0 and issymbol(line[vmin]): ispart=True
            if vmax<len(line)-1 and issymbol(line[vmax]): ispart=True
            if ispart:
                sm+=value
    return sm

#clean return at ends of lines, as it would be considered symbols
for i in range(len(lines)): lines[i]=lines[i].removesuffix("\n")

# for part 1, lets directly read lines + previous/next and find symbol like that
print("Part 1: "+str(sum(code1(v, lines[id-1] if id>0 else None, lines[id+1] if id<len(lines)-1 else None) for id,v in enumerate(lines))))

# for part 2, lets make it more clear with a "proper" global array of values, so we can easily search around gears
tab={}
for y,line in enumerate(lines):
    i=0
    while i<len(line):
        value=0
        vmin=i
        while i<len(line) and line[i].isdigit():
            value=value*10+int(line[i])
            i+=1
        vmax=min(i-1,len(line)-1)
        i+=1
        if value>0:
            ob=(value,vmin,y)
            for k in range(vmin, vmax+1):
                tab[(k,y)]=ob

part2=0
for y,line in enumerate(lines):
    for x,v in enumerate(line):
        if v=="*":
            nei=[]
            for a in range(-1,2):
                for b in range(-1,2):
                    pos=(x+a,y+b)
                    if (a!=0 or b!=0) and pos in tab: nei.append(tab[pos])
            nei=set(nei)
            if len(nei)==2:
                part2 += prod(v[0] for v in nei)
            #print(str(nei))
print("Part 2: "+str(part2))

#print(str(tab))


