import os
import time

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_19_1.txt"), "r").read().split("\n")

varnames="xmas"
opsymbols="-<>"

class Rule:
    dest=""
    testvar=-1 # number of variable to test
    testref=0 # value to compare to
    testtype=0 # type of test, 0 is no test, 1 is < 2 is >
    def __init__(self, rulestr):
        if rulestr.find(':')>=0: # test
            sep=rulestr.split(":")
            self.dest=sep[1]
            sign=max(sep[0].find('<'),sep[0].find('>'))
            self.testvar=varnames.index(sep[0][:sign])
            self.testref=int(sep[0][sign+1:])            
            self.testtype=opsymbols.index(sep[0][sign])
        else: # no test
            self.dest=rulestr
    def __str__(self):
        return varnames[self.testvar]+opsymbols[self.testtype]+str(self.testref)+":"+self.dest if self.testtype>0 else self.dest

class State:
    variables=[0,0,0,0]
    def __init__(self, varstr):
        self.variables = [int(x.split('=')[1]) for x in varstr.removesuffix('}').split(",")]
    def __str__(self):
        return ' , '.join([varnames[i]+"="+str(v) for i,v in enumerate(self.variables)])
    
instr={}
parts=[]
for l in lines:
    if l=='': continue
    if l[0]!="{":
        secs=l.removesuffix('}').split('{')
        name=secs[0]
        rules=[Rule(x) for x in secs[1].split(',')]
        instr[name]=rules
        #print(name,'{ '+' , '.join(str(r) for r in rules)+' }')
    else:
        ns=State(l)
        parts.append(ns)
        #print(ns)

def part1(part):
    accepted=False
    nextinst="in"
    dbgstr=nextinst
    while True:
        nextrules=instr[nextinst]
        nextinst=None
        for r in nextrules:
            if r.testtype==0: # no test
                nextinst=r.dest
                break
            elif r.testtype==1: # <
                if part.variables[r.testvar] < r.testref:
                    nextinst=r.dest
                    break
            else: # >
                if part.variables[r.testvar] > r.testref:
                    nextinst=r.dest
                    break
        dbgstr+=" -> "+nextinst
        if not nextinst:
            print("Error no next instruction found")
        elif nextinst=="A":
            accepted=True
            break
        elif nextinst=="R":
            accepted=False
            break
        
    #print(part,"  ==>>  ", dbgstr, sum(part.variables))
    return sum(part.variables) if accepted else 0

part1value = sum(part1(x) for x in parts)
print("Part 1:",part1value)