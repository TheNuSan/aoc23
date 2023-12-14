from enum import Enum
import math
import copy

class player:
    hp,mana,shield,poison,recharge="empty",0,0,0,0
    def __init__(self, hp, mana):
        self.hp=hp
        self.mana=mana
    def __str__(self):
        st="Player   hp:"+str(self.hp)+" mana:"+str(self.mana)
        if self.shield>0: st+=" shield:"+str(self.shield)
        if self.poison>0: st+=" poison:"+str(self.poison)
        if self.recharge>0: st+=" recharge:"+str(self.recharge)
        return st
        
class boss:
    hp=0
    dmg=0
    def __init__(self, hp, dmg):
        self.hp=hp
        self.dmg=dmg
    def __str__(self):
        return "Boss     hp:"+str(self.hp)
    
class Action:
    name=""
    manacost=0
    def __init__(self, name, manacost):
        self.name=name
        self.manacost=manacost
    def __str__(self):
        return str(self.name)
    
class state:
    totalmana=0
    steps=0
    pla,bos=None,None
    def __init__(self, pla, bos):
        self.pla=pla
        self.bos=bos
    def __str__(self):
        return str(self.totalmana)+" "+str(self.pla)+" "+str(self.bos)

def boss_attack(st):
    parmor=7 if st.pla.shield>0 else 0
    dmg=max(1,st.bos.dmg-parmor)
    st.pla.hp=max(0,st.pla.hp-dmg)
    #debugprint("Boss deal",dmg,"damage Player down to",st.pla.hp)

missile=Action("Missile", 53)
drain=Action("Drain", 73)
shield=Action("Shield", 113)
poison=Action("Poison", 173)
recharge=Action("Recharge", 229)
actions=[missile,drain,shield,poison,recharge]

def apply_effects(st):
    if st.pla.shield>0:
        st.pla.shield-=1
        #debugprint("Shield timer",st.pla.shield)
    if st.pla.poison>0:
        st.bos.hp-=3
        st.pla.poison-=1
        #debugprint("Poison deal 3 timer",st.pla.poison)
    if st.pla.recharge>0:
        st.pla.mana+=101
        st.pla.recharge-=1
        #debugprint("Recharge mana",st.pla.mana,"timer",st.pla.recharge)

def player_canaction(act,st):
    # enough mana?
    if st.pla.mana<act.manacost: return False
    elif act==shield and st.pla.shield>0: return False
    elif act==poison and st.pla.poison>0: return False
    elif act==recharge and st.pla.recharge>0: return False
    return True

def player_doaction(act,st):
    if act==missile:
        st.bos.hp-=4
    elif act==drain:
        st.bos.hp-=2
        st.pla.hp+=2
    elif act==shield:
        st.pla.shield=6
    elif act==poison:
        st.pla.poison=6
    elif act==recharge:
        st.pla.recharge=5
    st.totalmana+=act.manacost
    st.pla.mana-=act.manacost
    #debugprint("Player cast",act.name)
    return True

def printstate(st):
    ...
    #debugprint(st.pla)
    #debugprint(st.bos)

def intern_step(st,act):
    #debugprint("----- Player turn -----")
    printstate(st)
    apply_effects(st)
    if st.pla.hp<=0 or st.bos.hp<=0: return False
    if player_canaction(act,st):
        player_doaction(act,st)
    if st.pla.hp<=0 or st.bos.hp<=0: return False

    #debugprint("----- Boss turn -----")
    printstate(st)
    apply_effects(st)
    if st.pla.hp<=0 or st.bos.hp<=0: return False
    boss_attack(st)
    if st.pla.hp<=0 or st.bos.hp<=0: return False

    st.steps+=1
    return True

def step(st,act):
    cont=intern_step(st,act)
    if not cont:
        if st.bos.hp<=0 and st.pla.hp>0:
            print("Player WIN")
        if st.pla.hp<=0:
            print("Boss WIN")
    return cont

#debugprint=print

# example 1:
#basestate = state(player(10,250),boss(13,8))
#actlist=[poison,missile]

# example 2:
#basestate = state(player(10,250),boss(14,8))
#actlist=[recharge,shield,drain,poison,missile]
#for act in actlist:
#    if not step(basestate,act): break

#'''
lowestmana=math.inf
def state_ending(st):
    if st.pla.hp>0 and st.bos.hp>0: return False
    # if we won, check if we are the lowest mana
    global lowestmana
    if st.pla.hp>0 and st.totalmana<lowestmana:
        lowestmana=st.totalmana
    return True

is_part_2 = True

basestate = state(player(50,500),boss(58,9))
#basestate = state(player(10,250),boss(14,8))
curstep=[basestate]
while len(curstep)>0:
    nextstep=[]
    for st in curstep:
        #debugprint("----- Player turn -----")
        printstate(st)
        if is_part_2:
            st.pla.hp-=1
            if state_ending(st): continue
        apply_effects(st)
        if state_ending(st): continue
        for act in actions:
            # is the action possible?
            if st.totalmana+act.manacost<lowestmana and player_canaction(act,st):
                newst=copy.deepcopy(st)
                player_doaction(act,newst)
                if state_ending(newst): continue
                #debugprint("----- Boss turn -----")
                printstate(newst)
                apply_effects(newst)
                if state_ending(newst): continue
                boss_attack(newst)
                if state_ending(newst): continue

                newst.steps+=1
                nextstep.append(newst)
    print("==== Step done, left:",len(nextstep))
    curstep=nextstep

print("Lowest mana cost:",lowestmana)
#'''