import os
import time
import math
from PIL import Image, ImageDraw
import numpy as np
from itertools import pairwise

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_18_1.txt"), "r").read().split("\n")
points = []
dirchars = "RDLU"
ispart2 = True

# start by finding the global position of all the points
posx,posy=0,0
minx,miny,maxx,maxy=math.inf,math.inf,-math.inf,-math.inf
for l in lines:
    vals=l.split()
    dir=dirchars.index(vals[0])
    dist=int(vals[1])
    if ispart2:
        dir = int(vals[2][-2:-1])
        dist = int(vals[2][2:-2], 16)

    minx,miny,maxx,maxy=min(minx,posx),min(miny,posy),max(maxx,posx),max(maxy,posy)
    points.append([posx,posy])
    posx+=[1,0,-1,0][dir]*dist
    posy+=[0,1,0,-1][dir]*dist
points.append([posx,posy])
minx,miny,maxx,maxy=min(minx,posx),min(miny,posy),max(maxx,posx),max(maxy,posy)
minx,miny,maxx,maxy=minx-5,miny-5,maxx+5,maxy+5

# now separate the vertical/horizontal edges:
edgehor = [[p1,p2] for p1,p2 in pairwise(points) if p1[0]!=p2[0]]
#edgever = [[p1,p2] for p1,p2 in pairwise(points) if p1[1]!=p2[1]]
edges = [[points[i],points[i+1],points[i-1] if i>0 else points[-2],points[i+2] if i<len(points)-2 else points[1]] for i in range(0,len(points)-1)]
edgever = [x for x in edges if x[0][1]!=x[1][1]]

# fill pixels with red on the shape's edges
def filledges(pixels):
    st=[[0 for x in range(minx,maxx+1)] for y in range(miny,maxy+1)]
    for e in edgehor:
        sx,ex=e[0][0],e[1][0]
        if ex<sx: sx,ex=ex,sx
        for x in range(sx,ex+1):
            st[e[0][1]-miny][x-minx]=1
    for e in edgever:
        sy,ey=e[0][1],e[1][1]
        if ey<sy: sy,ey=ey,sy
        for y in range(sy,ey+1):
            st[y-miny][e[0][0]-minx]=1

    sizex,sizey=maxx-minx,maxy-miny
    for i in range(sizex+1): # for every pixel:
        for j in range(sizey+1):
            if st[j][i]>0.5:
                pixels[i,j] = (255, 127 ,127)
            else:
                pixels[i,j] = (0, 127 ,127)
    
# fill the shape as an image and display it
def solve_with_visuals():

    sizex,sizey=maxx-minx+1,maxy-miny+1
    img = Image.new(mode="RGB", size=(sizex, sizey))
    pixels = img.load() # create the pixel map
    filledges(pixels)
    
    vals=[[0 for x in range(sizex)] for y in range(sizey)]

    total=0
    for e in edgever:
        dx=e[0][0]-minx
        sy=min(e[0][1],e[1][1])
        ey=max(e[0][1],e[1][1])
        isdown = e[1][1]>e[0][1]
        
        if isdown:
            dx+=1
            sy+=1 if e[2][0]>e[0][0] else 0
            ey+=1 if e[3][0]<e[0][0] else 0
        else:
            sy+=1 if e[3][0]<e[0][0] else 0
            ey+=1 if e[2][0]>e[0][0] else 0
        
        side=1 if isdown else -1
        total+=dx*(ey-sy)*side
                
        for y in range(sy-miny, ey-miny):
            for x in range(dx):
                vals[y][x] += side

    for y in range(sizey):
        for x in range(sizex):
            v=vals[y][x]
            pv=pixels[x,y]
            pixels[x,y] = (pv[0], max(0,min(255,pv[2] + v*50)), 255 if v>0 else 0)
    img.show()
    #img.save('aoc_18_display.png')
    return total

# just solving by adding or substracting a rectangle area per vertical edge, depending on if it's aiming down or up
# the main difficulty is to handle the corners so you can extend or not to include the edge border only once
# I did it by checking, for each vertical edge, if the previous and next points are inward or outward
def solve():
    total=0
    for e in edgever:
        dx=e[0][0]-minx
        sy=min(e[0][1],e[1][1])
        ey=max(e[0][1],e[1][1])
        isdown = e[1][1]>e[0][1]
        
        if isdown:
            dx+=1
            sy+=1 if e[2][0]>e[0][0] else 0
            ey+=1 if e[3][0]<e[0][0] else 0
        else:
            sy+=1 if e[3][0]<e[0][0] else 0
            ey+=1 if e[2][0]>e[0][0] else 0
        
        side=1 if isdown else -1
        total+=dx*(ey-sy)*side

    return total

if ispart2: # part 2 is too large to show an image
    print("Part 2:",solve())
else:
    print("Part 1:",solve_with_visuals())

