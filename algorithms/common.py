import numpy as np

def greedy_coloring(graph, nodes, max_node):
    coloring = np.full(max_node + 1, -1, dtype=np.int32)
    for node in nodes:
        neighbor_colors = {coloring[n] for n in graph[node] if coloring[n] != -1}
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[node] = color
    return coloring
