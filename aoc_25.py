import os
import math
import networkx as nx
import matplotlib.pyplot as plt

wd=os.path.dirname(os.path.realpath(__file__))
lines = open(os.path.join(wd,"aoc_25_1.txt"), "r").read().split("\n")

gra = nx.Graph()

comps={}
for l in lines:
    pa=l.split(": ")
    gra.add_node(pa[0])
    for x in pa[1].split():
        gra.add_node(x)
        gra.add_edge(pa[0],x)

# I'm a bit lazy today, let's just use graph ploting with networkx to visualy find the 3 links to break
is_real_deal=True
if is_real_deal:
    gra.remove_edge("jxd","bbz")
    gra.remove_edge("glz","mxd")
    gra.remove_edge("clb","brd")
else:
    gra.remove_edge("pzl","hfx")
    gra.remove_edge("nvd","jqt")
    gra.remove_edge("cmg","bvb")

# then get the two sub-graphs
subs=nx.connected_components(gra)
lens=[len(x) for x in subs]
print(", ".join(str(x) for x in lens))
print("Result:",math.prod(lens))

# visualize the graph
#nx.draw(gra, with_labels=True, font_weight='bold', node_size=600, node_color='#aaaaaa')
#plt.show()