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

# Part 1, just straightforward push
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

# Part 2:
# only iterate on the particles, not the whole board
# use a dictionnary for the colision detection
gridx,gridy=len(puzzle[0]),len(puzzle)
# map of rocks:
occu={(i,j):[(i,j),'#'] for j,p in enumerate(puzzle) for i,c in enumerate(p) if c=='#'}

# to speed up, compute the distance to the next rock in each direction
dist_north=[[min(j,next((max(0,k-1) for k in range(gridy) if (i,j-k) in occu),j)) for i in range(gridx)] for j in range(gridy)]
dist_south=[[min(gridy-j-1,next((max(0,k-1) for k in range(gridy) if (i,j+k) in occu),gridy-j-1)) for i in range(gridx)] for j in range(gridy)]
dist_west=[[min(i,next((max(0,k-1) for k in range(gridx) if (i-k,j) in occu),i)) for i in range(gridx)] for j in range(gridy)]
dist_east=[[min(gridx-i-1,next((max(0,k-1) for k in range(gridx) if (i+k,j) in occu),gridx-i-1)) for i in range(gridx)] for j in range(gridy)]

#print("\n".join(["".join([str(i) for i in j]) for j in dist_east]))

# create a particles for each O
parts=[[(i,j),'O'] for j,p in enumerate(puzzle) for i,c in enumerate(p) if c=='O']
# add the particles to the map
occu |= {p[0]:p for p in parts}

# this try to push a particle in a direction
# with this method, we don't keep the order of the particles
# but it's not needed for this puzzle, just where are particles
# the great benefit here is that we can update the particles in any order
def pushpart(p,distab,dx,dy):
    # get distance to next rock in the direction
    dist=distab[p[0][1]][p[0][0]]
    if dist<1:
        return
    # try to move directly to this position
    nk=(p[0][0]+dist*dx,p[0][1]+dist*dy)
    while dist>0:
        # if the position is free, we found our target
        if not nk in occu:
            break
        # if not, we got back a step and try again
        nk=(nk[0]-dx,nk[1]-dy)        
        dist-=1
    # if we moved at all
    if dist>0:
        # remove/re-insert the particle in the occupency map
        del occu[p[0]]
        p[0]=nk
        occu[p[0]]=p

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
        # get a hash of the particles position, to see if it was already reached before
        # if it did, it means we have a cycle, so we can stop
        # putting a sorted here did a x150 speedup has without it the cycle must get the particles in the same exact position, to it is much longer (~33k instead of ~170)
        ch=hash(tuple(p[0] for p in sorted(parts)))
        if ch in histo:
            debcycl=histo[ch]
            cycledur=i-debcycl
            print("Step",i,counter_2())
            # we found a repeating cycle!
            # we can just skip all the next cycles up to when we almost reach the 1B goal
            cycleleft=(goal-i)%cycledur-1
            print("Hash FOUND! cycle:",debcycl,"cycles left:",cycleleft,"total cycles:",i+cycleleft)
            # then we step the final few cycles left to reach the 1B goal
            for j in range(cycleleft):
                cycle()
                if j%100==0: print("Post cycle step",j)
            break
        histo[ch]=i
        if i%100==0: print("Step",i)

part2()

#print(parts)
#print(occu)
printmap()

print("Part 2:",counter_2())
print("       ",time.process_time()-t)
