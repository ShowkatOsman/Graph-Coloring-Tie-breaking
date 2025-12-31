# algorithms/a10_SD_ID_CN_LD.py

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Saturation Degree coloring with tie-breakers:
    SD → ID → CN → LD
    """
    coloring = {}
    degrees = {v: len(neighbors) for v, neighbors in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}
    neighbor_colors = defaultdict(set)
    id_score = defaultdict(int)
    saturation = defaultdict(int)

    # Initialize the heap with (priority tuple, node)
    # Priority: (-saturation, -ID, -cone_number, -degree, node_id)
    heap = [(-0, -0, -cone_numbers[v], -degrees[v], v) for v in graph]
    heapq.heapify(heap)

    while heap:
        _, _, _, _, v = heapq.heappop(heap)

        if v in coloring:
            continue  # Already colored due to earlier update

        # Assign the smallest possible color not used by neighbors
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

            # Push updated priority for neighbor
            heapq.heappush(heap, (
                -saturation[neighbor],
                -id_score[neighbor],
                -cone_numbers[neighbor],
                -degrees[neighbor],
                neighbor
            ))

    return coloring
