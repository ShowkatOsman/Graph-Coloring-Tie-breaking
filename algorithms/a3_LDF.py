#LDF with heap based
import numpy as np
import heapq

def color_graph(graph, max_node):
    """
    Heap-based Largest Degree First (LDF) greedy graph coloring.
    At each step, selects the uncolored node with the highest degree.
    Returns a NumPy array of colors indexed by node ID.
    """
    n = max_node + 1
    colors = np.full(n, -1, dtype=np.int16)
    degrees = np.array([len(graph[v]) if v in graph else 0 for v in range(n)], dtype=np.int32)
    in_heap = [True] * n  # Track uncolored nodes

    # Build initial max-heap with (-degree, node)
    heap = [(-degrees[v], v) for v in graph]
    heapq.heapify(heap)

    while heap:
        _, current = heapq.heappop(heap)
        if not in_heap[current]:
            continue  # Already colored

        # Assign the smallest available color not used by neighbors
        used = {colors[neigh] for neigh in graph.get(current, []) if colors[neigh] != -1}
        for c in range(n):
            if c not in used:
                colors[current] = c
                break

        in_heap[current] = False

        # Degree does not change in standard LDF, so no re-pushing of neighbors
        # If dynamic updates were needed (e.g. adaptive LDF), reinsert neighbors here

    return colors
