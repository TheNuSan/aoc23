import os
import sys
import re
from functools import reduce
from math import prod

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_02_1.txt"), "r").readlines()
#lines = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green","Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue","Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red","Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red","Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]

def code1(x):
    d = x.split(":")
    id = int(d[0].split(" ")[1])
    bag1 = {"red": 12, "green": 13, "blue":14}

    def test_entry1(x):
        y=x.strip().split(" ")
        return bag1[y[1]] >= int(y[0])

    return id if all(map(lambda y: all(map(test_entry1, y.split(","))), d[1].split(";"))) else 0

def code2(x):
    d = x.split(":")
    curbag={"red": 0, "green": 0, "blue":0}
    
    def test_entry2(x):
        y=x.strip().split(" ")
        curbag[y[1]] = max(curbag[y[1]],int(y[0]))

    list(map(lambda y: list(map(test_entry2, y.split(","))), d[1].split(";")))
    return prod(list(v for k,v in curbag.items()))

#print(''.join(map(code2,lines)))
print("Part 1: "+str(sum(map(code1,lines))))
print("Part 2: "+str(sum(map(code2,lines))))
        
