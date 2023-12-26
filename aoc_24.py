import os
import time
from euclid import *
from itertools import combinations
import random
import pygame
from pygame.locals import *

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_24_1.txt"), "r").read().split("\n")

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
    #if abs(li.v)<0.001:
    if abs(li.v)<10.00: # temporary
        return True,li.p
    return False,0

def flatten(r,dir):
    r2=r.copy()
    r2.p=r2.p+(-r2.p.dot(dir)*dir) # +- a bit weird, but it's to keep points, not vectors
    r2.v=r2.v+(-r2.v.dot(dir)*dir)
    return r2


laser=Ray3(Point3(24, 13, 10), Vector3(-3, 1, 2))

random.seed(1234)
samples=50000
randscale=0.5
best=[math.inf,Point3(0,0,0),Vector3(0,0,0)]
raynum=50
for x in range(samples):
    axis=Vector3(random.uniform(-1, 1),random.uniform(-1, 1),random.uniform(-1, 1))
    if x>10000:
        randscale *= 0.999
        axis = best[1] + axis*randscale
    axis.normalize()
    if abs(axis)<=0.001:
        continue
    base=flatten(hail[0],axis)
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
print("ref:",Vector3(-3, 1, 2).normalized())
bestref=Ray3(best[1],best[2])
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

pygame.init()
 
# create the display surface object
# of specific dimension.
screen = pygame.display.set_mode((1000, 1000))
 

laser2=Ray3(Point3(24, 13, 10), Vector3(-3.5, 1.3, 2))

viewangle_x = 0
viewangle_y = 0
#scale=10
scale=1.0/2000000000000.0
nsc=3000000000000
def drawray(x,col):
    r = x.copy()
    r.p=qc*r.p
    r.v=qc*r.v
    pygame.draw.line(screen, col, (r.p.x*scale+500, r.p.y*scale+500), ((r.p.x+r.v.x*nsc)*scale+500, (r.p.y+r.v.y*nsc)*scale+500), 2)

def drawline(p1,p2,col):
    p1=qc*p1.copy()
    p2=qc*p2.copy()
    pygame.draw.line(screen, col, (p1.x*scale+500, p1.y*scale+500), (p2.x*scale+500, p2.y*scale+500), 2)


run = True 
# Creating a while loop
while run:
 
    # Iterating over all the events received from
    # pygame.event.get()
    for event in pygame.event.get():
 
        # If the type of the event is quit
        # then setting the run variable to false
        if event.type == QUIT:
            run = False
 
        # if the type of the event is MOUSEBUTTONDOWN
        # then storing the current position
        elif event.type == MOUSEBUTTONDOWN:
            ...
        elif event.type == KEYDOWN:
            if event.key == K_UP: viewangle_y=max(-3.1415,min(3.1415,viewangle_y+0.1))
            if event.key == K_DOWN: viewangle_y=max(-3.1415,min(3.1415,viewangle_y-0.1))
            if event.key == K_LEFT: viewangle_x+=0.1
            if event.key == K_RIGHT: viewangle_x-=0.1
            
    qc = Quaternion.new_rotate_euler(viewangle_x, viewangle_y, 0)

    screen.fill((0,0,0))

    for x in range(min(500000,len(hail))): drawray(hail[x], (255,255,255))

    '''
    random.seed(1234)
    samples=1
    best=[math.inf,Vector3(0,0,0)]
    for x in range(samples):
        #axis=Vector3(random.uniform(-1, 1),random.uniform(-1, 1),random.uniform(-1, 1))
        axis=laser.v
        axis.normalize()
        if abs(axis)<=0.001:
            continue
        col = (0,0,255)
        base=flatten(hail[0],axis)
        drawray(base, (0,255,255))
        interpos=[]
        for i in range(1,len(hail)):
            other=flatten(hail[i],axis)
            drawray(other, (0,255,255))
            inter,pos=intersectpos(base,other)
            if inter:
                drawline(pos,pos+Vector3(0,5,0), (255,255,0))
                interpos.append(pos)
        if len(interpos)==len(hail)-1:
            center=interpos[0]
            for i in range(1,len(interpos)):
                center=center+interpos[i]
            center*=1.0/len(interpos)
            bounds=0
            for i in interpos:
                bounds+=abs(center-i)
            bounds/=len(interpos)
            drawline(center,center+Vector3(0,-5,0), (255,0,0))
            if bounds<best[0]:
                best=[bounds,axis]
            #print(len(interpos),"intersections:",bounds,center)
        else:
            col=(255,0,127)
            ...
            #print(a,b,"No enough intersections",len(interpos))
        #drawray(Ray3(Point3(0,0,0)+axis*50, axis), col)
        drawline(Point3(0,0,0)+axis*(bounds+2),Point3(0,0,0)+axis*bounds, col)
    '''

    #drawray(laser, (0,255,0))
    #drawray(Ray3(Point3(0,0,0),best[1]), (255,255,0))
    drawline(best[1]-best[2]*nsc*500,best[1]+best[2]*nsc*500, (0,255,0))

    # Draws the surface object to the screen.
    pygame.display.update()