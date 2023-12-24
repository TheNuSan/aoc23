import os
import time
from euclid import *
from itertools import combinations

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_24_1.txt"), "r").read().split("\n")

areaminx,areamaxx,areaminy,areamaxy=200000000000000,400000000000000,200000000000000,400000000000000
#areaminx,areamaxx,areaminy,areamaxy=7,27,7,27

ignore_z=True
hail=[]
for l in lines:
    pa=[[int(y) for y in x.split(", ")] for x in l.split(' @ ')]
    if ignore_z:
        pa[0][2]=0
        pa[1][2]=0
    hail.append(Ray3(Point3(*pa[0]),Vector3(*pa[1])))

def intersect2(r1, r2, minx,maxx,miny,maxy):
    li = r1.connect(r2)
    if abs(li.v)<0.001:
        x,y=li.p.x,li.p.y
        if x>=minx and x<=maxx and y>=miny and y<=maxy:
            #print(r1,r2,li.p,abs(li.v)<0.001)
            return True
    return False

def intersect(r1, r2):
    if r1.v.normalized() == r2.v.normalized():
        # should check if lines are colinear!
        #print("Parallel",r1,r2)
        return False
    # to avoid issues around floating point precision
    # we first do a coarse distance test between the two lines
    # then from the closest point we go back an offset
    # and we translate everything to be local to that position
    # as all values used to translate are integers, we keep precise relative position
    # and we do a new distance test, as all values are small, the result is precise enough
    li = r1.connect(r2)
    tolerance=100.0
    if abs(li.v)<tolerance: # imprecise
        offset=1000.0
        mu1=int(max(0, (r1.p.distance(li.p1) - offset) / abs(r1.v)))
        mu2=int(max(0, (r2.p.distance(li.p2) - offset) / abs(r2.v)))
        #print("---",r1,r2,mu1,mu2)
        tp1 = Point3(0,0,0)
        intp1 = -(r1.p + mu1*r1.v)
        tp2 = (r2.p + mu2*r2.v) + intp1
        #print(li.p,intp1,tp1,tp2)
        minx,maxx,miny,maxy=areaminx+intp1.x,areamaxx+intp1.x,areaminy+intp1.y,areamaxy+intp1.y
        return intersect2(Ray3(tp1,r1.v),Ray3(tp2,r2.v),minx,maxx,miny,maxy)
    return False

counter=0
for a,b in combinations(hail, 2):
    if intersect(a,b): counter+=1
print("Part 1:",counter)
