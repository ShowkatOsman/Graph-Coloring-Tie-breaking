# algorithms/a15_ID_SD_LD_CN.py

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Incidence Degree coloring with tie-breakers:
    ID → SD → LD → CN
    """
    coloring = {}
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}
    neighbor_colors = defaultdict(set)
    saturation = defaultdict(int)
    id_score = defaultdict(int)

    # Priority: (-ID, -SD, -LD, -CN, node_id)
    heap = [(-0, -0, -degrees[v], -cone_numbers[v], v) for v in graph]
    heapq.heapify(heap)

    while heap:
        _, _, _, _, v = heapq.heappop(heap)

        if v in coloring:
            continue

        # Assign smallest color not used by neighbors
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
                -id_score[neighbor],
                -saturation[neighbor],
                -degrees[neighbor],
                -cone_numbers[neighbor],
                neighbor
            ))

    return coloring
