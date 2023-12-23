import os
import math

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_23_1.txt"), "r").read().split("\n")
gridx,gridy=len(lines[0]),len(lines)

names="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

nodecount=0
class Node:
    name=""
    x=0
    y=0
    all=[]
    outputs=[]
    def __init__(self,x,y):
        global nodecount
        self.name=names[nodecount%len(names)]
        nodecount+=1
        self.x=x
        self.y=y
        self.all=[]
        self.outputs=[]
    def __str__(self):
        #return self.name+":("+str(self.x)+", "+str(self.y)+") out: "+str(self.outputs)+" all: "+str(self.all)
        return self.name+" out: "+', '.join(x[0].name+"("+str(x[1])+")" for x in self.outputs)+" all: "+', '.join(x[0].name+"("+str(x[1])+")" for x in self.all)
    def __repr__(self):
        #return self.name+":("+str(self.x)+", "+str(self.y)+")"
        return self.name
    
nodes={}
graph=[]
start=Node(1,0)
end=Node(gridx-2,gridy-1)

nodes[(start.x,start.y)]=start
nodes[(end.x,end.y)]=end

dirs=[(-1,0),(0,-1),(1,0),(0,1)]
symbol="<^>v"

is_part_1 = False

def append_biggest(l,v,d):
    for i,x in enumerate(l):
        if x[0]==v:
            l[i]=(v,max(x[1],d))
            return
    l.append((v,d))

def find_nodes():
    #maze=[[x for x in y] for y in lines]
    towalk=[(start.x,start.y,start,0,1)]
    while len(towalk)>0:
        x,y,nxt,dist,prevdir=towalk.pop()
        outlist=[]
        for d in range(4):
            if d==prevdir: continue
            x2,y2=x+dirs[d][0],y+dirs[d][1]
            if x2<0 or x2>=gridx or y2<0 or y2>=gridy: continue
            c=lines[y2][x2]
            if c == '#': continue
            if is_part_1 and c != '.' and c!=symbol[d]: continue
            outlist.append((x2,y2,(d+2)%4))
        if len(outlist)==0:
            # found end?
            nn=nodes.get((x,y), None)
            if not nn:
                print("ERROR false end found")
            append_biggest(nxt.outputs, nn, dist)
            append_biggest(nxt.all, nn, dist)
            append_biggest(nn.all, nxt, dist)
        elif len(outlist)==1:
            #maze[y][x]=symbol[(outlist[0][2]+2)%4]
            towalk.append((outlist[0][0],outlist[0][1],nxt,dist+1,outlist[0][2]))
        elif len(outlist)>1:
            #maze[y][x]='o'
            nn=nodes.get((x,y), None)
            if not nn:
                nn=Node(x,y)
                nodes[(x,y)]=nn
                for x2,y2,d in outlist:
                    towalk.append((x2,y2,nn,1,d))
            append_biggest(nxt.outputs, nn, dist)
            append_biggest(nxt.all, nn, dist)
            append_biggest(nn.all, nxt, dist)
    #for n in nodes.values(): maze[n.y][n.x]=n.name
    #for y in maze: print(''.join(x for x in y))

find_nodes()

def find_longuest_steep():
    towalk=[(start,0)]
    paths=[]
    while len(towalk):
        nxt,dist=towalk.pop()
        for nn,d in nxt.outputs:
            towalk.append((nn,dist+d))
            if nn == end:
                paths.append(dist+d)
    print("Part 1:",max(paths))
    #print(sorted(paths, reverse=True))

def find_longuest_all():
    towalk=[(start,0,[start])]
    longuest=0
    pathfound=0
    while len(towalk):
        nxt,dist,hist=towalk.pop()
        for nn,d in nxt.all:
            if nn not in hist:
                towalk.append((nn,dist+d,hist+[nn]))
                if nn == end:
                    #print("path:",hist+[nn],dist+d)
                    pathfound+=1
                    longuest=max(longuest, dist+d)
    print("Part 2:",longuest)
    #print("paths found:",pathfound)
    #print(sorted(paths, reverse=True))

print(len(nodes)) 
# 1262816 too high

if is_part_1:
    find_longuest_steep()
else:
    find_longuest_all()

#print('\n'.join(str(x) for x in nodes.values()))