import os
import time
from euclid import *
from itertools import combinations
import random

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_24_1.txt"), "r").read().split("\n")

areaminx,areamaxx,areaminy,areamaxy=200000000000000,400000000000000,200000000000000,400000000000000
#areaminx,areamaxx,areaminy,areamaxy=7,27,7,27

ignore_z=False
hail=[]
hailv=[]
for l in lines:
    pa=[[int(y) for y in x.split(", ")] for x in l.split(' @ ')]
    if ignore_z:
        pa[0][2]=0
        pa[1][2]=0
    hail.append(Ray3(Point3(*pa[0]),Vector3(*pa[1])))
    hailv.append(Vector3(*pa[1]))

def intersect2Dprecise(r1, r2, minx,maxx,miny,maxy):
    li = r1.connect(r2)
    if abs(li.v)<0.001:
        x,y=li.p.x,li.p.y
        if x>=minx and x<=maxx and y>=miny and y<=maxy:
            #print(r1,r2,li.p,abs(li.v)<0.001)
            return True
    return False

def intersect2D(r31, r32):
    # should use 2D ray intersection instead
    r1=Ray3(Point3(r31.p.x,r31.p.y),Vector3(r31.v.x,r31.v.y))
    r2=Ray3(Point3(r32.p.x,r32.p.y),Vector3(r32.v.x,r32.v.y))
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
        #print(li.p,intp1,tp1,tp2)
        minx,maxx,miny,maxy=areaminx+intp1.x,areamaxx+intp1.x,areaminy+intp1.y,areamaxy+intp1.y
        return intersect2Dprecise(Ray3(tp1,r1.v),Ray3(tp2,r2.v),minx,maxx,miny,maxy)
    return False

print("Part 1:",sum(1 if intersect2D(a,b) else 0 for a,b in combinations(hail, 2)))

# part 2:

def intersect2(r1, r2, minx,maxx,miny,maxy):
    li = r1.connect(r2)
    if abs(li.v)<0.001:
        x,y=li.p.x,li.p.y
        return True
        #if x>=minx and x<=maxx and y>=miny and y<=maxy:
            #print(r1,r2,li.p,abs(li.v)<0.001)
        #    return True
    return False

def intersect(r1, r2):
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
        #print(li.p,intp1,tp1,tp2)
        minx,maxx,miny,maxy=areaminx+intp1.x,areamaxx+intp1.x,areaminy+intp1.y,areamaxy+intp1.y
        return intersect2(Ray3(tp1,r1.v),Ray3(tp2,r2.v),minx,maxx,miny,maxy)
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


#laser=Ray3(Point3(24, 13, 10), Vector3(-3, 1, 2))
centerpos=Point3(236791014726812.16, 271014556863332.75, 328486884021705.75)
#founddir=Vector3(-0.5384898531927084, -0.41700128875288917, 0.7322148613534998)
founddir=Vector3(-164.00, -127.00, 223.00)
#farpos=centerpos + (founddir * -3000000000000*5)
#farpos=Point3(363206674204109.00, 368909610239044.50, 156592420220259.50)
farpos=Point3(363206674204110, 368909610239045, 156592420220258)
laser=Ray3(farpos, founddir)

#25.087728259526394, Point3(236791014726783.22, 271014556863310.25, 328486884021718.69)
# Axis: Vector3(-0.54, -0.42, 0.73)]
# -0.5384898531927461 -0.417001288752925 0.7322148613534516
#
# best of best:
# [0.0, Vector3(236791014726812.16, 271014556863332.75, 328486884021705.75), Vector3(0.54, 0.42, -0.73)]
# 0.5384898531927084 0.41700128875288917 -0.7322148613534998

def find_best_axis_multiple():
    best=[math.inf,-1]
    for x in range(1,100000):
        vx=founddir*x
        diff=abs(vx.x-round(vx.x))+abs(vx.y-round(vx.y))+abs(vx.z-round(vx.z))
        if diff<best[0]:
            best=[diff,x]
    print(best)

def find_axis_dist():
    laserdists=[]
    for i in range(len(hail)):
        x=hail[i]
        inter,pos=intersectpos(laser,x)
        if inter:
            distray=x.p.distance(pos)/abs(hailv[i])
            distlaser=farpos.distance(pos)/abs(founddir)
            laserdists.append([distray, distlaser])
    laserdists.sort(key=lambda x: x[0])
    #print(', '.join(str(int(x[0]/10000000000))+" "+str(int(x[1]/10000000000)) for x in laserdists))
    print(len(laserdists))
    laserspeed=(laserdists[1][1]-laserdists[0][1])/(laserdists[1][0]-laserdists[0][0])
    timeoffset=laserdists[0][1]-laserdists[0][0]
    laseraboutdist=farpos + founddir*timeoffset
    print(laserspeed*founddir)
    print(laserspeed,timeoffset,laseraboutdist)
    return laserdists
    '''
    interpos2=[]
    for x in interpos:
        interpos2.append((x-interpos[0])/2741)

    best=[math.inf,-1]
    for u in range(1,10000):
        vx=founddir*x
        diff=0
        for x in interpos2:
            cx=x*u/2741
            diff+=abs(cx-round(cx))
        if diff<best[0]:
            best=[diff,u]
    print(best) # 6766
    print(', '.join(str(x*best[1]/2741) for x in interpos2))
    '''

laserd=find_axis_dist()

def checkcolision(testdir):
    colcounter=0
    for x in hail:
        if intersect(laser,x):
            colcounter+=1
    print("Cols:",colcounter)

# print(founddir*2741)
checkcolision(founddir)
print("Part 2:",str(farpos.x+farpos.y+farpos.z))

'''
random.seed(1234)
samples=50000
randscale=0.5
best=[math.inf,Point3(0,0,0),Vector3(0,0,0)]
raynum=5
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

print("best:",best)
print("best axis:",best[2].x,best[2].y,best[2].z)
print("ref:",Vector3(-3, 1, 2).normalized())
#bestref=Ray3(best[1],best[2])
#laser=Line3(Point3(24, 13, 10), Vector3(-3, 1, 2))
#'''

# now we found an approximate axis and center, we should:
# find all intersections points and sort them along the laser
# get all the distance between each points, find what factor can make them integer

'''
for r in hail:
    li = r.connect(laser)
    if abs(li.v)<100.001:
        mu=laser.p.distance(li.p2)/abs(laser.v)
        print("about Colliding:",abs(li.v),li.p1,mu)
    else:
        print("Not colliding")
'''