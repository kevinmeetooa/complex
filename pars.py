#!/usr/bin/python3
import graph as gr
def read_file(filepath):
    l=[]
    l2=[]
    boolsommet=False
    boolaretes=False
    with open(filepath) as fp:
       for line in fp:
           values = line.split()
           if (values[0]=="Sommets"):
               boolsommet=True
               continue
           if (values[0]=="Aretes"):
               boolaretes=True
               continue
           if (values[0]=="Nombre" and values[2]=="aretes"):
               boolsommet=False
               continue
           if (boolsommet==True):
               l.append(int(values[0]))
           if (boolaretes==True):
               l2.append((int(values[0]),int(values[1])))
    return l,l2

def graph_fromFile(filepath):
  nodes,edges=read_file(filepath)
  g=gr.Graph()
  for u in nodes:
    g.add_node(u)
  for e in edges:
    g.add_edge(e[0],e[1],0)
  return g
    
