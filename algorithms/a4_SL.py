import heapq
from collections import defaultdict
from algorithms.common import greedy_coloring  # Make sure you have this implemented

def color_graph(graph, max_node):
    """
    Colors the graph using Smallest Last ordering + greedy coloring.
    """
    order = smallest_last_order(graph)
    return greedy_coloring(graph, order, max_node)

def smallest_last_order(graph):
    """
    Compute the smallest last vertex ordering of the graph.
    graph: dict {node: neighbors_set/list}
    returns: list of nodes in smallest last order (to be used for greedy coloring)
    """
    # Copy graph to avoid mutation
    G = {node: set(neighbors) for node, neighbors in graph.items()}

    # Initialize degree tracking
    degree_buckets = defaultdict(set)
    degree_heap = []
    node_degree = {}

    for node in G:
        d = len(G[node])
        degree_buckets[d].add(node)
        heapq.heappush(degree_heap, d)
        node_degree[node] = d

    order = []

    while G:
        # Find the smallest degree with non-empty bucket
        while degree_heap:
            min_deg = heapq.heappop(degree_heap)
            if degree_buckets[min_deg]:
                break
        else:
            break  # Heap is empty

        # Get a valid node from that bucket
        while degree_buckets[min_deg]:
            node = degree_buckets[min_deg].pop()
            if node in G:
                break
        else:
            continue  # Bucket empty, go to next loop iteration

        order.append(node)
        neighbors = list(G[node])  # Safe copy

        # Update neighbors' degrees
        for neighbor in neighbors:
            if neighbor in G:
                old_deg = node_degree[neighbor]
                degree_buckets[old_deg].discard(neighbor)
                new_deg = old_deg - 1
                node_degree[neighbor] = new_deg
                degree_buckets[new_deg].add(neighbor)
                heapq.heappush(degree_heap, new_deg)
                G[neighbor].discard(node)

        del G[node]  # Remove current node

    return order[::-1]  # Reverse for smallest-last ordering
