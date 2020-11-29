#!/usr/bin/python3
import networkx as nx

def drawGraph(g):
    gg=nx.Graph()
    #gg=nx.dodecahedral_graph()

    for k in g._out:
        for e in g._out[k]:
            gg.add_edge(k,e)
    #nx.draw(gg)
    #nx.draw(gg)
    nx.draw(gg,pos=nx.spring_layout(gg)) # use spring layout
    nx.draw_networkx_labels(gg,pos=nx.spring_layout(gg))
        