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

# Part 2:
# idea is to have parts with ranges in each variables
# at each instuction, copy the parts for every test that could work
# at the end, each part and so it's range will be either accepted or not
# and we can simply sum that up

class StateRange:
    variables = [[1,4000],[1,4000],[1,4000],[1,4000]]
    nextinst = "in"
    def __str__(self):
        return str(self.variables)
    def combi(self):
        val=1
        for x in self.variables:
            val *= x[1]-x[0]+1
        return val
    
def part2():
    basestate=StateRange()
    states=[basestate]
    acceptedstates=[]
    rejectedstates=[]
    while len(states)>0:
        nextstates=[]
        for st in states:
            if st.nextinst=="A":
                acceptedstates.append(st)
                continue
            if st.nextinst=="R":
                rejectedstates.append(st)
                continue
            nextrules=instr[st.nextinst]
            st.nextinst=None
            for r in nextrules:
                if r.testtype==0: # no test
                    st.nextinst=r.dest
                    nextstates.append(st)
                    break
                elif r.testtype==1: # <
                    cv=st.variables[r.testvar]
                    if cv[0] < r.testref and cv[1] >= r.testref: # need to split
                        newstate=StateRange()
                        newstate.variables=[[x[0],x[1]] for x in st.variables]
                        newstate.nextinst=r.dest
                        newstate.variables[r.testvar][1] = r.testref-1
                        nextstates.append(newstate)
                        cv[0] = r.testref
                        st.nextinst=r.dest
                    elif cv[1] < r.testref:
                        st.nextinst=r.dest
                        nextstates.append(st)
                        break
                    elif cv[0] >= r.testref:
                        ...
                    else:
                        break
                else: # >
                    cv=st.variables[r.testvar]
                    if cv[0] <= r.testref and cv[1] > r.testref: # need to split
                        newstate=StateRange()
                        newstate.variables=[[x[0],x[1]] for x in st.variables]
                        newstate.nextinst=r.dest
                        newstate.variables[r.testvar][0] = r.testref+1
                        nextstates.append(newstate)
                        cv[1] = r.testref
                        st.nextinst=r.dest
                    elif cv[1] <= r.testref:
                        ...
                    elif cv[0] > r.testref:
                        st.nextinst=r.dest
                        nextstates.append(st)
                        break
                    else:
                        break
        states = nextstates
        #print("Step------\n"+'\n'.join(str(x) for x in states))
        
    
    #print('\n'.join(str(x)+" -> "+str(x.combi()) for x in acceptedstates))
    print("Part 2:",sum(x.combi() for x in acceptedstates))
part2()