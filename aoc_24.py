import os
import time
from euclid import *
from itertools import combinations
import random

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_24_0.txt"), "r").read().split("\n")

areaminx,areamaxx,areaminy,areamaxy=200000000000000,400000000000000,200000000000000,400000000000000
#areaminx,areamaxx,areaminy,areamaxy=7,27,7,27

ignore_z=False
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

#print("Part 1:",sum(1 if intersect(a,b) else 0 for a,b in combinations(hail, 2)))

# part 2:
'''
so each ray On->Vn has an intersection point Pn = On + kn * Vn with the laser
with 3 intersection point, we have: crossproduct(P2-P1,P3-P1) = 0

warning: I dont think this could ever work, as if you choose a point on one ray
the possible laser through a second ray form a plane, and the intersection with a third ray would be a point
but that means there is a different laser for each initial point
so we would need to use 4 rays somehow, maybe with 2 cross products?

G2=O2-O1 G3=O3-01
P2-P1=G2+k2*V2-k1*V1
P3-P1=G3+K3*V3-k1*V1

Cross product a,b:
        ay * bz - az * by = 0
        az * bx - ax * bz = 0
        ax * by - ay * bx = 0
(O2y+k2*V2y-O1y-k1*V1y) * (O3z+k3*V3z-O1z-k1*V1z) = (O2z+k2*V2z-O1z-k1*V1z) * (O3y+k3*V3y-O1y-k1*V1y)
(O2y+k2*V2y-O1y-k1*V1y) / (O2z+k2*V2z-O1z-k1*V1z) = (O3y+k3*V3y-O1y-k1*V1y) / (O3z+k3*V3z-O1z-k1*V1z)
k2*V2y = (O2z+k2*V2z-O1z-k1*V1z) * (O3y+k3*V3y-O1y-k1*V1y) / (O3z+k3*V3z-O1z-k1*V1z) - O2y+O1y+k1*V1y
k2*(V2y - V2z * (G3y+k3*V3y-k1*V1y) / (G3z+k3*V3z-k1*V1z)) = (G2z-k1*V1z) * (G3y+k3*V3y-k1*V1y) / (G3z+k3*V3z-k1*V1z) - G2y+k1*V1y

other idea, not mathematical:
for each angle, compute the bounds of all intersections in 2D from this viewpoint
take the angle with the smallest bounds, search around this angle for more detail
iterate up to the wanted precision (size of the bounds ~= 0)

this will probably be too slow with all the rays, but I can do the same with just 4 or 5 (smallest amout that has a unique laser?)
'''

def intersectpos(r1, r2):
    # do intersect in 2D
    li = r1.connect(r2)
    if abs(li.v)<0.001:
        return True,li.p
    return False,0

random.seed(1234)
samples=10000
best=[math.inf,Vector3(0,0,0)]
for x in range(samples):
        axis=Vector3(random.uniform(-1, 1),random.uniform(-1, 1),random.uniform(-1, 1))53)
        axis.normalize()
        if abs(axis)<=0.001:
            continue
        base=hail[0].copy()
        base.p=base.p+(-base.p.dot(axis)*axis) # +- a bit weird, but it's to keep points, not vectors
        base.v=base.v+(-base.v.dot(axis)*axis)
        interpos=[]
        for i in range(1,len(hail)):
            other=hail[i].copy()
            other.p=other.p+(-other.p.dot(axis)*axis)
            other.v=other.v+(-other.v.dot(axis)*axis)
            inter,pos=intersectpos(base,other)
            if inter:
                interpos.append(pos)
        if len(interpos)==len(hail)-1:
            center=interpos[0]
            for i in range(1,len(interpos)):
                center=center+interpos[i]
            bounds=0
            for i in interpos:
                bounds+=abs(center-i)
            bounds/=len(interpos)
            if bounds<best[0]:
                best=[bounds,axis]
            #print(a,b,len(interpos),"intersections:",bounds,center)
        else:
            ...
            #print(a,b,"No enough intersections",len(interpos))

print("best:",best)
print("ref:",Vector3(-3, 1, 2).normalized())
laser=Ray3(Point3(24, 13, 10), Vector3(-3, 1, 2))
#laser=Line3(Point3(24, 13, 10), Vector3(-3, 1, 2))

'''
for r in hail:
    li = r.connect(laser)
    if abs(li.v)<100.001:
        mu=laser.p.distance(li.p2)/abs(laser.v)
        print("about Colliding:",abs(li.v),li.p1,mu)
    else:
        print("Not colliding")
'''