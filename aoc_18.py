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

# start by finding the global position of all the points
posx,posy=0,0
minx,miny,maxx,maxy=math.inf,math.inf,-math.inf,-math.inf
for l in lines:
    vals=l.split()
    dir=dirchars.index(vals[0])
    dist=int(vals[1])
    col=vals[2][2:-2]
    minx,miny,maxx,maxy=min(minx,posx),min(miny,posy),max(maxx,posx),max(maxy,posy)
    points.append([posx,posy])
    posx+=[1,0,-1,0][dir]*dist
    posy+=[0,1,0,-1][dir]*dist
points.append([posx,posy])
minx,miny,maxx,maxy=min(minx,posx),min(miny,posy),max(maxx,posx),max(maxy,posy)
#print(points)
print(minx,miny,maxx,maxy)

# now separate the vertical/horizontal edges:
edgehor = [[p1,p2] for p1,p2 in pairwise(points) if p1[0]!=p2[0]]
edgever = [[p1,p2] for p1,p2 in pairwise(points) if p1[1]!=p2[1]]

def display():
    st=[['.' for x in range(minx,maxx+1)] for y in range(miny,maxy+1)]
    #for p in points: st[p[1]-miny][p[0]-minx]="#"
    for e in edgehor:
        sx,ex=e[0][0],e[1][0]
        if ex<sx: sx,ex=ex,sx
        for x in range(sx,ex+1):
            st[e[0][1]-miny][x-minx]="#"
    for e in edgever:
        sy,ey=e[0][1],e[1][1]
        if ey<sy: sy,ey=ey,sy
        for y in range(sy,ey+1):
            st[y-miny][e[0][0]-minx]="#"
    for y in st:
        print(''.join(x for x in y))

def displayedges():
    sizex,sizey=maxx-minx,maxy-miny
    img = Image.new(mode="RGB", size=(sizex, sizey))
    pixels = img.load() # create the pixel map
    filledges(pixels)
    img.show()
    #img.save('aoc_18_display.png')

def filledges(pixels):
    st=[[0 for x in range(minx,maxx+1)] for y in range(miny,maxy+1)]
    #for p in points: st[p[1]-miny][p[0]-minx]="#"
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
                pixels[i,j] = (255, 0 ,0)
            else:
                pixels[i,j] = (0, 0 ,0)
    

def part1():

    sizex,sizey=maxx-minx+1,maxy-miny+1
    img = Image.new(mode="RGB", size=(sizex, sizey))
    pixels = img.load() # create the pixel map
    filledges(pixels)

    total=0
    for y in range(miny,maxy+1):
        lim=y
        #relevant=[e for e in edgever if e[0][1]>=lim and e[1][1]<lim]
        relevant=[e for e in edgever if min(e[0][1],e[1][1])<=lim and max(e[0][1],e[1][1])>=lim]
        relevant.sort(key = lambda a: a[0][0])
        prev=math.inf
        hasprev=False
        totline=0
        if relevant:
            for r in relevant:
                side=r[0][1]<r[1][1]
                if side:
                    totline += r[0][0]-prev+1
                    for x in range(prev,r[0][0]+1):
                        pv=pixels[x-minx,y-miny]
                        pixels[x-minx,y-miny] = (pv[0], min(255,pv[2]+127), min(255,pv[1]+255))
                    hasprev=False
                    prev=r[0][0]+1
                else:
                    if not hasprev:
                        hasprev=True
                        prev=r[0][0]
            total+=totline
        #print(lim,totline,total)

    img.show()
    img.save('aoc_18_display.png')

    return total

#display()
#displayedges()
# 69861
print("Part 1:",part1())

