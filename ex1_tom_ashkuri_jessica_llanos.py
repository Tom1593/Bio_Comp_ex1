import networkx as nx
import itertools as itr
import os
import sys
import collections as col


def read_motif_from_file():
    fd = open("subgraphs.txt", 'r')
    motif_list = []
    line = fd.readline()
    while line != '':
        if line.__contains__('#'):
            line = fd.readline()
            line = line.strip('\n')
            motif_list.append(eval(line))
        else:
            line = fd.readline()
    fd.close()
    return motif_list


def find_motif(n):
    u_graph = []
    while True:
        new_edge = input()  # new edge in the form of 1 2
        if not new_edge:
            break
        else:
            edge = (new_edge.split(' ')[0], new_edge.split(' ')[1])
            if edge not in u_graph:
                u_graph.append(edge)

    user_graph = nx.DiGraph()
    user_graph.add_edges_from(u_graph)
    sub_graphs(n)                        # create motif list
    motif_list = read_motif_from_file()  # take the list
    motif_dict = col.OrderedDict()       # the list in alphabetic order
    g_motif_list = []
    for motif in motif_list:             # initialize motif list
        #trun motif to graph format
        motif_graph = nx.DiGraph()
        motif_graph.add_edges_from(motif)
        g_motif_list.append(motif_graph)
        motif_dict[motif_graph] = 0
    for size in range(n - 1, len(u_graph) + 1):
        u_motifs = list(itr.combinations(u_graph, size))
        for motif in u_motifs:
            new_motif = nx.DiGraph()               # create DirectedGraph object
            new_motif.add_edges_from(motif)        # add edges from subgraph
            if nx.is_weakly_connected(new_motif):  # make sure graph is connected
                for g_motif in motif_dict:
                    if nx.is_isomorphic(g_motif, new_motif):  # scan list and increment counter of isomorphic type
                        motif_dict[g_motif] += 1
                        break
    print_motif_to_file(g_motif_list, n, motif_dict)


def print_motif_to_file(g_motif_list, n, motif_dict):
    if os.path.exists("motif_subgraphs.txt"):
        os.remove("motif_subgraphs.txt")
    fd = open("motif_subgraphs.txt", 'a+')
    sys.stdout = fd
    print('n = ' + str(n) + '\n' + 'count = ' + str(len(g_motif_list)) + '\n')
    i = 1
    for motif in g_motif_list:
        print(f"#{i}")
        # turn motif to graph format
        print(f"count = {motif_dict[motif]}")
        print(motif.edges)
        i += 1
    fd.close()
    sys.stdout.close()


def print_to_file(unique_graphs, n):
    if os.path.exists("subgraphs.txt"):
        os.remove("subgraphs.txt")
    fd = open("subgraphs.txt", 'a+')
    sys.stdout = fd
    print('n = ' + str(n) + '\n' + 'count = ' + str(len(unique_graphs)) + '\n')
    i = 1
    for graph in unique_graphs:
        print(f"#{i}")
        print(graph.edges)
        i += 1
    fd.close()
    sys.stdout.close()


def sub_graphs(n):
    nodes = [node for node in range(1, n + 1)]  # nodes = 1,2,3,...,n
    complete_graph_edges = list(itr.permutations(nodes, 2))	 # all node pair permutations
    complete_graph = nx.DiGraph()
    complete_graph.add_edges_from(complete_graph_edges)

    unique_graphs = [complete_graph]
    for size in range(n - 1, len(complete_graph_edges) + 1):
        subgraphs = list(itr.combinations(complete_graph_edges, size))  # list of combinations of size 2n
        for subgraph in subgraphs:
            candidate_graph = nx.DiGraph()  # create DirectedGraph object
            candidate_graph.add_nodes_from(nodes)  # add nodes
            candidate_graph.add_edges_from(subgraph)  # add edges from subgraph
            if nx.is_weakly_connected(candidate_graph):  # make sure graph is connected
                for graph in unique_graphs:
                    exists_flag = False
                    if nx.is_isomorphic(graph, candidate_graph):  # Scan list to see if same type already exists
                        exists_flag = True
                        break
                if not exists_flag:
                    unique_graphs.append(candidate_graph)  # If not found in list add to list
    unique_graphs.remove(unique_graphs[0])  # Remove complete graph
    unique_graphs.append(complete_graph)  # and add it to end of list

    print_to_file(unique_graphs, n)


def main():
    q = int(input("enter question number:"))
    n = int(input("enter n:"))
    if q == 1:
        sub_graphs(n)
    if q == 2:
        find_motif(n)


if __name__ == "__main__":
    main()
