import os
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_21_1.txt"), "r").read().split("\n")
map=[[c!='#' for c in l] for l in lines]
gridx,gridy=len(map[0]),len(map)
startx,starty=next((i,l.index('S')) for i,l in enumerate(lines) if 'S' in l)

print('\n'.join(''.join('_' if y else "M" for y in x) for x in map))
print(gridx,gridy)
print(startx,starty)

# Part 1:
cur=set()
cur.add((startx,starty))
for x in range(50):
    nextcur=set()
    for p in cur:
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            npx,npy=p[0]+dx,p[1]+dy
            if npx<0 or npx>=gridx or npy<0 or npy>=gridy: continue
            if map[npy][npx]:
                nextcur.add((npx,npy))
    cur=nextcur
print(len(cur))
