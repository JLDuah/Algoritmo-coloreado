# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 11:02:49 2014

@author: user
"""

import random as rn
import simpy
import networkx as nx


SIM_TIME = 20

class Node:
    n = 0  # Variable static de la clase
    states = ['Isolated', 'Legal', 'Illegal', 'NoColour']  # estados posibles del nodo
    colours = ['rojo', 'azul', 'verde']  # colores.Futuro:obtenidos de argum. en shell
    N = 5  # número de nodos. Futuro: también de argum. en shell
    G = nx.barabasi_albert_graph(N, N - 1)  # Grafo en el que se aplica el algoritmo
    nodesList = G.nodes()  # lista de los nodos con indices (del array) coincidiendo con ellos

    def __init__(self, env):
        self.env = env
        # En la inicialización, escoge el color
        # de menos peso
        self.main_proc = env.process(self.main(env))
        Node.nodesList[Node.n] = self  # Introduzco en la lista de nodos este nodo
        self.info = {'ID': Node.n, 'C': Node.colours[0], 'S': Node.states[0],
                     'AW': 0, 'NeighIDs_A': [],
                     'N_AgAdW_A': dict()}
        # Node.G.add_node(Node.n,self.info) --> Por si luego quiero utilizar mejor networkx
        Node.n += 1
        self.Interval = 0.9 + rn.random()  # Simulo us (microseg.) para el tiempo simulado
        # Esta variable establece el instante de comienzo de trans.
        # También podría poner: randint(900000,1000000) (Preguntar)
        self.info['NeighIDs_A'].extend(Node.G.neighbors(self.info['ID']))
        # self.info['Neighbour_AgeAdjustedWeights_Array'] = Peso de los vecinos. Incorporar un temporizador
        # a cada uno de 3M, para saber si es válida la info.
        for i in Node.G.neighbors(self.info['ID']):
            self.info['N_AgAdW_A'][i] = 0

    def node_calc_weight(self):  # función para calcular el peso
        if self.info['S'] == Node.states[1]:
            self.info['AW'] = len(Node.G.neighbors(self.info['ID'])) + rn.random()
        elif self.info['S'] == Node.states[2]:
            self.info['AW'] = rn.random()
        else:
            """Código restante de la función"""

    def send_messages(self, env):
        for i in self.info['NeighIDs_A']:
            self.advise_neigh(i, env)
            # avisar al nodo receptor que se le envía un mensaje y lo tiene que procesar

    def advise_neigh(self, id, env):
        if Node.nodesList[id].info['N_AgAdW_A'][self.info['ID']] == 0:  # Observar si el vector está vacio
            Node.nodesList[id].info['N_AgAdW_A'][self.info['ID']] = {
                'NID': id,
                'W': self.info['AW'],
                'C': self.info['C'],
                'S': self.info['S'],
                'NoN': len(Node.G.neighbors(id)),
                'FMLST': 0,
                'TS': env.now}
            """if self.info['C'] == self.info['N_AgAdW_A']['C']:  # Clash
                self.clash(id)"""
        else:  # Si no es nueva la entrada, solo cambio unos campos
            self.info['N_AgAdW_A'][id]['W'] = Node.nodesList[id].info['AW']
            self.info['N_AgAdW_A'][id]['C'] = Node.nodesList[id].info['C']
            self.info['N_AgAdW_A'][id]['S'] = Node.nodesList[id].info['S']

    def main(self, env):
        while True:
            yield env.timeout(2.5)  # self.Interval
            self.Interval = 0.9 + rn.random()  # recalculo el intervalo de transmisión
            self.send_messages(env)

    def clash(self, id):
        if self.info['AW'] >= self.info['N_AgAdW_A'][id]['W']:
            self.info['S'] = Node.states[1]
            Node.nodesList[id].info['S'] = Node.states[2]
            Node.nodesList[id].info['C'] = Node.colours[0]
        else:
            self.info['S'] = Node.states[2]
            Node.nodesList[id].info['S'] = Node.states[1]
            self.info['C'] = Node.colours[0]

env = simpy.Environment()
Nodo0 = Node(env)
# print(Node.G.neighbors(0))
#print(Nodo0.info)
#print(Nodo0.info['N_AgAdW_A'][4])
#print(Nodo0.Interval)
Nodo1 = Node(env)
#print(Node.G.neighbors(1))
#print(Nodo1.info)
Nodo2 = Node(env)
#print(Node.G.neighbors(2))
#print(Nodo2.info)
Nodo3 = Node(env)
#print(Node.G.neighbors(3))
#print(Nodo3.info)
Nodo4 = Node(env)
#print(Node.G.neighbors(4))
#print(Nodo4.info)
env.run(10)
print('{}\n{}\n{}\n{}\n{}'.format(Nodo0.info,Nodo1.info,Nodo2.info,Nodo3.info,Nodo4.info))
