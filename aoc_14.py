import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math
import time

t = time.process_time()

wd=os.path.dirname(os.path.realpath(__file__))
# read without the \n at the end
lines = open(os.path.join(wd,"aoc_14_1.txt"), "r").read().split("\n")
puzzle = [list(l) for l in lines]

def part1(puz):
    gridx,gridy=len(puz[0]),len(puz)
    for i in range(gridx):
        tar=0
        for j in range(gridy):
            c = puz[j][i]
            if c=="#":
                tar=j+1
            elif c=="O":
                if tar!=j:
                    puz[tar][i]=c
                    puz[j][i]="."
                tar+=1

def counter_1(puz):
    return sum([(len(puz)-i)*sum([1 for c in l if c=='O']) for i,l in enumerate(puz)])

#part1(puzzle)
#print("Part 1:",counter_1(puzzle))

# for part 2:
gridx,gridy=len(puzzle[0]),len(puzzle)
# map of rocks:
occu={(i,j):[(i,j),'#'] for j,p in enumerate(puzzle) for i,c in enumerate(p) if c=='#'}

dist_north=[[min(j,next((max(0,k-1) for k in range(gridy) if (i,j-k) in occu),j)) for i in range(gridx)] for j in range(gridy)]
dist_south=[[min(gridy-j-1,next((max(0,k-1) for k in range(gridy) if (i,j+k) in occu),gridy-j-1)) for i in range(gridx)] for j in range(gridy)]
dist_west=[[min(i,next((max(0,k-1) for k in range(gridx) if (i-k,j) in occu),i)) for i in range(gridx)] for j in range(gridy)]
dist_east=[[min(gridx-i-1,next((max(0,k-1) for k in range(gridx) if (i+k,j) in occu),gridx-i-1)) for i in range(gridx)] for j in range(gridy)]

#print("\n".join(["".join([str(i) for i in j]) for j in dist_east]))

# add particles
parts=[[(i,j),'O'] for j,p in enumerate(puzzle) for i,c in enumerate(p) if c=='O']
occu |= {p[0]:p for p in parts}

def pushpart(p,distab,dx,dy):
    dist=distab[p[0][1]][p[0][0]]
    if dist<1:
        return
    nk=(p[0][0]+dist*dx,p[0][1]+dist*dy)
    while dist>0:
        if not nk in occu:
            break
        nk=(nk[0]-dx,nk[1]-dy)        
        dist-=1
    if dist>0:
        del occu[p[0]]
        p[0]=nk
        occu[p[0]]=p

def push(i,j,dx,dy):
    nk=(i,j)
    if nk not in occu:
        return
    p=occu[nk]
    if p[1]!='O':
        return
    del occu[nk]
    while True:
        nk=(nk[0]+dx,nk[1]+dy)
        if nk[0]<0 or nk[0]>=gridx or nk[1]<0 or nk[1]>=gridy:
            break
        if nk in occu:
            break
        p[0]=nk
    occu[p[0]]=p

def push_north():
    for i in range(gridx):
        for j in range(gridy):
            push(i,j,0,-1)

def push_south():
    for i in range(gridx):
        for j in range(gridy-1,-1,-1):
            push(i,j,0,1)

def push_east():
    for j in range(gridy):
        for i in range(gridx-1,-1,-1):
            push(i,j,1,0)

def push_west():
    for j in range(gridy):
        for i in range(gridx):
            push(i,j,-1,0)

def cycle_old():
    push_north()
    push_west()
    push_south()
    push_east()

def cycle():
    for p in parts: pushpart(p,dist_north,0,-1)
    for p in parts: pushpart(p,dist_west,-1,0)
    for p in parts: pushpart(p,dist_south,0,1)
    for p in parts: pushpart(p,dist_east,1,0)

def counter_2():
    return sum((gridy-j) for j in range(gridy) for i in range(gridx) if (i,j) in occu and occu[(i,j)][1]=='O')
    
def printmap():
    print("----------------")
    print("\n".join(["".join([occu[(i,j)][1] if (i,j) in occu else "." for i in range(gridx)]) for j in range(gridy)]))

#print(hash(tuple(tuple(p) for p in parts)))

def part2():
    histo={}
    goal=1000000000
    for i in range(goal):
        cycle()
        ch=hash(tuple(p[0] for p in sorted(parts)))
        if ch in histo:
            debcycl=histo[ch]
            cycledur=i-debcycl
            print("Step",i,counter_2())
            # we found a repeating cycle!
            cycleleft=(goal-i)%cycledur-1
            print("Hash FOUND! cycle:",debcycl,"cycles left:",cycleleft,"total cycles:",i+cycleleft)
            for j in range(cycleleft):
                cycle()
                if j%100==0: print("Post cycle step",j)
            break
        histo[ch]=i
        if i%100==0: print("Step",i)

part2()

#print(parts)
#print(occu)
#printmap()

print("Part 2:",counter_2())
print("       ",time.process_time()-t)
#print("\n".join([''.join(l) for l in puzzle]))
