import os
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_20_1.txt"), "r").read().split("\n")
lines.append("button -> broadcaster")

class Module:
    name="None"
    inputs=[]
    outputs=[]
    type=0 # 0=broad, 1=flipflop, 2=conjonction, 3=output
    flipflop=False
    conjunction=[]
    def __str__(self):
        return self.name + [" (broad)"," (flipflop)"," (Conjonction)"," (out)"][self.type] + " : " + ", ".join(x[0].name for x in self.inputs) + " -> " + ", ".join(x.name for x in self.outputs)
    def __repr__(self):
        return self.name
    
modules = {}
# first pass: create modules
for l in lines:
    sep = l.split(" -> ")
    mod = Module()
    mod.inputs=[]
    if sep[0][0]=='%':
        mod.name=sep[0][1:]
        mod.type=1
    elif sep[0][0]=='&':
        mod.name=sep[0][1:]
        mod.type=2
    else:
        mod.name=sep[0]
    modules[mod.name] = mod

finaloutputs=[]

# second pass: link them (inputs and outputs)
for l in lines:
    sep = l.split(" -> ")
    name=sep[0].removeprefix('%').removeprefix('&')
    mod = modules[name]
    mod.outputs = []
    for x in sep[1].split(', '):
        if x in modules:
            mod.outputs.append(modules[x])
        else: # unknown module, create an output one
            nmod = Module()
            nmod.name = x
            nmod.type = 3
            nmod.inputs=[]
            nmod.outputs=[]
            modules[nmod.name] = nmod
            finaloutputs.append(nmod)
            mod.outputs.append(nmod)
    for x in mod.outputs:
        x.inputs.append([mod,False])

#for m in modules.values(): print(m)

print("Outputs:",",".join(x.name for x in finaloutputs))

presses=0
def ButtonPress():
    global presses
    presses+=1
    # low pulses are False, high pulses are True
    broad=modules["broadcaster"]
    button=modules["button"]
    pulses=[[broad,button,False]]
    highcounter=0
    lowcounter=0
    while len(pulses)>0:
        nextpulses=[]
        for p in pulses:
            dest=p[0]
            src=p[1]
            put=p[2]
            if put:
                highcounter+=1
            else:
                lowcounter+=1
            #print(src.name + " " + str(put) + " -> " + dest.name)
            if dest.type == 0: # broadcaster
                for x in dest.outputs: nextpulses.append([x,dest,put])
            elif dest.type == 1: # flipflop
                if not put: # low pulse
                    dest.flipflop = not dest.flipflop
                    for x in dest.outputs: nextpulses.append([x,dest,dest.flipflop])
            elif dest.type == 2: # conjonction
                for x in dest.inputs:
                    if x[0]==src:
                        x[1]=put
                        break
                sndput=not all(x[1] for x in dest.inputs)
                for x in dest.outputs: nextpulses.append([x,dest,sndput])
                # part 2: find cycles in the main conjugations
                if not sndput and dest in mainconjs:
                    if dest not in cyclefound:
                        cyclefound.append(dest)
                        mainresults.append([dest,presses])
                        print("Cycle",dest.name,presses)

        pulses=nextpulses
    return highcounter,lowcounter

mainconjs=[m for m in modules.values() if m.type==2 and any(x.type==1 for x in m.outputs)]
print("main conjonctions:",mainconjs)
mainresults = []
cyclefound = []

is_part_1 = False
if is_part_1:
    totalhigh,totallow=0,0
    for i in range(1000):
        #print("----------------")
        curhigh,curlow=ButtonPress()
        totalhigh+=curhigh
        totallow+=curlow
    print("Part 1:",totallow*totalhigh)
else:
    while True:
        ButtonPress()
        if len(cyclefound) >= len(mainconjs):
            break

    print("Cycles:",mainresults)
    # should find gcd for a generic thing
    print("Part 2:",math.prod(x[1] for x in mainresults))
