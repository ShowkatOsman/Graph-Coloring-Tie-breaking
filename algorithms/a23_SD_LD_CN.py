import heapq
from collections import defaultdict

def compute_cone_numbers(graph):
    """
    Cone Number (CN) = sum of degrees of neighbors.
    Precompute for all nodes.
    """
    degree = {node: len(neighs) for node, neighs in graph.items()}
    cone_number = {}
    for node, neighs in graph.items():
        cone_number[node] = sum(degree[neigh] for neigh in neighs)
    return cone_number

def color_graph(graph, max_node):
    """
    DSATUR with tie-breakers:
    1. Saturation Degree (SD)
    2. Largest Degree (LD)
    3. Cone Number (CN)
    """
    # Precompute degrees and CN
    degrees = {node: len(neighs) for node, neighs in graph.items()}
    cone_numbers = compute_cone_numbers(graph)

    # Tracking structures
    colors = {}
    neighbor_colors = defaultdict(set)

    # Build initial heap (negative for max-heap)
    heap = [(-0, -degrees[node], -cone_numbers[node], node) for node in graph]
    heapq.heapify(heap)
    in_heap = {node: True for node in graph}

    while heap:
        sat_neg, deg_neg, cn_neg, node = heapq.heappop(heap)
        if node in colors:
            continue  # already colored

        # Assign smallest available color
        used_colors = neighbor_colors[node]
        color = 0
        while color in used_colors:
            color += 1
        colors[node] = color

        # Update neighbors
        in_heap[node] = False
        for neigh in graph[node]:
            if neigh not in colors:
                neighbor_colors[neigh].add(color)
                # Update saturation and re-push
                new_sat = len(neighbor_colors[neigh])
                heapq.heappush(heap, (-new_sat, -degrees[neigh], -cone_numbers[neigh], neigh))

    return colors
