import os
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_22_1.txt"), "r").read().split("\n")

vrac=[[[int(x) for x in c.split(',')] for c in l.split('~')] for l in lines]
gridx=max(max(b[0][0],b[1][0]) for b in vrac)+1
gridy=max(max(b[0][1],b[1][1]) for b in vrac)+1
gridz=max(max(b[0][2],b[1][2]) for b in vrac)+1
print(gridx,gridy,gridz)
blocks=sorted(vrac, key=lambda x: min(x[0][2],x[1][2]))
names="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
def print_side():
    bp=[['-' if z==gridz-1 else '.' for x in range(gridx)] for z in range(gridz)]
    for i,b in enumerate(blocks):
        sx,ex=min(b[0][0],b[1][0]),max(b[0][0],b[1][0])
        sy,ey=min(b[0][1],b[1][1]),max(b[0][1],b[1][1])
        sz,ez=min(b[0][2],b[1][2]),max(b[0][2],b[1][2])
        
        bx,nx=sx,ex
        #bx,nx=sy,ey
        for x in range(bx,nx+1):
            for z in range(sz,ez+1):
                bp[gridz-z-1][x]=names[i%26]
    print('\n'.join(''.join(x) for x in bp))

heightmap=[[[0,None] for x in range(gridx)] for y in range(gridy)]
support=[]
for i,b in enumerate(blocks):
    sx,ex=min(b[0][0],b[1][0]),max(b[0][0],b[1][0])
    sy,ey=min(b[0][1],b[1][1]),max(b[0][1],b[1][1])
    sz,ez=min(b[0][2],b[1][2]),max(b[0][2],b[1][2])
    curz=0
    for x in range(sx,ex+1):
        for y in range(sy,ey+1):
            curz=max(curz,heightmap[y][x][0])
    
    dz=sz-curz-1
    b[0][2]-=dz
    b[1][2]-=dz
    suplist=[]
    for x in range(sx,ex+1):
        for y in range(sy,ey+1):
            hm=heightmap[y][x]
            if hm[1] and hm[0]==sz-dz-1 and not hm[1] in suplist:
                suplist.append(hm[1])
            heightmap[y][x] = [ez-dz,b]
    support.append(suplist)

print(blocks)
print(heightmap)

candestroy=0
supporter=[0 for x in support]
for i,b in enumerate(support):
    if len(b)==1:
        for x in b:
            supporter[blocks.index(x)]+=1

print_side()
for i,b in enumerate(support):
    print(names[i%26],', '.join(names[blocks.index(x)%26] for x in b))

print(', '.join(names[i%26]+"="+str(x) for i,x in enumerate(supporter)))

print(len([1 for x in supporter if x==0]))