import numpy as np
import heapq

def color_graph(graph, max_node):
    """
    Heap-based graph coloring using priority: (-ID, -SD, -deg, node)
    - graph: dict-based graph {node: [neighbor1, neighbor2, ...]}
    - max_node: highest node index
    """
    n = max_node + 1
    neighbors = graph  # dict: node -> list of neighbors

    uncolored = set(graph.keys())
    coloring = np.full(n, -1, dtype=np.int32)
    saturation = [0] * n
    degrees = [len(neighbors.get(v, [])) for v in range(n)]
    incidence = degrees.copy()

    # Initial heap
    heap = [(-incidence[v], -saturation[v], -degrees[v], v) for v in range(n) if v in neighbors]
    heapq.heapify(heap)

    in_heap = [True] * n

    while uncolored:
        # Pop node with highest priority
        while True:
            _, _, _, node = heapq.heappop(heap)
            if in_heap[node]:
                current = node
                break

        # Assign smallest available color
        neighbor_colors = {coloring[nb] for nb in neighbors[current] if coloring[nb] != -1}
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[current] = color

        uncolored.remove(current)
        in_heap[current] = False

        # Update neighbors
        for nb in neighbors[current]:
            if in_heap[nb]:
                neighbor_color_set = {coloring[n] for n in neighbors[nb] if coloring[n] != -1}
                saturation[nb] = len(neighbor_color_set)
                incidence[nb] = sum(1 for n in neighbors[nb] if coloring[n] == -1)

                heapq.heappush(heap, (-incidence[nb], -saturation[nb], -degrees[nb], nb))

    return coloring
