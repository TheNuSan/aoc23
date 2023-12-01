import os
import sys
import re
from functools import reduce

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_01_1.txt"), "r").readlines()
#lines = ["two1nine","eightwothree","abcone2threexyz","xtwone3four","4nineeightseven2","zoneight234","7pqrstsixteen","one2one"]

def code1(x):
    ma=re.findall("[0-9]", x)
    #return ','.join(x for x in ma)+'\n'
    return int(ma[0]+ma[-1])

keys={"one":1, "two": 2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}
for i in range(1,10): keys[str(i)]=i

def findkeys(x, searchfunc):
    return list(sorted(filter(lambda a : a[0]>-1, [[searchfunc(x,k),v] for k,v in keys.items()])))

def code2(x):
    mastart = findkeys(x, lambda a,b: a.find(b))
    maend = findkeys(x, lambda a,b: a.rfind(b))
    #return x+": "+"".join(map(lambda a: str(a[1]), mastart))+"\n"
    #return x+": "+str(mastart[0][1])+str(maend[-1][1])+"\n"
    return int(str(mastart[0][1])+str(maend[-1][1]))
    #return int(str(ma[0][1])+str(ma[-1][1]))

#print(''.join(map(code2,lines)))
print("Part 1: "+str(sum(map(code1,lines))))
print("Part 2: "+str(sum(map(code2,lines))))
