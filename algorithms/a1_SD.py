import numpy as np
import heapq
from collections import defaultdict

def color_graph(graph, max_node=None):
    """
    DSATUR graph coloring algorithm using a heap for efficient node selection.
    Priority: Saturation → Node Name (alphabetical).
    Returns a dictionary {node_id: color}.
    """
    nodes = list(graph.keys())
    node_to_index = {node: idx for idx, node in enumerate(nodes)}
    index_to_node = {idx: node for node, idx in node_to_index.items()}
    n = len(nodes)

    # Initialize
    colors = np.full(n, -1, dtype=int)
    saturation = np.zeros(n, dtype=int)
    neighbor_colors = [set() for _ in range(n)]

    # Build initial heap: (-saturation, node_name)
    heap = [(-saturation[i], index_to_node[i]) for i in range(n)]
    heapq.heapify(heap)
    in_heap = [True] * n

    while heap:
        _, current_node = heapq.heappop(heap)
        current = node_to_index[current_node]

        if colors[current] != -1:
            continue  # Already colored

        # Assign smallest possible color
        used = {colors[node_to_index[neigh]] for neigh in graph[current_node]
                if colors[node_to_index[neigh]] != -1}
        for c in range(n):
            if c not in used:
                colors[current] = c
                break

        in_heap[current] = False

        # Update saturation of neighbors and push updated entries into heap
        for neigh in graph[current_node]:
            if neigh not in node_to_index:
                continue
            ni = node_to_index[neigh]
            if in_heap[ni] and colors[current] not in neighbor_colors[ni]:
                neighbor_colors[ni].add(colors[current])
                saturation[ni] += 1
                heapq.heappush(heap, (-saturation[ni], index_to_node[ni]))

    # Return color assignment as {original_node: color}
    return {index_to_node[i]: colors[i] for i in range(n)}
