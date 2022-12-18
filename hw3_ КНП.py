import networkx as nx
import matplotlib.pyplot as plt
import random

MIN_NODES_COUNT = 5
MAX_NODES_COUNT = 10
K = 3

POS = None


def get_random_from_list(g_list):
    index = random.randint(0, len(g_list) - 1)
    return g_list[index]


def get_random_weight():
    return random.randint(1, 100)


def get_nodes_count():
    return random.randint(MIN_NODES_COUNT, MAX_NODES_COUNT)


def random_boolean():
    return random.choice([True, False])


def put_first_edge(g, count):
    first = random.randint(1, count)
    second = random.randint(1, count)
    while first == second:
        second = random.randint(1, count)
    g.add_edge(first, second, weight=get_random_weight())


def connect_node_randomly(g, node):
    for j in list(g.nodes):
        if node != j and random_boolean():
            g.add_edge(node, j, weight=get_random_weight())


def get_random_graph():
    g = nx.Graph()
    nodes_count = get_nodes_count()
    put_first_edge(g, nodes_count)
    for i in range(1, nodes_count + 1):
        connect_node_randomly(g, i)
    while len(list(g.nodes)) != nodes_count:
        for i in range(1, nodes_count + 1):
            if i not in list(g.nodes):
                connect_node_randomly(g, i)

    return g


def draw_graph(g, pos=None):
    if pos is None:
        pos = nx.spring_layout(g)
    plt.plot()
    options = {
        'node_color': 'red',
        'node_size': 200,
        'width': 3,
        'with_labels': True,
        'pos': pos
    }
    nx.draw(g, **options)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=labels)
    plt.show()
    return pos


def get_min_weight_edge(g):
    min_edge = list(g.edges.data('weight'))[0]
    for (u, v, w) in g.edges.data('weight'):
        if w < min_edge[2]:
            min_edge = (u, v, w)
    return min_edge


def get_spanning_tree(g):
    nodes = list(g.nodes)
    spanning_tree = nx.Graph()
    min_edge = get_min_weight_edge(g)
    spanning_tree.add_edge(min_edge[0], min_edge[1], weight=min_edge[2])
    nodes.remove(min_edge[0])
    nodes.remove(min_edge[1])

    while len(nodes) > 0:
        min_edge = None
        for sp_node in list(spanning_tree.nodes):
            for node in nodes:
                if g.has_edge(sp_node, node):
                    w = g.edges[sp_node, node]['weight']
                    if min_edge is None or w < min_edge[2]:
                        min_edge = (sp_node, node, w)
        spanning_tree.add_edge(min_edge[0], min_edge[1], weight=min_edge[2])
        nodes.remove(min_edge[1])
    return spanning_tree


def remove_max_edges(g):
    sorted_edges = sorted(g.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    for i in range(0, K - 1):
        g.remove_edge(sorted_edges[i][0], sorted_edges[i][1])
    return g


if __name__ == "__main__":
    G = get_random_graph()
    POS = draw_graph(G)
    ST = get_spanning_tree(G)
    plt.pause(0.3)
    draw_graph(ST, POS)
    remove_max_edges(ST)
    plt.pause(0.3)
    draw_graph(ST, POS)
    for subgraph in nx.connected_components(ST):
        print(subgraph)
