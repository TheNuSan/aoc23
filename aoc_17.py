import os
import copy
import heapq

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_17_1.txt"), "r").read().split("\n")
grid = [[int(c) for c in l] for l in lines]
gridx,gridy=len(grid[0]),len(grid)

dirs=[[1,0],[0,1],[-1,0],[0,-1]] # right, down, left, up

class Path:
    cost=0
    posx=0
    posy=0
    lastdir=-1
    lastdircount=0
    #histo=[]
    def __str__(self):
        return "Cost:"+str(self.cost)+" ["+str(self.posx)+","+str(self.posy)+"] "+str(self.lastdir)+"|"+str(self.lastdircount)+" Path:"+str(self.histo)
    def printmap(self):
        #for y in range(gridy): print(''.join("■" if (x,y) in self.histo else str(grid[y][x]) for x in range(gridx)))
        print("No histo")
    def totalcost(self):
        return self.cost + abs(self.posx-gridx-1) + abs(self.posy-gridy-1)
    # overload < operator
    def __lt__(self, other):
        return self.totalcost() < other.totalcost()

pool=[Path()]
heapq.heapify(pool)
visited={}

#mindist,maxdist=0,3 # Part 1
mindist,maxdist=3,10 # Part 2

steps=0
end=None
while pool and not end:
    p=heapq.heappop(pool)
    for i,d in enumerate(dirs):
        # direction should not do a 180
        nobacktrack = (i+2)%4!=p.lastdir
        # cannot keep the same direction for too long
        maxlimit = i!=p.lastdir or p.lastdircount<maxdist
        # must keep the same direction at least some number
        minlimit = i==p.lastdir or p.lastdircount>mindist
        if  p.lastdir<0 or (nobacktrack and maxlimit and minlimit):
            # cannot go in a direction, if mindist would make it go outside the limit anyway
            curmindist = (max(0,mindist-p.lastdircount) if i==p.lastdir else mindist) + 1
            # compute final position in at least mindist blocks
            posx,posy = p.posx+d[0]*curmindist, p.posy+d[1]*curmindist            
            if posx<0 or posx>=gridx or posy<0 or posy>=gridy: continue
            ndc=p.lastdircount
            if i!=p.lastdir: ndc=0
            # compute total cost of each steps
            ncost=0
            for j in range(1,curmindist+1):
                ncost+=grid[p.posy+d[1]*j][p.posx+d[0]*j]
                ndc+=1
            vk=(posx,posy,i,ndc)
            if vk in visited: continue
            visited[vk]=True
            np=copy.deepcopy(p)
            #np.histo=copy.deepcopy(p.histo)
            np.cost+=ncost
            np.posx,np.posy=posx,posy
            #np.histo.append((p.posx,p.posy))
            np.lastdir=i
            np.lastdircount=ndc
            if posx==gridx-1 and posy==gridy-1: # goal reached
                #np.histo.append((posx,posy))
                end=np
                break
            #print(np)
            heapq.heappush(pool, np)
            #pool.append(np)
    #pool.sort(key=lambda x: -x.cost) # depth search
    #pool.sort(key=lambda x: -x.totalcost()) # A* search
    steps+=1
    if steps%10000==0:
        if len(pool)>0:
            pp=pool[-1]
            #print("=-----------=")
            #pp.printmap()
            print("Best: "+str(pp.totalcost())+" real:"+str(pp.cost)+" "+str(len(pool)))
    #print(", ".join(str(p) for p in pool))
    #break

print("===============")
if end:
    #print(end)
    end.printmap()
    print("Path found:"+str(end.cost))
else:
    print("No Path Found :(")

