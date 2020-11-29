#!/usr/bin/python3
from pars import graph_fromFile
from display import drawGraph
from collections import deque
from graph import rndm
from graph import algo_matching
from graph import algo_greedy
import time
import numpy as np
import matplotlib.pyplot as plt
import math
import random

def stat_rndm(nmax,p,inst,inter):
    stat=np.zeros(shape=(inter,inst))
    for i in range(1,inter+1):
        for j in range(1,inst+1):
            start_time = time.time()
            g=rndm(int(i*nmax/(inter+1)),p)
            end_time = time.time()
            stat[i-1,j-1]= end_time -start_time
    return np.mean(stat,axis=1)

def display_time_matching_vs_greedy(nmax,p,p2,inst,inter):  
    stat=np.zeros(shape=(inter,inst))
    stat2=np.zeros(shape=(inter,inst))
    stat3=np.zeros(shape=(inter,inst))
    stat4=np.zeros(shape=(inter,inst))
    for i in range(1,inter+1):
        for j in range(1,inst+1):
            g=rndm(int(i*nmax/(inter+1)),p)
            start_time = time.time()
            algo_matching(g)
            end_time = time.time()
            start_time2 = time.time()
            algo_greedy(g)
            end_time2 = time.time()
            g2=rndm(int(i*nmax/(inter+1)),p2)
            start_time3 = time.time()
            algo_matching(g2)
            end_time3 = time.time()
            start_time4 = time.time()
            algo_greedy(g2)
            end_time4 = time.time()
            stat[i-1,j-1]= end_time -start_time
            stat2[i-1,j-1]= end_time2 -start_time2
            stat3[i-1,j-1]= end_time3 -start_time3
            stat4[i-1,j-1]= end_time4 -start_time4
    stat,stat2,stat3,stat4=np.mean(stat,axis=1),np.mean(stat2,axis=1),np.mean(stat3,axis=1) ,np.mean(stat4,axis=1) 
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat4),label='Algorithme glouton, p='+str(p2))
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat2),label='Algorithme glouton, p='+str(p))
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat3),label='Algorithme de couplage, p='+str(p2))
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat),label='Algorithme de couplage, p='+str(p))
    plt.legend()
    plt.yscale("log")
    plt.ylabel('Moyenne de temps d\'exécution (s)')
    plt.xlabel('Taille des instances de graphe (nb de sommets)')
    plt.title("Durée d'exécution des algorithmes couplage et glouton ")
    plt.show()
    
def display_size_matching_vs_greedy(nmax,p,p2,inst,inter):
    plt.figure()
    ax = plt.subplot(111)
    width=5
    stat=np.zeros(shape=(inter,inst))
    stat2=np.zeros(shape=(inter,inst))
    stat3=np.zeros(shape=(inter,inst))
    stat4=np.zeros(shape=(inter,inst))
    for i in range(1,inter+1):
        for j in range(1,inst+1):
            g=rndm(int(i*nmax/(inter+1)),p)
            m=len(algo_matching(g))
            n=len(algo_greedy(g))
            g2=rndm(int(i*nmax/(inter+1)),p2)
            q=len(algo_matching(g2))
            r=len(algo_greedy(g2))
            stat[i-1,j-1]= m
            stat2[i-1,j-1]= n
            stat3[i-1,j-1]= q
            stat4[i-1,j-1]= r
    stat,stat2,stat3,stat4=np.mean(stat,axis=1),np.mean(stat2,axis=1),np.mean(stat3,axis=1) ,np.mean(stat4,axis=1) 
    ax.bar([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat2),width,label='Algo glouton, p='+str(p))
    ax.bar([int(i*nmax/(inter+1))+width for i in range(1,inter+1)],list(stat3),width,label='Algo glouton, p='+str(p2))
    ax.bar([int(i*nmax/(inter+1))+2*width for i in range(1,inter+1)],list(stat),width,label='Algo couplage, p='+str(p))
    ax.bar([int(i*nmax/(inter+1))+3*width for i in range(1,inter+1)],list(stat4),width,label='Algo couplage, p='+str(p2))
    plt.legend()
    plt.ylabel('Taille de la couverture renvoyée')
    plt.xlabel('Taille des instances de Graph (nb de sommets)')
    plt.show()

def find_couv(g,c_opt,c_curent):
    e=g.first_edge()
    if e is not None:
        i,j=e
        gi=g.copy()
        gi.delete_node(i)
        gj=g.copy()
        gj.delete_node(j)
        c_i=c_curent.copy()
        c_i.add(i)
        c_j=c_curent.copy()
        c_j.add(j)
        find_couv(gi,c_opt,c_i)
        find_couv(gj,c_opt,c_j)
    else:
        if len(c_curent) < len(c_opt):
            c_opt.clear()
            c_opt.update(c_curent)

def branch_covering(g):
    c_opt=set(g._nodes)
    c_curent=set()
    find_couv(g,c_opt,c_curent)
    return c_opt

def find_couv_born(g,c_opt,c_curent):
    binf=g.graph_lower_bound()+len(c_curent)
    solrea=algo_greedy(g)+list(c_curent)
    bsup=len(solrea)
    if (bsup<len(c_opt)):
        c_opt.clear()
        c_opt.update(solrea)
        
    if binf<len(c_opt) and (binf<bsup):
        e=g.first_edge()
        if e is not None:
            i,j=e
            gi=g.copy()
            gi.delete_node(i)
            gj=g.copy()
            gj.delete_node(j)
            c_i=c_curent.copy()
            c_i.add(i)
            c_j=c_curent.copy()
            c_j.add(j)
            binfi=gi.graph_lower_bound()+len(c_i)
            binfj=gj.graph_lower_bound()+len(c_j)
                
            if binfi<binfj :
                find_couv_born(gi,c_opt,c_i)
                find_couv_born(gj,c_opt,c_j)
            else:
                find_couv_born(gj,c_opt,c_j)
                find_couv_born(gi,c_opt,c_i)
        else:
            if len(c_curent) < len(c_opt):
                c_opt.clear()
                c_opt.update(c_curent)

def branch_bound_covering(g):
    c_opt=set(g._nodes)
    c_curent=set()
    find_couv_born(g,c_opt,c_curent)
    return c_opt

def find_couv_born_imp1(g,c_opt,c_curent):
    binf=g.graph_lower_bound()+len(c_curent)
    solrea=algo_greedy(g)+list(c_curent)
    bsup=len(solrea)
    if (bsup<len(c_opt)):
        c_opt.clear()
        c_opt.update(solrea)
        
    if binf<len(c_opt) and (binf<bsup):
        e=g.first_edge()
        if e is not None:
            i,j=e
            gi=g.copy()
            gi.delete_node(i)
            gj=g.copy()
            gj.delete_node(j)
            c_i=c_curent.copy()
            c_i.add(i)
            c_j=c_curent.copy()
            c_j.add(j)
            binfi=gi.graph_lower_bound()+len(c_i)
            binfj=gj.graph_lower_bound()+len(c_j)
                
            if binfi<binfj :
                find_couv_born_imp1(gi,c_opt,c_i)
                c_j.update(set(gj._out[i]))
                gj.delete_nodes([i]+gj._out[i])
                find_couv_born_imp1(gj,c_opt,c_j)
            else:
                find_couv_born_imp1(gj,c_opt,c_j)
                c_i.update(set(gi._out[j]))
                gi.delete_nodes([j]+gi._out[j])
                find_couv_born_imp1(gi,c_opt,c_i)
        else:
            if len(c_curent) < len(c_opt):
                c_opt.clear()
                c_opt.update(c_curent)

def branch_bound_covering_imp1(g):
    c_opt=set(g._nodes)
    c_curent=set()
    find_couv_born_imp1(g,c_opt,c_curent)
    return c_opt
    
    
def find_couv_born_imp2(g,c_opt,c_curent):
    binf=g.graph_lower_bound()+len(c_curent)
    solrea=algo_greedy(g)+list(c_curent)
    bsup=len(solrea)
    if (bsup<len(c_opt)):
        c_opt.clear()
        c_opt.update(solrea)
        
    if binf<len(c_opt) and (binf<bsup):
        e=g.first_edge()
        if e is not None:
            i,j=e
            degi=len(g._out[i])
            degj=len(g._out[j])
            gi=g.copy()
            gi.delete_node(i)
            gj=g.copy()
            gj.delete_node(j)
            c_i=c_curent.copy()
            c_i.add(i)
            c_j=c_curent.copy()
            c_j.add(j)
            binfi=gi.graph_lower_bound()+len(c_i)
            binfj=gj.graph_lower_bound()+len(c_j)
                
            if binfi<binfj or degi>degj:
                find_couv_born_imp2(gi,c_opt,c_i)
                c_j.update(set(gj._out[i]))
                gj.delete_nodes([i]+gj._out[i])
                find_couv_born_imp2(gj,c_opt,c_j)
            else:
                if binfi>binfj or degi<degj:
                    find_couv_born_imp2(gj,c_opt,c_j)
                    c_i.update(set(gi._out[j]))
                    gi.delete_nodes([j]+gi._out[j])
                    find_couv_born_imp2(gi,c_opt,c_i)
        else:
            if len(c_curent) < len(c_opt):
                c_opt.clear()
                c_opt.update(c_curent)

def branch_bound_covering_imp2(g):
    c_opt=set(g._nodes)
    c_curent=set()
    find_couv_born_imp2(g,c_opt,c_curent)
    return c_opt


def iterative_branch_covering(g):
    c_opt=np.linspace(0,1,len(g._out)+1)
    stack = deque([g]) 
    if g is None:
        return
    while stack: 
        gcurrent = stack.pop() 
        e=gcurrent.first_edge() 
        if e is None:
            if (len(gcurrent._visites) < len(c_opt)):
                c_opt=set(gcurrent._visites)
        else:
            i,j=e
            gi,gj=gcurrent.copy(),gcurrent.copy()
            gi.delete_node(i)
            gj.delete_node(j)
            gi._visites.append(i)
            gj._visites.append(j)
            stack.extend([gj,gi])
    return c_opt
    

def iterative_branch_and_bound(g):
    global minactuel
    c_opt=np.linspace(0,1,len(g._out)+1)
    stack = deque([g]) 
    if g is None:
        return
    while stack:         
        gcurrent = stack.pop() 
        #print("graphe actuel:")
        #print(gcurrent._out)
        e=gcurrent.first_edge() 
        visites=gcurrent._visites
        solrea=algo_greedy(gcurrent)+visites
        #print("minactuel: "+str(minactuel))
        #print("SOLREA --------")
        #print(solrea)
        bornesup=len(solrea)
        borneinf=gcurrent.graph_lower_bound()+len(visites)
        #print("Borne inf:")
        #print(borneinf)
        if (borneinf>=minactuel):
            #print(borneinf)
            #print(minactuel)
            continue
        #if (bornesup>minactuel):
        #    continue
        if (bornesup<len(c_opt)):
            c_opt=set(solrea)
            minactuel=bornesup
        if (bornesup<borneinf):
            c_opt=set(solrea)
            minactuel=bornesup
        #print("Borne inf: "+str(borneinf))
        if e is None:
            if (len(gcurrent._visites) < len(c_opt)):
                c_opt=set(gcurrent._visites)
            if (borneinf<minactuel):
                minactuel=borneinf
        else:
            i,j=e
            #print("(i,j): "+str((i,j)))
            gi,gj=gcurrent.copy(),gcurrent.copy()
            gi.delete_node(i)
            gj.delete_node(j)
            gi._visites.append(i)
            gj._visites.append(j)
            binfi=gi.graph_lower_bound()
            binfj=gj.graph_lower_bound()
            #print("binfi, binfj: "+str(binfi)+" "+str(binfj))
            #print(gi._out)
            #print(gj._out)
            if (binfi<binfj):
                stack.extend([gj,gi])
            else:
                stack.extend([gi,gj])
    return c_opt    
    
def display_with_vs_without_bounds(nmax,p,inst,inter):
    stat=np.zeros(shape=(inter,inst))
    stat2=np.zeros(shape=(inter,inst))
    for i in range(1,inter+1):
        for j in range(1,inst+1):
            g=rndm(int(i*nmax/(inter+1)),p)
            start_time = time.time()
            branch_covering(g)
            end_time = time.time()
            start_time2 = time.time()
            branch_bound_covering(g)
            end_time2 = time.time()
            stat[i-1,j-1]= end_time -start_time
            stat2[i-1,j-1]= end_time2 -start_time2
    stat=np.mean(stat,axis=1)
    stat2=np.mean(stat2,axis=1)
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat),label='Branchement sans bornes')
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat2),label='Branchement avec bornes')
    plt.legend()
    plt.yscale("log")
    plt.ylabel('Moyenne de temps d\'exécution (s)')
    plt.xlabel('Taille des instances de graphe (nb de sommets)')
    plt.title("Durée d'exécution de l'algorithme de branchement")
    plt.show()
    
def display_without_bounds(nmax,p,p2,inst,inter):
    stat=np.zeros(shape=(inter,inst))
    stat2=np.zeros(shape=(inter,inst))
    for i in range(1,inter+1):
        for j in range(1,inst+1):
            g=rndm(int(i*nmax/(inter+1)),p)
            start_time = time.time()
            branch_covering(g)
            end_time = time.time()
            start_time2 = time.time()
            g=rndm(int(i*nmax/(inter+1)),p2)
            branch_covering(g)
            end_time2 = time.time()
            stat[i-1,j-1]= end_time -start_time
            stat2[i-1,j-1]= end_time2 -start_time2
    stat=np.mean(stat,axis=1)
    stat2=np.mean(stat2,axis=1)
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat),label='p='+str(p))
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat2),label='p='+str(p2))
    plt.legend()
    plt.yscale("log")
    plt.ylabel('Moyenne de temps d\'exécution (s)')
    plt.xlabel('Taille des instances de graphe (nb de sommets)')
    plt.title("Durée d'exécution de l'algorithme de branchement")
    plt.show()    
    
    
def display_bb_vs_imp1(nmax,p,inst,inter):
    stat=np.zeros(shape=(inter,inst))
    stat2=np.zeros(shape=(inter,inst))
    for i in range(1,inter+1):
        for j in range(1,inst+1):
            n=int(i*nmax/(inter+1))
            g=rndm(n,1/np.sqrt(n))
            start_time = time.time()
            branch_bound_covering(g)
            end_time = time.time()
            start_time2 = time.time()
            branch_bound_covering_imp1(g)
            end_time2 = time.time()
            stat[i-1,j-1]= end_time -start_time
            stat2[i-1,j-1]= end_time2 -start_time2
    stat=np.mean(stat,axis=1)
    stat2=np.mean(stat2,axis=1)
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat),label='Branchement avec bornes')
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat2),label='Branchement avec bornes amélioré')
    plt.legend()
    plt.yscale('log')
    plt.ylabel('Moyenne de temps d\'exécution (s)')
    plt.xlabel('Taille des instances de graphe (nb de sommets)')
    plt.title("Durée d'exécution de l'algorithme de branchement")
    plt.show() 
    
def display_imp1_vs_imp2(nmax,p,inst,inter):
    stat=np.zeros(shape=(inter,inst))
    stat2=np.zeros(shape=(inter,inst))
    for i in range(1,inter+1):
        for j in range(1,inst+1):
            n=int(i*nmax/(inter+1))
            g=rndm(n,1/np.sqrt(n))
            start_time = time.time()
            branch_bound_covering_imp1(g)
            end_time = time.time()
            start_time2 = time.time()
            branch_bound_covering_imp2(g)
            end_time2 = time.time()
            stat[i-1,j-1]= end_time -start_time
            stat2[i-1,j-1]= end_time2 -start_time2
    stat=np.mean(stat,axis=1)
    stat2=np.mean(stat2,axis=1)
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat),label='Branchement avec bornes amélioré')
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat2),label='Nouvel algorithme')
    plt.legend()
    plt.yscale("log")
    plt.ylabel('Moyenne de temps d\'exécution (s)')
    plt.xlabel('Taille des instances de graphe (nb de sommets)')
    plt.title("Durée d'exécution de l'algorithme de branchement")
    plt.show()     
    
def display_comp(nmax,inst,inter):
    stat=np.zeros(shape=(inter,inst))
    stat2=np.zeros(shape=(inter,inst))
    stat3=np.zeros(shape=(inter,inst))
    stat4=np.zeros(shape=(inter,inst))
    for i in range(1,inter+1):
        for j in range(1,inst+1):
            n=int(i*nmax/(inter+1))
            start_time = time.time()
            #g=rndm(n,0.01)
            end_time = time.time()
            start_time2 = time.time()
            g=rndm(n,0.1)
            end_time2 = time.time()
            start_time3 = time.time()
            g=rndm(n,0.5)
            end_time3 = time.time()
            start_time4 = time.time()
            g=rndm(n,0.9)
            end_time4 = time.time()
            #stat[i-1,j-1]= end_time -start_time
            stat2[i-1,j-1]= np.sqrt(end_time2 -start_time2)
            stat3[i-1,j-1]= np.sqrt(end_time3 -start_time3)
            stat4[i-1,j-1]= np.sqrt(end_time4 -start_time4)
    #stat=np.mean(stat,axis=1)
    stat2=np.mean(stat2,axis=1)
    stat3=np.mean(stat3,axis=1)
    stat4=np.mean(stat4,axis=1)
    #plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat),label='p=0.01')
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat2),label='p=0.1 (sqrt)')
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat3),label='p=0.5')
    plt.plot([int(i*nmax/(inter+1)) for i in range(1,inter+1)],list(stat4),label='p=0.9')
    plt.legend()
    #plt.yscale("log")
    plt.ylabel('Moyenne des racines carrées des temps d\'exécution (s)')
    plt.xlabel('Taille des instances de graphe (nb de sommets)')
    plt.title("Temps de génération d'instances aléatoires de graphe")
    plt.show()     
    

    
    
if __name__ == "__main__":
  minactuel=np.Infinity
  #g=Graph()
  inter=10 #nombre de taille differentes d'instance
  nmax=150 # taille max d'une instance
  inst=20 #nombre d'instance d'une taille donnée
  p=0.5 # parametre de construction d'un graph aléatoire
  g=graph_fromFile("file.txt")
  g=rndm(25,1/math.sqrt(25))
  print(len(g))
  print(g._nodes)
  print(g._out)
  print(g._weight)
  print("degree :")
  a=g.degree()
  print(a)
  print(g.node_degMax())
  g1=g.copy()
  
  
  #drawGraph(g1)

  g1.delete_nodes(['3','4'])
  print("G1:--------")
  print(g1._nodes)
  print(g1._out)
  print(g1._weight)
  print("degree :")
  a=g1.degree()
  print(a)

  
  """print("Couplage naif")
  print(algo_matching(g1))
  
  print("Couplage glouton")
  print(algo_greedy(g1))
  
  print("Branchement récursif")
  print(branch_covering(g1))
  """
  
  
  """
  #Branchement récursif
  
  
  print("Branchement récursif")
  start=time.time()
  a=branch_covering(g)
  end=time.time()
  print(str(a)+" Taille de la solution: "+str(len(a))+" tps: "+str(end-start))
  print("Branchement itératif")
  start=time.time()
  a=iterative_branch_covering(g)
  end=time.time()
  print(str(a)+" Taille de la solution: "+str(len(a))+" tps: "+str(end-start))
  
  """
  #Branch and bound itératif
  
  #drawGraph(g1)
  
  display_time_matching_vs_greedy(300,0.2,0.8,inst,inter)
  #display_size_matching_vs_greedy(250,0.2,0.8,inst,inter)
  n=18
  #display_without_bounds(n,0.2,0.8,inst,inter)
  #display_with_vs_without_bounds(n,1/np.sqrt(n),inst,inter)
  n2=24
  #display_bb_vs_imp1(n2,1/np.sqrt(n2),inst,inter)
  n3=45
  #display_imp1_vs_imp2(n3,1/np.sqrt(n3),inst,inter)
  #display_comp(n3,inst,inter)