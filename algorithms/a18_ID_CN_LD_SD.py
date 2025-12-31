# algorithms/a18_ID_CN_LD_SD.py

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Incidence Degree coloring with tie-breakers:
    ID → CN → LD → SD
    """
    coloring = {}
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}
    neighbor_colors = defaultdict(set)
    saturation = defaultdict(int)
    id_score = defaultdict(int)

    # Initialize heap with priority tuple:
    # (-ID, -CN, -LD, -SD, node_id)
    heap = [(-0, -cone_numbers[v], -degrees[v], -0, v) for v in graph]
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

        # Update neighbors after coloring v
        for neighbor in graph[v]:
            if neighbor in coloring:
                continue

            if color not in neighbor_colors[neighbor]:
                neighbor_colors[neighbor].add(color)
                saturation[neighbor] += 1

            id_score[neighbor] += 1

            # Push updated priority for neighbor
            heapq.heappush(heap, (
                -id_score[neighbor],
                -cone_numbers[neighbor],
                -degrees[neighbor],
                -saturation[neighbor],
                neighbor
            ))

    return coloring
