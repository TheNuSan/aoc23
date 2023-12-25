import os
import math
import networkx as nx
import matplotlib.pyplot as plt

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_25_1.txt"), "r").read().split("\n")

class Component:
    name="Empty"
    links=[]
    def __init__(self,name):
        self.name=name
        self.links=[]
    def __str__(self) -> str:
        return self.name + " " + str(self.links)
    def __repr__(self) -> str:
        return self.name

gra = nx.Graph()

comps={}
for l in lines:
    pa=l.split(": ")
    ca=comps.get(pa[0], None)
    if not ca:
        gra.add_node(pa[0])
        ca = Component(pa[0])
        comps[ca.name] = ca
    for x in pa[1].split():
        co=comps.get(x, None)
        if not co:
            gra.add_node(x)
            co = Component(x)
            comps[co.name] = co
        ca.links.append(co)
        co.links.append(ca)
        gra.add_edge(pa[0],x)

is_real_deal=True
if is_real_deal:
    gra.remove_edge("jxd","bbz")
    gra.remove_edge("glz","mxd")
    gra.remove_edge("clb","brd")
else:
    gra.remove_edge("pzl","hfx")
    gra.remove_edge("nvd","jqt")
    gra.remove_edge("cmg","bvb")

#print("\n".join(str(x) for x in comps.values()))
subs=nx.connected_components(gra)
lens=[len(x) for x in subs]
print(", ".join(str(x) for x in lens))
print("Result:",math.prod(lens))

# visualize the graph
#nx.draw(gra, with_labels=True, font_weight='bold', node_size=600, node_color='#aaaaaa')
#plt.show()