# algorithms/a25_ID_SD_CN.py
# Incidence Degree (ID) → Saturation Degree (SD) → Cone Number (CN) → Node ID
# CN is implemented as degree + 1 for memory efficiency.

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Parameters
    ----------
    graph : dict[int, Iterable[int]]
        Adjacency list: node -> iterable of neighbors
    max_node : int
        Highest node id (kept for interface compatibility)

    Returns
    -------
    dict[int, int]
        node -> color (0-based)
    """

    coloring = {}                                  # node -> color
    degrees = {v: len(neighs) for v, neighs in graph.items()}  # ID is just degree
    cone_numbers = {v: degrees[v] + 1 for v in graph}          # CN = deg + 1
    neighbor_colors = defaultdict(set)             # node -> set of neighbor colors
    saturation = defaultdict(int)                  # node -> #distinct neighbor colors

    # Priority: (-ID, -SD, -CN, node)
    def priority(v):
        return (-degrees[v], -saturation[v], -cone_numbers[v], v)

    # Build initial heap
    heap = [priority(v) for v in graph.keys()]
    heapq.heapify(heap)

    while heap:
        pr = heapq.heappop(heap)
        v = pr[-1]
        if pr != priority(v):
            continue  # stale
        if v in coloring:
            continue  # already colored

        # Assign smallest available color
        used = neighbor_colors[v]
        c = 0
        while c in used:
            c += 1
        coloring[v] = c

        # Update neighbors
        for nbr in graph.get(v, ()):
            if nbr in coloring:
                continue
            if c not in neighbor_colors[nbr]:
                neighbor_colors[nbr].add(c)
                saturation[nbr] += 1
            heapq.heappush(heap, priority(nbr))

    return coloring
