import numpy as np
import heapq

def color_graph(graph, max_node=None):
    n = max_node + 1
    neighbors = graph  # dict: node -> list of neighbors

    uncolored = set(graph.keys())
    coloring = np.full(n, -1, dtype=np.int32)
    saturation = [0] * n
    incidence = [len(neighbors.get(v, [])) for v in range(n)]

    # Initialize heap with (-incidence, -saturation, node)
    heap = [(-incidence[v], -saturation[v], v) for v in range(n) if v in graph]
    heapq.heapify(heap)

    in_heap = [True] * n

    while uncolored:
        # Get the next uncolored node
        while heap:
            _, _, node = heapq.heappop(heap)
            if in_heap[node]:
                break

        # Assign the smallest possible color
        neighbor_colors = {coloring[nbr] for nbr in neighbors[node] if coloring[nbr] != -1}
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[node] = color

        uncolored.remove(node)
        in_heap[node] = False

        # Update neighbors’ saturation and incidence, then push updated values
        for nbr in neighbors[node]:
            if in_heap[nbr]:
                neighbor_color_set = {coloring[n] for n in neighbors[nbr] if coloring[n] != -1}
                saturation[nbr] = len(neighbor_color_set)

                incidence[nbr] = sum(1 for neighbor in neighbors[nbr] if coloring[neighbor] == -1)

                heapq.heappush(heap, (-incidence[nbr], -saturation[nbr], nbr))

    return coloring
