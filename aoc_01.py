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

def code2(x):
    mastart = list(sorted(filter(lambda a : a[0]>-1, [[x.find(k),k,v] for k,v in keys.items()])))
    maend = list(sorted(filter(lambda a : a[0]>-1, [[x.rfind(k),k,v] for k,v in keys.items()])))
    #return x+": "+"".join(map(lambda a: str(a[2]), mastart))+"\n"
    #return x+": "+str(mastart[0][2])+str(maend[-1][2])+"\n"
    return int(str(mastart[0][2])+str(maend[-1][2]))
    #return int(str(ma[0][2])+str(ma[-1][2]))

#print(''.join(map(code2,lines)))
print(sum(map(code2,lines)))
