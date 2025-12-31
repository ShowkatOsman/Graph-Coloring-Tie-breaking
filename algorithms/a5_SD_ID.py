import numpy as np
import heapq

def color_graph(graph, max_node=None):
    n = max_node + 1  # total number of nodes
    neighbors = graph  # dict: node -> list of neighbors

    uncolored = set(graph.keys())
    coloring = np.full(n, -1, dtype=np.int32)
    saturation = [0] * n

    # incidence degree (dynamic: only uncolored neighbors count)
    incidence_degree = [len(neighbors.get(i, [])) for i in range(n)]

    # Build initial heap with priority: (-saturation, -incidence_degree, node)
    heap = [(-saturation[v], -incidence_degree[v], v) for v in range(n) if v in graph]
    heapq.heapify(heap)

    in_heap = [True] * n  # track which nodes are still uncolored

    while uncolored:
        # Get uncolored node with highest priority
        while heap:
            _, _, node = heapq.heappop(heap)
            if in_heap[node]:
                break

        # Assign smallest available color
        neighbor_colors = {coloring[nbr] for nbr in neighbors[node] if coloring[nbr] != -1}
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[node] = color
        uncolored.remove(node)
        in_heap[node] = False

        # Update saturation + incidence degree of neighbors and push back
        for nbr in neighbors[node]:
            if in_heap[nbr]:
                neighbor_color_set = {coloring[n] for n in neighbors[nbr] if coloring[n] != -1}
                saturation[nbr] = len(neighbor_color_set)

                # incidence degree = number of uncolored neighbors
                incidence_degree[nbr] = sum(1 for nn in neighbors[nbr] if in_heap[nn])

                heapq.heappush(heap, (-saturation[nbr], -incidence_degree[nbr], nbr))

    return coloring
