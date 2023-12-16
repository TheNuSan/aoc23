import os

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_16_1.txt"), "r").read().split("\n")

dirs=[[1,0],[0,1],[-1,0],[0,-1]] # right,down,left,up
ref1=[1,0,3,2] # \
ref2=[3,2,1,0] # /
gridx,gridy=len(lines[0]),len(lines)

def init_grid(): return [[[c,[False,False,False,False]] for c in l] for l in lines]

def draw_grid(grid):
    print("==============================")
    dirsc=">v<^"
    for x in grid:
        st=""
        for g in x:
            if g[0]!=".":
                st+=g[0]
                continue
            num=g[1].count(True)
            if num==1:
                st+=next(dirsc[i] for i in range(4) if g[1][i])
            elif num>1:
                st+=str(num)
            else:
                st+=g[0]
        print(st)

def count_energy(grid): return sum(1 if g[1].count(True)>0 else 0 for x in grid for g in x)

def get_ray(r,dir): return [[r[0][0]+dirs[dir][0], r[0][1]+dirs[dir][1]],dir]

def simu(rays):
    grid=init_grid()
    while len(rays)>0:
        nr=[]
        for r in rays:
            if r[0][0]<0 or r[0][0]>=gridx or r[0][1]<0 or r[0][1]>=gridy:
                continue
            g = grid[r[0][1]][r[0][0]]
            c,dir=g[0],r[1]
            if g[1][dir]: # already visited
                continue
            g[1][dir] = True
            if c=='.' or (c=='|' and (dir==1 or dir==3)) or (c=='-' and (dir==0 or dir==2)):
                nr.append(get_ray(r,dir))
            elif c=='\\':
                nr.append(get_ray(r,ref1[dir]))
            elif c=='/':
                nr.append(get_ray(r,ref2[dir]))
            elif c=='|':
                nr.append(get_ray(r,1))
                nr.append(get_ray(r,3))
            elif c=='-':
                nr.append(get_ray(r,0))
                nr.append(get_ray(r,2))
        rays=nr
        #draw_grid(grid)
    #draw_grid(grid)
    return count_energy(grid)
            
# Part 1, top left
part1 = simu([[[0,0],0]])
print("Part 1:",part1)

mostenergy=0
for x in range(gridx): mostenergy=max(mostenergy,simu([[[x,0],1]])) # top row
for x in range(gridx): mostenergy=max(mostenergy,simu([[[x,gridy-1],3]])) # bottom row
for y in range(gridy): mostenergy=max(mostenergy,simu([[[0,y],0]])) # left column
for y in range(gridy): mostenergy=max(mostenergy,simu([[[gridx-1,y],2]])) # right column

print("Part 2:",mostenergy)
