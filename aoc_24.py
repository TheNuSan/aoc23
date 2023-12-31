import os
import time
from euclid import *
from itertools import combinations
import random

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_24_1.txt"), "r").read().split("\n")

# Part 1:

areaminx,areamaxx,areaminy,areamaxy=200000000000000,400000000000000,200000000000000,400000000000000
#areaminx,areamaxx,areaminy,areamaxy=7,27,7,27

hail=[]
hailv=[]
for l in lines:
    pa=[[int(y) for y in x.split(", ")] for x in l.split(' @ ')]
    hail.append(Ray3(Point3(*pa[0]),Vector3(*pa[1])))
    hailv.append(Vector3(*pa[1]))

def intersect2D(r31, r32):
    r1 = Ray2(Point2(r31.p.x,r31.p.y), Vector2(r31.v.x,r31.v.y))
    r2 = Ray2(Point2(r32.p.x,r32.p.y), Vector2(r32.v.x,r32.v.y))
    pc = r1.intersect(r2)
    if not pc:
        return False
    if pc.x>=areaminx and pc.x<=areamaxx and pc.y>=areaminy and pc.y<=areamaxy:
        return True
    return False

print("Part 1:",sum(1 if intersect2D(a,b) else 0 for a,b in combinations(hail, 2)))

# Part 2:

def intersect3D(r1, r2):
    if r1.v.normalized() == r2.v.normalized():
        # should check if lines are colinear!
        print("Parallel",r1,r2)
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
        li2 = Ray3(tp1,r1.v).connect(Ray3(tp2,r2.v))
        return abs(li2.v)<0.001
    return False

def intersectpos(r1, r2):
    # do intersect in 2D
    li = r1.connect(r2)
    #if abs(li.v)<0.001:
    if abs(li.v)<10.00: # temporary
        return True,li.p
    return False,0

def flatten(r,dir):
    r2=r.copy()
    r2.p=r2.p+(-r2.p.dot(dir)*dir) # +- a bit weird, but it's to keep points, not vectors
    r2.v=r2.v+(-r2.v.dot(dir)*dir)
    return r2

# first step: find the ray direction
# I use a stochastic brute force solution: try random direction and see which is the best
# then continue searching around this direction until reached a desire precision
# to evaluate how "good" a ray is, I take the size of the bounding circle of the intersection between 5 rays
# the smallest the bounding circle, the more those points are confunded, on the correct ray they are matching exactly

random.seed(1234)
samples=50000
randscale=0.5
best=[math.inf,Point3(0,0,0),Vector3(0,0,0)]
raynum=5 # we take 5 consecutive rays to try to find the best angle
for x in range(samples):
    axis=Vector3(random.uniform(-1, 1),random.uniform(-1, 1),random.uniform(-1, 1))
    if x>10000:
        randscale *= 0.999
        axis = best[2] + axis*randscale
    axis.normalize()
    if abs(axis)<=0.001:
        continue
    firstnum=random.randint(0,max(0, len(hail)-raynum-1))
    base=flatten(hail[firstnum],axis)
    interpos=[]
    raycc=min(raynum,len(hail))
    for i in range(1,raycc):
        other=flatten(hail[i],axis)
        inter,pos=intersectpos(base,other)
        if inter:
            interpos.append(pos)
    if len(interpos)==raycc-1:
        center=interpos[0]
        for i in range(1,len(interpos)):
            center=center+interpos[i]
        center*=1.0/len(interpos)
        bounds=0
        for i in interpos:
            bounds+=abs(center-i)
        bounds/=len(interpos)
        if bounds<best[0]:
            best=[bounds,center,axis]
        #print(a,b,len(interpos),"intersections:",bounds,center)
    else:
        ...
        #print(a,b,"No enough intersections",len(interpos))

#print("best:",best)
print("best axis:",best[2].x,best[2].y,best[2].z)

centerpos=Point3(0,0,0)+best[1] # we need a point, not a vector
founddir=-best[2] # todo: should automatically find the side of the ray direction
farpos=centerpos + (founddir * -3000000000000*5) # we estimate the starting position being far way
#founddir=Vector3(-0.5384898531927084, -0.41700128875288917, 0.7322148613534998)
#founddir=Vector3(-164.00, -127.00, 223.00)
#farpos=Point3(363206674204110, 368909610239045, 156592420220258)

# here we check the timings of all the rays and adjust the laser start pos/direction accordingly
def find_axis_dist():
    global founddir
    global farpos
    laser=Ray3(farpos, founddir)
    laserdists=[]
    # get all the approximated hit positions
    for i in range(len(hail)):
        x=hail[i]
        inter,pos=intersectpos(laser,x)
        if inter:
            distray=x.p.distance(pos)/abs(hailv[i])
            distlaser=farpos.distance(pos)/abs(founddir)
            laserdists.append([distray, distlaser])
    # sort them front to back
    laserdists.sort(key=lambda x: x[0])
    #print(', '.join(str(int(x[0]/10000000000))+" "+str(int(x[1]/10000000000)) for x in laserdists))
    print(len(laserdists))
    # get the nearest two hits from the laser's start, those would have the best precision
    # compute the laser velocity: two hits distance divided by their time difference
    laserspeed=(laserdists[1][1]-laserdists[0][1])/(laserdists[1][0]-laserdists[0][0])
    # compute the distance between the start of our test laser and the actual start of the laser
    timeoffset=laserdists[0][1]-laserdists[0][0]
    
    # the new laser direction is just the old one scaled with the found speed
    newdir=laserspeed*founddir
    # rounding it seems to be better, but it may just be my dataset
    founddir = Vector3(round(newdir.x),round(newdir.y),round(newdir.z))
    print(founddir)
    
    # the new laser start position is moved according to the offset we found
    laseraboutdist=farpos + founddir*timeoffset
    print(laserspeed,timeoffset,laseraboutdist)
    farpos = Point3(round(laseraboutdist.x),round(laseraboutdist.y),round(laseraboutdist.z))

# we do the computation twice, the first one is not precise enough
# the second one will have a good founddir and farpos to work with
find_axis_dist()
find_axis_dist()

# on my dataset, this was enough to find the correct solution
# but on other, maybe the rounding doesn't work as well
# in this case, I would probably test for location around the position we found
# until there is one that does collide precisely with every ray

# now we can check if all the ray have a precise collision with the laser
# if true, we really found the correct laser
def checkcolision(testdir):
    colcounter=0
    laser=Ray3(farpos, founddir)
    for x in hail:
        if intersect3D(laser,x):
            colcounter+=1
    print("Cols:",colcounter)

checkcolision(founddir)
print("Part 2:",str(farpos.x+farpos.y+farpos.z))