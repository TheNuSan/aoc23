import os
import time

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_19_1.txt"), "r").read().split("\n")

varnames="xmas"
opsymbols="-<>"

class Rule:
    dest=""
    testvar=-1 # index of the variable to test
    testref=0 # value to compare the variable to
    testtype=0 # type of test, 0 is no test (jump), 1 is "<" and 2 is ">"
    def __init__(self, rulestr):
        if rulestr.find(':')>=0: # has a test
            sep=rulestr.split(":")
            self.dest=sep[1]
            sign=max(sep[0].find('<'),sep[0].find('>')) # find index of the sign
            self.testvar=varnames.index(sep[0][:sign])
            self.testref=int(sep[0][sign+1:])            
            self.testtype=opsymbols.index(sep[0][sign])
        else: # no test
            self.dest=rulestr
    def __str__(self):
        return varnames[self.testvar]+opsymbols[self.testtype]+str(self.testref)+":"+self.dest if self.testtype>0 else self.dest

instr={}
parts=[]
for l in lines:
    if l=='': continue
    if l[0]!="{": # instruction set
        secs=l.removesuffix('}').split('{')
        instr[secs[0]]=[Rule(x) for x in secs[1].split(',')]
    else: # part
        parts.append([int(x.split('=')[1]) for x in l.removesuffix('}').split(",")])

# idea is to have states with ranges [minimum,maximum] in each variables
# at each instuction, split the input range in two for for every test if needed
# its needed if the reference value is included in the range
# when every range has finished it's journey through instructions, each state's range will be either accepted or not
# and we can simply sum up the combination of each state's variable's ranges

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
    def  isinside(self, part):
        return all(part[i]>=x[0] and part[i]<=x[1] for i,x in enumerate(self.variables))
    
states=[StateRange()] # start from the whole range
acceptedstates=[]
rejectedstates=[]
while len(states)>0: # while there is still states with instructions left
    st=states.pop() # take the next state
    if st.nextinst=="A": # is the state range done and accepted?
        acceptedstates.append(st)
        continue
    if st.nextinst=="R": # is the state range done and rejected?
        rejectedstates.append(st)
        continue
    nextrules=instr[st.nextinst] # get next rule set
    for r in nextrules:
        if r.testtype==0: # no test, jump
            st.nextinst=r.dest
            states.append(st)
            break
        elif r.testtype==1: # <
            cv=st.variables[r.testvar]
            if cv[0] < r.testref and cv[1] >= r.testref: # need to split the range in two
                newstate=StateRange()
                newstate.variables=[[x[0],x[1]] for x in st.variables] # copy the ranges
                newstate.nextinst=r.dest
                newstate.variables[r.testvar][1] = r.testref-1
                states.append(newstate)
                cv[0] = r.testref
            elif cv[1] < r.testref: # the whole range pass the test
                st.nextinst=r.dest
                states.append(st)
                break
        else: # >
            cv=st.variables[r.testvar]
            if cv[0] <= r.testref and cv[1] > r.testref: # need to split the range in two
                newstate=StateRange()
                newstate.variables=[[x[0],x[1]] for x in st.variables] # copy the ranges
                newstate.nextinst=r.dest
                newstate.variables[r.testvar][0] = r.testref+1
                states.append(newstate)
                cv[1] = r.testref
            elif cv[0] > r.testref: # the whole range pass the test
                st.nextinst=r.dest
                states.append(st)
                break
    #print("Step------\n"+'\n'.join(str(x) for x in states))
    
print("Part 1:",sum(sum(x) for x in parts if any(y.isinside(x) for y in acceptedstates)))
#print('\n'.join(str(x)+" -> "+str(x.combi()) for x in acceptedstates))
print("Part 2:", sum(x.combi() for x in acceptedstates))