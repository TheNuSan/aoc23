import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math
import time

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_13_1.txt"), "r").readlines()

def solve(tab, wantederrors):
    print("----------------")
    gridx=len(tab[0])
    gridy=len(tab)
    sols=0
    resu=0
    print("Grid:",gridx,gridy)
    # vertical mirrors:
    for i in range(1,gridx):
        nm=min(i,gridx-i)
        errors=sum(int(tab[j][i-k-1]!=tab[j][i+k]) for j in range(0,gridy) for k in range(nm))
        if errors==wantederrors:
            print("Found vertical",i)
            sols+=1
            resu+=i
            for l in tab:
                print(l[:i]+"|"+l[i:])
    # horizontal mirrors:
    for j in range(1,gridy):
        nm=min(j,gridy-j)
        errors=sum(int(tab[j-k-1][l]!=tab[j+k][l]) for l in range(0,gridx) for k in range(nm))
        if errors==wantederrors:
            print("Found horizontal",j)
            sols+=1
            resu+=j*100
            for i,l in enumerate(tab):
                if i==j:
                    print("-"*gridx)
                print(l)
    print("Found",sols,"solutions",resu)
    return resu
    #print("\n".join(tab))

cur=[]
totalpart1=0
totalpart2=0
puz=[]
for line in lines:
    line=line.removesuffix("\n")
    if line=='':
        puz.append(cur)
        cur=[]
    else:
        cur.append(line)
puz.append(cur)

for p in puz:
    totalpart1+=solve(p,0)
    totalpart2+=solve(p,1)

print("Part 1:",totalpart1)
print("Part 2:",totalpart2)