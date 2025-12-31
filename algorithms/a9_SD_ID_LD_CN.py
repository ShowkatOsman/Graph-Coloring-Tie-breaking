# algorithms/a9_SDIRLD_CN.py

def color_graph(graph, max_node):
    import heapq
    from collections import defaultdict

    # Initialize all nodes as uncolored
    coloring = {}
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}
    neighbor_colors = defaultdict(set)
    id_score = defaultdict(int)

    # Saturation degree tracking
    saturation = defaultdict(int)

    # Priority Queue: (-saturation, -ID, -degree, -cone, node_id)
    heap = [(-0, -0, -degrees[v], -cone_numbers[v], v) for v in graph]
    heapq.heapify(heap)

    while heap:
        # Pop node with highest priority
        _, _, _, _, v = heapq.heappop(heap)

        if v in coloring:
            continue  # Skip if already colored due to previous heap duplicates

        # Assign the smallest available color
        used_colors = {coloring[nbr] for nbr in graph[v] if nbr in coloring}
        color = 0
        while color in used_colors:
            color += 1
        coloring[v] = color

        # Update saturation and ID scores for neighbors
        for neighbor in graph[v]:
            if neighbor not in coloring:
                # If this color is new to neighbor's neighbors
                if color not in neighbor_colors[neighbor]:
                    saturation[neighbor] += 1
                    neighbor_colors[neighbor].add(color)

                id_score[neighbor] += 1  # Increase ID (already colored neighbor count)

                # Push updated neighbor back into heap with new priority
                heapq.heappush(heap, (
                    -saturation[neighbor],
                    -id_score[neighbor],
                    -degrees[neighbor],
                    -cone_numbers[neighbor],
                    neighbor
                ))

    return coloring
