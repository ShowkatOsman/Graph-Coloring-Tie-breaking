# algorithms/a13_SD_CN_ID_LD.py

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Saturation Degree coloring with tie-breakers:
    SD → CN → ID → LD
    """
    coloring = {}
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}
    neighbor_colors = defaultdict(set)
    id_score = defaultdict(int)
    saturation = defaultdict(int)

    # Priority: (-SD, -CN, -ID, -LD, node_id)
    heap = [(-0, -cone_numbers[v], -0, -degrees[v], v) for v in graph]
    heapq.heapify(heap)

    while heap:
        _, _, _, _, v = heapq.heappop(heap)

        if v in coloring:
            continue  # Skip if already colored

        # Find smallest color not used by neighbors
        used_colors = {coloring[n] for n in graph[v] if n in coloring}
        color = 0
        while color in used_colors:
            color += 1
        coloring[v] = color

        # Update neighbors
        for neighbor in graph[v]:
            if neighbor in coloring:
                continue

            if color not in neighbor_colors[neighbor]:
                neighbor_colors[neighbor].add(color)
                saturation[neighbor] += 1

            id_score[neighbor] += 1

            heapq.heappush(heap, (
                -saturation[neighbor],
                -cone_numbers[neighbor],
                -id_score[neighbor],
                -degrees[neighbor],
                neighbor
            ))

    return coloring
