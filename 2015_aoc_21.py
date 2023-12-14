import os
import sys
import re
from functools import reduce
from functools import cmp_to_key
from math import prod
import math
import time

t = time.process_time()

class perso:
    name,hp,damage,armor="empty",0,0,0
    def __init__(self, name, hp, damage, armor):
        self.name=name
        self.hp=hp
        self.damage=damage
        self.armor=armor
    def __str__(self):
        return self.name+" -> hp:"+str(self.hp)+" damage:"+str(self.damage)+" armor:"+str(self.armor)

class weapon:
    name,cost,damage,armor="empty",0,0,0
    def __init__(self, name, cost, damage, armor):
        self.name=name
        self.cost=cost
        self.damage=damage
        self.armor=armor
    def __str__(self):
        return self.name+" -> cost:"+str(self.cost)+" damage:"+str(self.damage)+" armor:"+str(self.armor)

shoplist="""
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage+1     25     1       0
Damage+2     50     2       0
Damage+3    100     3       0
Defense+1    20     0       1
Defense+2    40     0       2
Defense+3    80     0       3
"""
shoptab=[[((int(z) if z.isdigit() else z) for z in y.split()) for y in x.split('\n') if y and ":" not in y] for x in shoplist.split('\n\n')]
shopweapons=[weapon(*y) for y in shoptab[0]]
shoparmors=[weapon(*y) for y in shoptab[1]]
shoprings=[weapon(*y) for y in shoptab[2]]

def attack(a,d):
    dmg=max(1,a.damage-d.armor)
    d.hp=max(0,d.hp-dmg)
    #print(a.name,"deal",dmg,"damage",d.name,"down to",d.hp)

def play_match(p,b):
    while True:
        attack(p,b)
        if b.hp<=0:
            break
        attack(b,p)
        if p.hp<=0:
            break
    if p.hp>0:
        # player is still alive!
        #print("Player WIN")
        #print(p)
        return True
    else:
        #print("Boss WIN")
        #print(b)
        return False


#print("Weapons:\n"+'\n'.join(str(s) for s in shopweapons))
#print("Armors:\n"+'\n'.join(str(s) for s in shoparmors))
#print("Rings:\n"+'\n'.join(str(s) for s in shoprings))

def apply(p,o):
    p.damage+=o.damage
    p.armor+=o.armor
    return o.cost

def simu(ispart2):
    searchcost=0 if ispart2 else math.inf
    weapcount=len(shopweapons)
    armocount=len(shoparmors)
    ringcount=len(shoprings)
    for w in range(weapcount):
        for a in range(-1,armocount):
            for r1 in range(-1,ringcount):
                for r2 in range(-1,ringcount):
                    # cant have the same ring twice
                    if r1>=0 and r1==r2:
                        continue
                    cur = perso("player", 100, 0, 0)
                    cost=apply(cur, shopweapons[w])
                    if a>=0: cost+=apply(cur, shoparmors[a])
                    if r1>=0: cost+=apply(cur, shoprings[r1])
                    if r2>=0: cost+=apply(cur, shoprings[r2])
                    if (cost>searchcost if ispart2 else cost<searchcost):
                        boss = perso("boss", 109, 8, 2)
                        win=play_match(cur, boss)
                        if win != ispart2:
                            searchcost=cost

    if not ispart2:
        print("Part 1: Lowest cost while wining:",searchcost)
    else:
        print("Part 2: Highest cost while losing:",searchcost)

simu(False)
simu(True)


