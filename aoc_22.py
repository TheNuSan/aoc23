import os
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_22_1.txt"), "r").read().split("\n")

names="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
blockcounter=0

class Block:
    name="$"
    start=[]
    end=[]
    top=[]
    down=[]
    def __init__(self, start, end):
        global blockcounter
        self.name=names[blockcounter%len(names)]
        blockcounter+=1
        self.start=min(start,end)
        self.end=[x for x in max(start,end)] # we need to store a copy in case start==end
        self.top=[]
        self.down=[]
    def __str__(self):
        return self.name + " " + str(self.start) + " " + str(self.end)
    def __repr__(self):
        return self.name

vrac=[]
for l in lines:
    cc=[[int(x) for x in c.split(',')] for c in l.split('~')]
    vrac.append(Block(cc[0],cc[1]))

gridx=max(b.end[0] for b in vrac)+1
gridy=max(b.end[1] for b in vrac)+1
gridz=max(b.end[2] for b in vrac)+1
print(gridx,gridy,gridz)
blocks=sorted(vrac, key=lambda x: x.start[2])

#print(",".join(str(x) for x in blocks))

def print_side():
    bp=[['-' if z==gridz-1 else '.' for x in range(gridx)] for z in range(gridz)]
    for b in blocks:
        #bx,nx=b.start[0],b.end[0]
        bx,nx=b.start[1],b.end[1]
        for x in range(bx,nx+1):
            for z in range(b.start[2],b.end[2]+1):
                bp[gridz-z-1][x]=b.name
    print('\n'.join(''.join(x) for x in bp))

#print_side()

heightmap=[[[0,None] for x in range(gridx)] for y in range(gridy)]

for b in blocks:
    curz=0
    for x in range(b.start[0],b.end[0]+1):
        for y in range(b.start[1],b.end[1]+1):
            curz=max(curz,heightmap[y][x][0])
    
    dz=b.start[2]-curz-1
    b.start[2]-=dz
    b.end[2]-=dz

    for x in range(b.start[0],b.end[0]+1):
        for y in range(b.start[1],b.end[1]+1):
            hm=heightmap[y][x]
            if hm[1] and hm[0]==b.start[2]-1:
                if not hm[1] in b.down: b.down.append(hm[1])
                if not b in hm[1].top: hm[1].top.append(b)
            heightmap[y][x] = [b.end[2],b]

#print(blocks)
#print(heightmap)

print_side()
#for b in blocks: print(b.name,"->",', '.join(x.name for x in b.top))

# 386
# we can destroy any block that have nothing on top or where all top on blocks have more than 1 support 
candestroy=[b for b in blocks if len(b.top)==0 or all(len(f.down)>1 for f in b.top)]
#print(candestroy)
print(len(candestroy))

#'''