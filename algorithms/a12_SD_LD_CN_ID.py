# algorithms/a12_SD_LD_CN_ID.py

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Saturation Degree coloring with tie-breakers:
    SD → LD → CN → ID
    """
    coloring = {}
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}
    neighbor_colors = defaultdict(set)
    id_score = defaultdict(int)
    saturation = defaultdict(int)

    # Priority: (-SD, -LD, -CN, -ID, node_id)
    heap = [(-0, -degrees[v], -cone_numbers[v], -0, v) for v in graph]
    heapq.heapify(heap)

    while heap:
        _, _, _, _, v = heapq.heappop(heap)

        if v in coloring:
            continue  # Already colored due to earlier heap push

        # Assign the smallest available color not used by neighbors
        used = {coloring[n] for n in graph[v] if n in coloring}
        color = 0
        while color in used:
            color += 1
        coloring[v] = color

        # Update neighbor info
        for neighbor in graph[v]:
            if neighbor in coloring:
                continue

            if color not in neighbor_colors[neighbor]:
                neighbor_colors[neighbor].add(color)
                saturation[neighbor] += 1

            id_score[neighbor] += 1

            heapq.heappush(heap, (
                -saturation[neighbor],
                -degrees[neighbor],
                -cone_numbers[neighbor],
                -id_score[neighbor],
                neighbor
            ))

    return coloring
