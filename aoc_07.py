import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_07_1.txt"), "r").readlines()

hands = [[v if i%2==0 else int(v) for i,v in enumerate(l.split())] for l in lines]

def getrank(c):
    tab = sorted([c[0].count(x) for x in set(c[0])], reverse=True)
    cc = len(tab)
    if cc==1: return 7 # five of a kind
    if cc==2:
        if tab[0]==4: return 6 # four of a kind
        return 5 # full house
    if cc==3:
        if tab[0]==3: return 4 # three of a kind
        return 3 # two pair
    if cc==4: return 2 # one pair
    return 1

orders = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']

def judge1(a,b):
    atab = getrank(a)
    btab = getrank(b)
    #print(a[0] + " -> " + str(atab) + " | " + b[0] + " -> " + str(btab))
    if atab != btab: return 1 if atab < btab else -1
    for i in range(5):
        ao = orders.index(a[0][i])
        bo = orders.index(b[0][i])
        #print("     "+str(ao)+" " + str(bo))
        if ao != bo: return 1 if ao > bo else -1
    return 0

#print('\n'.join((c[0] + " rank " + str(getrank(c)) for c in hands)))

sortedhands = sorted(hands, key=cmp_to_key(judge1), reverse=True)

part1 = sum(c[1] * (i+1) for i,c in enumerate(sortedhands))

#print('\n'.join(c[0] for c in sortedhands))
print("Part 1: " + str(part1))

orders2 = ['A','K','Q','T','9','8','7','6','5','4','3','2','J',]

def getrank2(c):
    tab = sorted([[c[0].count(x),x] for x in set(c[0])], reverse=True)
    # Joker will transform into the most other present card
    if len(tab)>1:
        for i,v in enumerate(tab):
            if v[1]=='J':
                tab[1 if i==0 else 0][0] += v[0]
                del(tab[i])
                break
    #print(c[0]+" -> "+str(tab))
    cc = len(tab)
    if cc==1: return 7 # five of a kind
    if cc==2:
        if tab[0][0]==4: return 6 # four of a kind
        return 5 # full house
    if cc==3:
        if tab[0][0]==3: return 4 # three of a kind
        return 3 # two pair
    if cc==4: return 2 # one pair
    return 1

def judge2(a,b):
    atab = getrank2(a)
    btab = getrank2(b)
    #print(a[0] + " -> " + str(atab) + " | " + b[0] + " -> " + str(btab))
    if atab != btab: return 1 if atab < btab else -1
    for i in range(5):
        ao = orders2.index(a[0][i])
        bo = orders2.index(b[0][i])
        #print("     "+str(ao)+" " + str(bo))
        if ao != bo: return 1 if ao > bo else -1
    return 0

#print('\n'.join((c[0] + " rank " + str(getrank2(c)) for c in hands)))
#'''
sortedhands2 = sorted(hands, key=cmp_to_key(judge2), reverse=True)

part2 = sum(c[1] * (i+1) for i,c in enumerate(sortedhands2))

#print('\n'.join(c[0] for c in sortedhands2))
print("Part 2: " + str(part2))
#''' 


