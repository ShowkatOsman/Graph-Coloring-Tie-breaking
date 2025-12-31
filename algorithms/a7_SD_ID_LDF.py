import numpy as np
import heapq

def color_graph(graph, max_node):
    """
    Coloring with priority: (-saturation, -incidence, -degree, node)
    Works with dict-based graph input.
    """
    n = max_node + 1
    neighbors = graph  # dict: node -> list of neighbors

    uncolored = set(graph.keys())
    coloring = np.full(n, -1, dtype=np.int32)
    saturation = [0] * n
    incidence = [len(neighbors.get(v, [])) for v in range(n)]
    degrees = [len(neighbors.get(v, [])) for v in range(n)]

    # Initialize heap
    heap = [(-saturation[v], -incidence[v], -degrees[v], v) for v in range(n) if v in neighbors]
    heapq.heapify(heap)

    in_heap = [True] * n

    while uncolored:
        # Pop the next uncolored node
        while True:
            _, _, _, node = heapq.heappop(heap)
            if in_heap[node]:
                current = node
                break

        # Assign smallest valid color
        neighbor_colors = {coloring[nbr] for nbr in neighbors[current] if coloring[nbr] != -1}
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[current] = color

        uncolored.remove(current)
        in_heap[current] = False

        # Update neighbors
        for nbr in neighbors[current]:
            if in_heap[nbr]:
                # Update saturation
                neighbor_color_set = {coloring[n] for n in neighbors[nbr] if coloring[n] != -1}
                saturation[nbr] = len(neighbor_color_set)

                # Update incidence (uncolored neighbors)
                incidence[nbr] = sum(1 for n in neighbors[nbr] if coloring[n] == -1)

                heapq.heappush(heap, (-saturation[nbr], -incidence[nbr], -degrees[nbr], nbr))

    return coloring
