import os
import time
import pygame
import math
from pygame.locals import *
import pygame.freetype

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_20_0e.txt"), "r").read().split("\n")
for i in range(len(lines)):
    lines[i]=lines[i].replace("broadcaster","brd")
lines.append("but -> brd")

class Module:
    name="None"
    inputs=[]
    outputs=[]
    type=0 # 0=broad, 1=flipflop, 2=conjonction, 3=output
    flipflop=False
    conjunction=[]
    lowlist=[]
    def __init__(self):
        self.lowlist=[]
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

for m in modules.values():
    print(m)

print("Outputs:",",".join(x.name for x in finaloutputs))

def Part1():
    totalhigh,totallow=0,0
    for i in range(1000):
        #print("----------------")
        curhigh,curlow=ButtonPress()
        totalhigh+=curhigh
        totallow+=curlow
    print("Part 1:",totallow,totalhigh,totallow*totalhigh)

part2running=True
presses=0
historic={}
def Part2():
    while part2running:
        #print("----------------")
        ButtonPress()
    print("Part 2:",presses)

presses=0
def ButtonPress():
    global part2running
    global presses
    presses+=1
    # low pulses are False, high pulses are True
    broad=modules["brd"]
    button=modules["but"]
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
            '''if not put and dest in finaloutputs:
                print("Final Output ",dest.name,put)
                nextpulses=[]
                part2running=False
                break'''
                
            #print(src.name + " " + str(put) + " -> " + dest.name)
            if dest.type == 0: # broadcaster
                for x in dest.outputs: nextpulses.append([x,dest,put])
            elif dest.type == 1: # flipflop
                if not put: # low pulse
                    dest.flipflop = not dest.flipflop
                    if not dest in historic: historic[dest] = {}
                    hd=historic[dest]
                    if not presses in hd: hd[presses] = []
                    hd[presses].append(dest.flipflop)
                    for x in dest.outputs: nextpulses.append([x,dest,dest.flipflop])
            elif dest.type == 2: # conjonction
                for x in dest.inputs:
                    if x[0]==src:
                        x[1]=put
                        break
                sndput=not all(x[1] for x in dest.inputs)
                if not dest in historic: historic[dest] = {}
                hd=historic[dest]
                if not presses in hd: hd[presses] = []
                hd[presses].append(sndput)
                for x in dest.outputs: nextpulses.append([x,dest,sndput])
        pulses=nextpulses
    return highcounter,lowcounter

for i in range(200):
    ButtonPress()

mainconjs=[m for m in modules.values() if m.type==2 and any(x.type==1 for x in m.outputs)]
def find_child_list(m):
    foundchild=[]
    todo=[m]
    while len(todo)>0:
        x=todo.pop()
        foundchild.append(x)
        for y in x.inputs:
            if y[0] not in foundchild:
                todo.insert(0,y[0])
    print(m.name,"->",", ".join(x.name for x in foundchild))
    return foundchild


cursection=finaloutputs

testnode=finaloutputs[0]
if "pn" in modules: testnode=modules["pn"]

cursection=[testnode]
childs=find_child_list(testnode)

# lets try computing the loop of each flipflop of the test node
loops={}

broad=modules["brd"]

def send_bulk(presscount):
    order=1
    bulk=[[broad,False,presscount,order]]
    while len(bulk)>0:
        nextbulk=[]
        for p in bulk:
            src=p[0]
            for m in src.outputs:
                if m.type==1: # flip-flop
                    if not p[1]:
                        pressout=math.floor(p[2]/2)
                        if pressout>0:
                            order+=1
                            m.lowlist.append([src,True,pressout,order])
                            nextbulk.append([m,True,pressout,order])
                            m.lowlist.append([src,False,pressout,order])
                            nextbulk.append([m,False,pressout,order])
                elif m.type==2: # conjonction
                    order+=1
                    m.lowlist.append([src,p[1],pressout,order])
                        
        bulk=nextbulk
send_bulk(1000)

nodesections=[]
foundnodes=[]
while len(cursection)>0:
    nodesections.append([])
    nextsection=[]
    for x in cursection:
        if x not in foundnodes:
            foundnodes.append(x)
        nodesections[-1].append(x)
        for y in x.inputs:
            if y[0] not in foundnodes:
                foundnodes.append(y[0])
                nextsection.append(y[0])
    cursection=nextsection

nodepos={}
for i,s in enumerate(nodesections):
    for j,n in enumerate(s):
        nodepos[n]=(i*200+30,j*80-i*40+i*i*10+530)

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
font = pygame.freetype.Font(None, 24)
rect=pygame.draw.rect
circ=pygame.draw.circle
line=pygame.draw.line

coltype=[(250, 250, 0),(250, 100, 0),(100, 250, 250),(250, 250, 250)]

def DrawGraph():
    collink=[(255,255,255),(255,0,0)]
    colflip=[(0,255,0),(255,0,0)]
    for s in nodesections:
        for n in s:
            pos=nodepos[n]
            for l in n.outputs:
                if l in nodepos:
                    goalx,goaly=nodepos[l]
                    goalpos=(goalx,goaly+15)
                    if goalpos[0]<=pos[0]:
                        goalpos=(goalpos[0]+70,goalpos[1]-5)
                    line(screen, collink[int(goalpos[0]>pos[0])], (pos[0],pos[1]+15), goalpos)
                else:
                    circ(screen, (255,0,0), pos, 10)
            rect(screen, coltype[n.type], (pos[0],pos[1],70,28))
            if n.type==1: # flip-flop
                rect(screen, colflip[int(n.flipflop)], (pos[0]+45,pos[1]+4,18,18))
            if n.type==2: # conjunction
                rect(screen, colflip[int(all(x[1] for x in n.inputs))], (pos[0]+45,pos[1]+4,18,18))
            font.render_to(screen, (pos[0]+5,pos[1]+5), n.name, (0, 0, 0))

def DrawSignals():
    px,py=90,70
    sx=10
    barheight=450
    for x in range(200):
        ppx,ppy=px + x * sx,py - 70
        if x%10==0:
            rect(screen, (180,180,180), (ppx,ppy,2,barheight+30))
            font.render_to(screen, (ppx+5,ppy+5), str(x), (255, 255, 255))
        else:
            rect(screen, (100,100,100), (ppx,ppy + 30,2,barheight))
        
    for m,h in historic.items():
        if m not in childs:
            continue
        rect(screen, coltype[m.type], (px-75,py,70,28))
        font.render_to(screen, (px-70,py+5), m.name, (0, 0, 0))
        for t,r in h.items():
            for i,f in enumerate(r):
                rect(screen, (0,255,0) if f else (255,0,0), (px + t * sx + i*4,py,2,40))
        py += 50

def DrawLowList():
    px,py=90,670
    for m in modules.values():
        if m not in childs:
            continue
        rect(screen, coltype[m.type], (px-75,py,70,28))
        font.render_to(screen, (px-70,py+5), m.name, (0, 0, 0))
        strlist=str(m.lowlist)
        font.render_to(screen, (px,py+5), strlist, (255, 255, 255))
        
        py += 50

def CreateGame():
    run = True
    while run:
        #for bp in range(1): ButtonPress()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    run = False
        screen.fill((30, 0, 0))
        font.render_to(screen, (5,5), str(presses), (255, 255, 255))
        DrawGraph()
        DrawLowList()
        DrawSignals()
        pygame.display.update()
    pygame.quit()

CreateGame()
#Part1()
#Part2()