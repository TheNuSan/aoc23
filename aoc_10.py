import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_10_1.txt"), "r").readlines()

spy,spx=[(i,l.find("S")) for i,l in enumerate(lines) if "S" in l][0]

def find_next(px,py,x,y):
    c=lines[y][x]
    #print(c)
    if c=="|": return x,y+(1 if py<y else -1)
    if c=="-": return x+(1 if px<x else -1),y
    if c=="L": return (x+1,y) if py<y else (x,y-1)
    if c=="J": return (x-1,y) if py<y else (x,y-1)
    if c=="7": return (x-1,y) if py>y else (x,y+1)
    if c=="F": return (x+1,y) if py>y else (x,y+1)
    print("Unknowk tile found: "+c)

starts=[]
Spipe1=False
Spipe2=False
if spx>0 and lines[spy][spx-1] in "-LF": starts.append((spx-1,spy))
if spy>0 and lines[spy-1][spx] in "|7F":
    starts.append((spx,spy-1))
    Spipe1=True
if spx<len(lines[0])-1 and lines[spy][spx+1] in "-7J": starts.append((spx+1,spy))
if spy<len(lines)-1 and lines[spy+1][spx] in "|LJ":
    starts.append((spx,spy+1))
    Spipe2=True

# if the two paths are above and below, S will be considered similar to a |
# this is needed for second part
isSpipe=Spipe1 and Spipe2

paths=[]

def find_path(prevx,prevy,bx,by):
    paths.append((bx,by))
    while True:
        nx,ny=find_next(prevx,prevy,bx,by)
        if (nx,ny) in paths:
            return
        paths.append((nx,ny))
        prevx,prevy=bx,by
        bx,by=nx,ny

paths.append((spx,spy))
find_path(spx,spy,starts[0][0],starts[0][1])
# no need to follow the second path, as it's a loop
#find_path(spx,spy,starts[1][0],starts[1][1])

print(str(spx) + " " + str(spy))
#print(paths)
print("Part 1: " + str(int(len(paths)/2)))

# part 2 is pretty ugly...

gx,gy=len(lines[0])-1,len(lines)
print("Grid: "+str(gx)+" "+str(gy))
counter=0
for y in range (gy):
    deep=0
    curline=list(lines[y])
    lastcomp=""
    for x in range(gx):
        if (x,y) in paths:
            c = curline[x]
            # search for mixed bend that indicate a vertical separation
            if c == "J" and lastcomp=="F": deep+=1
            if c == "7" and lastcomp=="L": deep+=1
            if c in "LJF7": lastcomp=c
            if c == "|": deep += 1
            if isSpipe and c == "S": deep += 1
        else:
            if deep%2==1:
                curline[x]="."
                counter += 1
            else:
                curline[x]=" "
            #curline[x]=str(deep)
    ''' curline[0]=str(int(y/100)%10)
    curline[1]=str(int(y/10)%10)
    curline[2]=str(y%10)
    curline[3]=' ' '''
    lines[y]="".join(curline)

sss=''.join(lines)
#print(sss.translate(str.maketrans('LJF7-|', '└┘┌┐─│')))
#print(sss) # why does it stop after half the lines? it's visual code
#for i,l in enumerate(lines): print("{:03d}".format(i) + str(l.removesuffix("\n")))
for i,l in enumerate(lines): print(l.removesuffix("\n").translate(str.maketrans('LJF7-|', '└┘┌┐─│')))
print("Part 2: "+str(counter))

