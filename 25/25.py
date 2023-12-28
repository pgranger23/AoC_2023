import networkx as nx
import numpy as  np

def parse_input(fname:str):
    with open(fname, 'r') as f:
        lines = f.readlines()

    graph = nx.Graph()
    for line in lines:
        node, lines = line.strip('\n').split(':')
        for node2 in lines.strip(' ').split(' '):
            graph.add_edge(node, node2)
    return graph

def prob1():
    print("##########First part of the problem##########")
    graph = parse_input('input.1')
    nx.draw(graph)
    to_remove = nx.minimum_edge_cut(graph)
    graph.remove_edges_from(to_remove)
    result = np.prod([len(g) for g in nx.connected_components(graph)])
    print(f"Result is: {result}")




def prob2():
    print("##########Second part of the problem##########")

if __name__ == '__main__':
    prob1()
    prob2()
