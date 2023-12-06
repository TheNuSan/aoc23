import os
import sys
import re
from functools import reduce
from math import prod
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_06_1.txt"), "r").readlines()

flat = list(list(filter(str.isdigit,line.split())) for line in lines)
races = [[int(flat[0][i]),int(flat[1][i])] for i,_ in enumerate(flat[0])]

part1 = prod(list(len([1 for i in range(1,r[0]) if ((r[0]-i) * i)>r[1]]) for r in races))
print("Partie 1: "+str(part1))

flat2 = list(''.join(filter(str.isdigit,line.split())) for line in lines)
race2 = [int(flat2[0]),int(flat2[1])]
# haha, it's long, but not that long, so no need to improve on the computation
# part2 = len([1 for i in range(1,race2[0]) if ((race2[0]-i) * i)>race2[1]])

# but lets do it anyway, so it's instant
# 2nd order equation solve:
# (dist - x) * x - best = 0
# -1 * x² + dist * x - best
def solve(a,b,c):
    delta = b*b - 4*a*c
    return (-b-math.sqrt(delta))/(2*a), (-b+math.sqrt(delta))/(2*a)

dist,best = race2[0],race2[1]
r1,r2=solve(-1, dist, -best)
if r2<r1: r1,r2=r2,r1
part2=math.floor(r2)-math.ceil(r1)+1
print("Partie 2: "+str(part2))
    


