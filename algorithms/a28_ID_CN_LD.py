# algorithms/a28_ID_CN_LD.py
# Incidence Degree (ID) primary (dynamic: #already-colored neighbors)
# Tie-break 1: Cone Number (CN = degree + 1)
# Tie-break 2: Largest Degree (LD = degree)
#
# Memory-friendly for large graphs (~1M edges) on low-RAM machines.

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Parameters
    ----------
    graph : dict[int, Iterable[int]]
        adjacency list mapping node -> iterable of neighbors
    max_node : int
        highest node id (for interface compatibility)

    Returns
    -------
    dict[int,int]
        mapping node -> color (0-based)
    """

    # --- Static precomputations ---
    degrees = {v: len(neighs) for v, neighs in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}  # CN = deg + 1

    # --- Dynamic state ---
    coloring = {}                       # node -> color
    neighbor_colors = defaultdict(set)  # node -> set of distinct neighbor colors
    id_score = defaultdict(int)         # node -> # already-colored neighbors

    # Priority function:
    #   Primary: -id_score[v]
    #   Tie 1:  -cone_numbers[v]
    #   Tie 2:  -degrees[v]
    #   Final:  node id
    def priority(v):
        return (-id_score[v], -cone_numbers[v], -degrees[v], v)

    # Initial heap (all id_score == 0)
    heap = [priority(v) for v in graph.keys()]
    heapq.heapify(heap)

    while heap:
        pr = heapq.heappop(heap)
        v = pr[-1]

        # Skip stale entries
        if pr != priority(v):
            continue
        if v in coloring:
            continue

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

            id_score[nbr] += 1
            heapq.heappush(heap, priority(nbr))

    return coloring
