import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_12_1.txt"), "r").readlines()

######## PART 1 ################


def solvepart1naive(pos, dam):
    leeway=len(pos) - (sum(dam)+len(dam)-1)
    if leeway<0:
        print("Error leeway computation")
        return 0
    if leeway==0:
        #print(str(pos) + " " + str(1))
        return 1
    
    places=len(dam)+1
    
    #print(pos)
    #print(dam)
    #print(str(leeway) + " " + str(len(pos)) + " " + str(places))

    # we can then redistribute the leeway points in every place before, between or after the damage groups
    def combi(start, length, points):
        ret=[]
        for i in range(start,length):
            if points>1:
                ret += [[i]+(j if type(j) == list else [j]) for j in combi(i,length, points-1)]
            else:
                ret.append(i)
        #print(" - " + str(start) + " "+str(points) + " " + str(ret))
        return ret
    
    counter=0
    lst=combi(0,places,leeway)
    #print(lst)
    for c in lst:
        st=""
        for j in range(places):
            pc= c.count(j) if type(c) == list else (1 if c==j else 0)
            st+=''.join(['.' for x in range(pc)])
            if j>0 and j<places-1:
                st+="."
            if j<len(dam):
                st+=''.join(['#' for x in range(dam[j])])
        if len(st) != len(pos):
            print("Error len of pos")
            return
        valid=True
        for i,c in enumerate(pos):
            if c!="?" and c!=st[i]:
                valid=False
                break
        if valid:
            counter+=1
            #print(("VALID : " if valid else "INVALID : ") + str(st))
    #print(str(pos) + " " + str(counter))
    return counter

def part1naive(l):
    p=l.split()
    pos=p[0]
    dam=[int(x) for x in p[1].split(",")]
    val = solvepart1naive(pos, dam)
    #print("-",l.removesuffix("\n"),"->",val)
    return val

##############################################

# basic memoisation
cache={}

debugoff=-1
def printdebug(*args):
    print("_"*(debugoff*5),*args)

def debugsolve(st, li):
    global debugoff
    debugoff+=1
    
    # memoization search:
    memkey=st+str(li)
    if memkey in cache:
        return cache[memkey]
    
    val=solve(st,li)

    # memoization add:
    cache[memkey]=val

    debugoff-=1
    return val

def solve(st, li):
    #printdebug("  "+''.join(str(i%10) for i in range(len(st))))
    #printdebug("> "+str(st)+" "+str(li))
    # start by testing basic picross leeway value
    leeway=len(st) - (sum(li)+len(li)-1)
    if leeway<0:
        #printdebug("<leeway impossible")
        return 0
    if leeway==0:
        valid=True
        cand='.'.join("#"*l for l in li)
        #printdebug("|candidate:",cand)
        if len(cand) != len(st):
            #printdebug("<Error cand",cand,st)
            return 0
        for i,c in enumerate(st):
            if c!="?" and c!=cand[i]:
                valid=False
                break
        if not valid:
            #printdebug("<leeway impossible as candidate")
            return 0
        #printdebug("<leeway 1")
        return 1
    # test if blocks are already all marked in the string
    nblocks=sum(i for i in li)
    strblocks=st.count("#")
    #printdebug("|blocks:",nblocks,"strblocks",strblocks)
    if nblocks<strblocks:
        #printdebug("<cannot fit those blocks")
        return 0
    #if nblocks==strblocks:
        ##printdebug("<blocks already marked")
        # need to test if blocks are correct, not just total number
        #return 1
    # split the string by the highest block and see where it can fit
    top=max(li)
    idx=next(i for i,v in enumerate(li) if v==top)
    start=sum(li[i] for i in range(idx)) + idx
    places=leeway+1
    #printdebug("|places:",places,"top:",top,"idx:",idx,"start:",start)
    libef=li[:idx]
    liaft=li[idx+1:]
    cursum=0
    for i in range(start,start+places):
        #if i>0: print("before:",i-1,st[i-1])
        #if i+top<len(st): print("after:",i+top,st[i+top])
        #print("relevant:",''.join(st[i+j] for j in range(top)))
        #conf=sum(1 for j in range(top) if st[i+j]==".")
        #print("conflict",conf)
        if i>0 and st[i-1]=="#":
            #printdebug("|skip 1:",i,st[i-1])
            continue
        if i+top<len(st) and st[i+top]=="#":
            #printdebug("|skip 2:",i+top,st[i+top])
            continue
        if any(True for j in range(top) if st[i+j]=="."):
            #printdebug("|skip 3:",i)
            continue
        #printdebug("|place",i,"testing")
        combbef,combaft=1,1
        # find combinatory on the string before the block, in a recursive way
        stbef=st[:max(0,i-1)]
        if len(libef)>0 or stbef.count("#")>0:
            if len(libef)>0 and len(stbef)>0:
                #printdebug("|stbef:",stbef,"libef:",libef)
                combbef=debugsolve(stbef,libef)
            else:
                combbef=0
        if combbef==0:
            #printdebug("|place",i,"failed bef")
            continue
        # find combinatory on the string after the block, in a recursive way
        staft=st[i+1+top:]
        if len(liaft)>0 or staft.count("#")>0:
            if len(liaft)>0 and len(staft)>0:
                #printdebug("|staft:",staft,"liaft:",liaft)
                combaft=debugsolve(staft,liaft)
            else:
                combaft=0
        if combaft==0:
            #printdebug("|place",i,"failed aft")
            continue
        cursum += combbef*combaft
    #printdebug("<end",str(st),str(li),"->",cursum)
    return cursum


def start_solve(st, li):
    # simplify cuts
    st='.'.join([s for s in st.split('.') if s!=''])
    return debugsolve(st, li)

def part1(line):
    p=line.split()
    pos=p[0]
    dam=[int(x) for x in p[1].split(",")]
    val = start_solve(pos, dam)
    #print("-",line.removesuffix("\n"),"->",val)
    return val

#print("resultat:",start_solve(".??..??...?##.", [1,1,3]))
#print("resultat:",start_solve(".??.?#??##???.", [1,6]))
#print("resultat:",start_solve("?#???#???#", [1,1,2]))
 
def find_result_diff():
    diffcount=0
    for i,l in enumerate(lines):
        ra = part1naive(l)
        rb = part1(l)
        if ra != rb:
            print("diff",i,l.removesuffix("\n")," -> ",ra,rb)
            diffcount+=1
    
    if diffcount>0:
        print(diffcount,"differences")
    else:
        print("Everything match")

def printdebug(*args): return
#find_result_diff()

#testline="????#???#.?#???#?.#? 2,2,1,1,4,2"
#print("resultat:",part1(testline))
#print("part 1: ",part1naive(testline))

print("Part 1:",sum(part1(l) for l in lines))

# let's test brute force part 2
progress=0
def part2(l):
    global progress
    progress+=1
    p=l.split()
    pos=p[0]
    dam=[int(x) for x in p[1].split(",")]
    mult=5
    pos2="?".join(pos for i in range(mult))
    dam2=[]
    for i in range(mult):
        dam2 += dam
    val = start_solve(pos2, dam2)
    #print(progress,"-",l.removesuffix("\n"),"->",val)
    return val

print("Part 2:",sum(part2(l) for l in lines))

#print("resultat:",part2(".???.??..#..?#??? 1,1,1,1"))
