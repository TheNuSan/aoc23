import os
import math
from math import floor
from PIL import Image, ImageDraw

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_21_1.txt"), "r").read().split("\n")
map=[[c!='#' for c in l] for l in lines]
gridx,gridy=len(map[0]),len(map)
startx,starty=next((i,l.index('S')) for i,l in enumerate(lines) if 'S' in l)

#print('\n'.join(''.join('_' if y else "M" for y in x) for x in map))
print(gridx,gridy)
print(startx,starty)
startgridx,startgridy=gridx,gridy

# there is a large empty diamond at 64 steps from the start
# this is the key for it to be solvable at some specifics steps counts that can be arbitrarily large
# so after initial 64, each 131 steps give a full regular diamond of the map full
# so at each diamond, the amount of cells filled is not dependent of the exact path, but just on the size
# where everything is at same distance
# so next diamond is at 64 + 131 steps
#
# we cut the repeating square into 2 area, A and B 
# --------
# |B /\ B|
# | /  \ |
# |/  A \|
# |\    /|
# | \  / |
# |B \/ B|
# --------
#
# and each part A and B can be in two state, after an even number of steps or after an odd number of steps


# compute parts:
partAp = 0 # inside diamond, even
partAi = 0 # inside diamond, odd
partBp = 0 # outside diamond, even
partBi = 0 # outside diamond, odd

print("--------------------------")
diag=floor((gridx-1)/2)
for j,y in enumerate(map):
    for i,x in enumerate(y):
        if not map[j][i]: continue
        ri=abs(i-startx)
        rj=abs(j-starty)
        even=i%2==j%2
        partA=(ri+rj)<=diag
        if even:
            if partA:
                partAp+=1
            else:
                partBp+=1
        else:
            if partA:
                partAi+=1
            else:
                partBi+=1

# part B (either i or p) is one too much
# why????
partBi-=1

print("Part Ap",partAp)
print("Part Ai",partAi)
print("Part Bp",partBp)
print("Part Bi",partBi)

totalsteps=26501365
prevdiamond=floor((totalsteps-64)/131)
prevsteps=prevdiamond*131+64
print("prevdiamond",prevdiamond)
print("prevsteps:",prevsteps)
print("diff:",totalsteps-prevsteps)

# steps +1 to acount for the initial diamond
prevdiamond += 1

# there is 202300 expanding diamond steps around the original diamond

def compute_diamon_direct(x):
    
    # part 1 depend on eveness of the number of steps
    even=x%2==0
    A1 = partAp if even else partAi
    A2 = partAi if even else partAp
    B=partBi+partBp

    # quantity of B parts
    diasize = (2*x-1)*(2*x-1)
    mulB = int((diasize-1)/4)

    # there is two separate A parts
    # here is the central one
    fac1=floor((x-1)/2)
    fac1b=floor((fac1)/2)*(fac1+1)
    if fac1%2==1: fac1b += floor((fac1+1)/2)
    fac1c=8*fac1b
    
    # here is the other A part
    fac2=floor((x)/2)
    fac2b=fac2*fac2*4

    dirvalue = A1 + fac1c * A1 + fac2b * A2 + mulB * B

    print("part 2 direct:",dirvalue)


def compute_diamond_area(steps):
    B=partBi+partBp
    mulA1,mulA2=0,0
    mulamount=4
    # there is only about 200k steps
    # so we can just iterate through it
    for x in range(1,steps+1):
        even=x%2==0
        A1 = partAp if even else partAi
        A2 = partAi if even else partAp
        diasize = (2*x-1)*(2*x-1)
        mulB = int((diasize-1)/4)
        value = A1 + mulA1 * A1 + mulA2 * A2 + mulB * B
        if x==prevdiamond:
            print("Part 2 iterative:",value)
        if even:
            mulA1+=mulamount
        else:
            mulA2+=mulamount
        mulamount+=4

compute_diamond_area(prevdiamond)
compute_diamon_direct(prevdiamond)

# Part 1:

# repeat system for testing
repeat=1
halfrepeat=floor(repeat/2)
map=[[map[j%gridx][i%gridy] for i in range(gridx*repeat)] for j in range(gridy*repeat)]
startx,starty=startx+startgridx*halfrepeat,starty+startgridy*halfrepeat
gridx,gridy=gridx*repeat,gridy*repeat

cur=set()
cur.add((startx,starty))
for x in range(64):
    nextcur=set()
    for p in cur:
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            npx,npy=p[0]+dx,p[1]+dy
            if npx<0 or npx>=gridx or npy<0 or npy>=gridy: continue
            if map[npy][npx]:
                nextcur.add((npx,npy))
    cur=nextcur
print("Part 1:",len(cur))

def draw_image():
    img = Image.new(mode="RGB", size=(gridx, gridy))
    pixels = img.load() # create the pixel map

    for j,y in enumerate(map):
        for i,x in enumerate(y):
            pixels[i,j] = (i%startgridx,j%startgridy,0) if x else (0,0,0)   
            if i==startx and j==starty:
                pixels[i,j] = (255,255,255)

    for px,py in cur:
        pixels[px,py] = (0,0,255)
    img.show()
    #img.save('aoc_21_1.png')
#draw_image()