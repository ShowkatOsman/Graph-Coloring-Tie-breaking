#ID with heap based
import numpy as np
import heapq

def color_graph(graph, max_node):
    """
    Heap-based Incidence Degree graph coloring algorithm.
    Priority: Highest incidence degree (number of already colored neighbors).
    Returns a NumPy array with color assignments.
    """
    n = max_node + 1
    colors = np.full(n, -1, dtype=np.int16)
    incidence = np.zeros(n, dtype=np.int16)
    in_heap = [True] * n  # Track which nodes are still uncolored

    # Initialize heap: (-incidence[node], node)
    heap = [(-incidence[node], node) for node in graph]
    heapq.heapify(heap)

    while heap:
        _, current = heapq.heappop(heap)

        if not in_heap[current]:
            continue  # Already colored

        # Assign the smallest available color not used by neighbors
        used = {colors[neigh] for neigh in graph[current] if colors[neigh] != -1}
        for c in range(n):
            if c not in used:
                colors[current] = c
                break

        in_heap[current] = False

        # Update incidence of uncolored neighbors and push back into heap
        for neighbor in graph[current]:
            if in_heap[neighbor]:
                incidence[neighbor] += 1
                heapq.heappush(heap, (-incidence[neighbor], neighbor))

    return colors
