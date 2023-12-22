import os
import math
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

# compute parts:
partAp = 0 # inside diamond, even
partAi = 0 # inside diamond, odd
partBp = 0 # outside diamond, even
partBi = 0 # outside diamond, odd

print("--------------------------")
diag=math.floor((gridx-1)/2)
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


repeat=1
halfrepeat=math.floor(repeat/2)
map=[[map[j%gridx][i%gridy] for i in range(gridx*repeat)] for j in range(gridy*repeat)]
startx,starty=startx+startgridx*halfrepeat,starty+startgridy*halfrepeat
gridx,gridy=gridx*repeat,gridy*repeat
# lines on S row and column are empty, maybe that is a key?
#print(lines[starty])
#print(''.join(x[startx] for x in lines))
#print("starts:",startx,starty)
# also there is a diamond at 64 steps from start
# where everything is at same distance
# so next diamond is at 64 + 131 steps
totalsteps=26501365
prevdiamond=math.floor((totalsteps-64)/131)
prevsteps=prevdiamond*131+64
print("prevdiamond",prevdiamond)
print("prevsteps:",prevsteps)
print("diff:",totalsteps-prevsteps)

# steps +1 to acount for the initial diamond
prevdiamond += 1

# there is 202300 expanding diamond steps around the original diamond

# pair
# diamond 1: 3847 A pair ?
# diamond 2: 34893

# impair
# diamond 1: 3957 A impair ?
# diamond 2: 35223
# diamond 3: 97645
#print("Test 2 Ai:",partAi + 4*partAp + 2*partBp + 2*partBi)
#print("Test 2 Ap:",partAp + 4*partAi + 2*partBp + 2*partBi)
#print("Test 3 Ai:",partAi + 4*partAp + 8*partAi + 6*partBp + 6*partBi)

def compute_diamond_area(steps):
    B=partBi+partBp
    mulA1,mulA2=0,0
    mulamount=4
    # this could be made into a direct formula
    # but there is only about 200k steps
    # so lets just iterate through it
    for x in range(1,steps+1):
        even=x%2==0
        A1 = partAp if even else partAi
        A2 = partAi if even else partAp
        diasize = (2*x-1)*(2*x-1)
        mulB = int((diasize-1)/4)
        value = A1 + mulA1 * A1 + mulA2 * A2 + mulB * B
        if x==prevdiamond:
            print("Part 2:",value)
        if even:
            mulA1+=mulamount
        else:
            mulA2+=mulamount
        mulamount+=4

compute_diamond_area(prevdiamond)
# 637537341306357 is right !

# Part 1:
cur=set()
cur.add((startx,starty))
for x in range(64+1):
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