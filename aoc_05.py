import os
import sys
import re
from functools import reduce
from math import prod
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_05_1.txt"), "r").readlines()

seeds=[]
maps={}
links={}
curmap=""
for i, line in enumerate(lines):
    line=line.removesuffix("\n")
    if line.startswith("seeds: "):
        seeds = list(int(v) for v in line[7:].split(" "))
    elif line.find(" map:")>=0:
        mapname=line[:-5].split("-")
        links[mapname[0]]=mapname[2]
        curmap=mapname[2]
    elif len(line)>0:
        if not curmap in maps: maps[curmap] = []
        maps[curmap].append(list(int(v) for v in line.split(" ")))

# part 1, we can do it directly

def transformseed(id):
    curmap="seed"
    num = id
    #st = curmap + " " + str(num)+" -> "
    while curmap!=None:
        if curmap in links:
            curmap=links[curmap]
            tab=maps[curmap]
            trans = [num+j[0]-j[1] for j in tab if num >= j[1] and num<j[1]+j[2]]
            #print(str(tab))
            #print(" -> " + str(trans))
            if len(trans)==1:
                num = trans[0]
            elif len(trans)>1:
                print("Error seed " + id + " has several match in " + curmap)
            #st += curmap + " " + str(num)+" -> "
        else:
            curmap=None
    return num

low=None
for id in seeds:
    num=transformseed(id)
    if not low: low=num
    low=min(low, num)  
    #print(st)

print("Part 1: "+str(low))

# part 2, we need to track all ranges, and divide them accordingly

ranges={}
ranges["seed"]=[]
for i in range(int(len(seeds)/2)):
    start=seeds[i*2]
    length=seeds[i*2+1]
    ranges["seed"].append([start, start, length])

def trans_range(ri, rs, res):
    #print(ri)
    #print(rs)
    
    pred=ri[0]
    pree=min(ri[0]+ri[2],rs[1])
    
    #print(str(pred) + " " + str(pree))
    if pree>pred: res.append([pred, pred+ri[1]-ri[0], pree-pred])
    
    midd=max(ri[0],rs[1])
    mide=min(ri[0]+ri[2],rs[1]+rs[2])
    if mide>midd: res.append([midd, midd+ri[1]-ri[0], mide-midd])
    #print(str(midd) + " " + str(mide))

    endd=max(ri[0],rs[1]+rs[2])
    ende=ri[0]+ri[2]
    if ende>endd: res.append([endd, endd+ri[1]-ri[0], ende-endd])
    #print(str(endd) + " " + str(ende))
    #print(' + '.join(str(v[1]) + "->" + str(v[1]+v[2]) for v in res))
   
    

#trans_range([0,0,math.inf], [10,79,14], [])
#trans_range([20,20,64], [10,79,14], [])

def apply_range(curres, tmap):
    # slice the ranges
    for r in tmap:
        nextres=[]
        for r2 in curres:
            trans_range(r2, r, nextres)
        #print(' + '.join(str(v[1]) + "->" + str(v[1]+v[2]) for v in nextres))
        curres=nextres
    # progress the ranges
    res=[]
    for r2 in curres:
        nrr=[r2[0],r2[1],r2[2]]
        for r in tmap:
            midd=max(r2[0],r[1])
            mide=min(r2[0]+r2[2],r[1]+r[2])
            if mide>midd:
                nrr[0] += r[0]-r[1]
        res.append(nrr)
    #print(' + '.join(str(v[1]) + "->" + str(v[1]+v[2]) for v in curres))
    return res

#rangeseed=apply_range([[0,0,math.inf]], ranges["seed"])
#ranges["seed"]=rangeseed
    
#print(apply_range([[55,10,13]], [[52,50,12]]))
#'''
def printrange(rn, name):
    s=""
    for id in range(50,100):
        num = id
        trans = [num+j[0]-j[1] for j in rn if num >= j[1] and num<j[1]+j[2]]
        if len(trans)==1:
            num = trans[0]
        elif len(trans)>1:
            print("Error seed " + str(id) + " has several match ")
        s+=" {:02d}".format(num)
    print(s + " " + name)

curmap="seed"
while curmap in links:
    currange=ranges[curmap]
    nextmap=links[curmap]
    #printrange(currange, curmap)
    infmap=apply_range([[0,0,math.inf]], maps[nextmap] )
    
    #print(' input: '+' | '.join(str(v[0]) + "->" + str(v[0]+v[2]) + " + " + str(v[1]-v[0]) for v in currange))
    #print("    si: "+' | '.join(str(v[1]) + "->" + str(v[1]+v[2]) + " + " + str(v[0]-v[1]) for v in maps[nextmap]))
    #print("    by: "+' | '.join(str(v[1]) + "->" + str(v[1]+v[2]) + " + " + str(v[0]-v[1]) for v in infmap))
    #print(curmap+" -> "+nextmap)
    ranges[nextmap]=apply_range(currange, infmap)
    curmap=nextmap
    
#print("Final: "+' | '.join(str(v[0]) + "->" + str(v[0]+v[2]) + " + " + str(v[1]-v[0]) for v in ranges["location"]))
#printrange(ranges["location"], "location")
low2=math.inf
if "location" in ranges:
    for v in ranges["location"]:
        low2 = min(low2, v[0])

print("Part 2: "+str(low2))
#'''
#print(apply_range([[0,0,math.inf]], [[45,77,23],[81,45,17]]))

#print("seeds: "+str(seeds))
#print("links: " + str(links))
#print(str(maps))




