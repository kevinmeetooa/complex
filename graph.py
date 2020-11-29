#!/usr/bin/python3
import copy
import random 
from collections import deque
import numpy as np
import math

class Graph:
  def __init__(self,nodes=None,edges=None,weights=None,visites=None):
    if (nodes is not None and edges is not None) and weights is not None and visites is not None:
      self._nodes=nodes
      self._out=edges
      self._weight=weights
      self._visites=visites
    else:
      self._nodes=[]
      self._out=dict()
      self._weight=dict()
      self._visites=[]
  
  def __len__(self):
    return len(self._nodes)
  
  def __iter__(self):
    return iter(self._nodes)
  
  def add_node(self,u):
    if u not in self._nodes:
      self._nodes.append(u)
      self._out[u]=[]
  
  def add_edge(self,u,v,weight=None):
    if u not in self._nodes:
     self.add_node(u)
    if v not in self._nodes:
      self.add_node(v)
    if v not in self._out[u]:
        self._out[u].append(v)
    if u not in self._out[v]:
        self._out[v].append(u)
    self._weight.update({(u,v):weight})
    self._weight.update({(v,u):weight})
  
  def delete_node(self,u):
    if u in self._nodes:
      self._nodes.remove(u)
      del self._out[u]

      for k in self._out:
        if u in self._out[k]:
          self._out[k].remove(u)
      
      l=[ k for k in self._weight if u in k]
      for e in l:
        del self._weight[e]
  
  def delete_nodes(self,l):
    for e in l:
      self.delete_node(e)
  
  def degree(self):
    l=[len(self._out[u]) for u in self._nodes ]
    return l

  def node_degMax(self):
    l=self.degree()
    deg_max=max(l)
    return self._nodes[l.index(deg_max)]
    
  def getDegMax(self):
    l=self.degree()
    if (l==[]):
      return 0
    return max(l)
      
  def copy(self):
    return Graph(copy.deepcopy(self._nodes),
                copy.deepcopy(self._out),
                copy.deepcopy(self._weight),
                copy.deepcopy(self._visites))
  def first_edge(self):
    if sum(self.degree())==0:
        return None
    for k in self._out:
        if len(self._out[k])!=0:
            return (k,self._out[k][0])
            
  def edge_number(self):
    i=0
    gcopy=self.copy()
    for u in gcopy._nodes:
      for k in gcopy._out:
        if u in gcopy._out[k]:
          gcopy._out[k].remove(u)
          i+=1
      del gcopy._out[u]
    return i
    

  def graph_lower_bound(self):
      m=self.edge_number()
      n=len(self._nodes)
      delta=self.getDegMax()
      #print("m, n, delta: "+str(m)+" "+str(n)+" "+str(delta))
      #print("taille couplage: "+str(len(algo_matching(self))/2))
      b3=0.5*(2*n-1-np.sqrt((2*n-1)*(2*n-1)-8*m))
      b3=math.ceil(b3)
      if (delta==0):
        return 0
      borneinf=max(math.ceil(m/delta),len(algo_matching(self))/2,b3)
      return borneinf

        
  
def rndm(n,p):
      g=Graph()
      for i in range(1,n+1):
          for j in range(1,n+1):
              if i!=j:
                  r=random.randint(1,100)
                  if r<=p*100:
                      g.add_edge(i,j,0)
                  else:
                      g.add_node(i)
                      g.add_node(j)
      return g
    
def algo_matching(g):
    c=[]
    for k in g._out:
        for e in g._out[k]:
            if e not in c and k not in c:
                c.append(k)
                c.append(e)
    return c
            
def algo_greedy(g):
    g1=g.copy()
    c=[]
    while sum(g1.degree()) != 0:
        s=g1.node_degMax()
        c.append(s)
        g1.delete_node(s)
    return c
        

    
