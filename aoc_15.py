import os

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_15_1.txt"), "r").read().split(",")

def hashcode(v):
    seed=0
    for x in v: seed=((seed+ord(x))*17)%256
    #print(v,"=",seed)
    return seed

print("Part 1:",sum(hashcode(x) for x in lines))

boxes=dict()

def printboxes():
    for i,b in boxes.items():
        if len(b)>0:
            print("Box "+str(i)+": "+' '.join("["+str(j)+" "+str(l)+"]" for j,l in b.items()))
    print("")

for x in lines:
    sep=max(x.find('='), x.find('-'))
    label=x[:sep]
    boxid=hashcode(label)
    #print("After \""+x+"\":")
    #print("Label:",label,"Boxid:",boxid," ",x[sep])
    if x[sep]=='=':
        # this dictionary need to be ordered for the algorithm to work
        if boxid not in boxes: boxes[boxid]=dict()
        boxes[boxid][label]=int(x[sep+1:]) # set the lens
    elif boxid in boxes and label in boxes[boxid]:
        del boxes[boxid][label] # remove the label if present
    #printboxes()

part2 = sum(sum((i+1)*(j+1)*b[lk] for j,lk in enumerate(b)) for i,b in boxes.items())
print("Part 2:",part2)