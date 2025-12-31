# algorithms/a26_ID_CN_SD.py
# Incidence Degree (ID) primary, tie-break with Cone Number (CN), then Saturation Degree (SD).
# CN implemented as degree + 1 for memory efficiency.

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Parameters
    ----------
    graph : dict[int, Iterable[int]]
        adjacency list mapping node -> iterable of neighbors
    max_node : int
        highest node id (interface compatibility; not required)

    Returns
    -------
    dict[int,int]
        mapping node -> color (0-based)
    """

    # ---------- Lightweight precomputations ----------
    # degrees = ID (static)
    degrees = {v: len(neighs) for v, neighs in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}   # CN = degree + 1 (lightweight)
    coloring = {}                                       # node -> color
    neighbor_colors = defaultdict(set)                  # node -> set of colors seen in neighbors
    saturation = defaultdict(int)                       # node -> |neighbor_colors[node]|

    # ---------- Priority function ----------
    # Priority order (max behavior):
    # 1) ID (degree)  -> higher better
    # 2) CN (degree+1) -> higher better
    # 3) SD (saturation) -> higher better
    # 4) node id -> lower node id for deterministic tie-break
    def priority(v):
        return (-degrees[v], -cone_numbers[v], -saturation[v], v)

    # Build initial heap with initial priorities (saturation = 0)
    heap = [priority(v) for v in graph.keys()]
    heapq.heapify(heap)

    # ---------- Main loop: lazy-heap DSATUR-like coloring ----------
    while heap:
        pr = heapq.heappop(heap)
        v = pr[-1]

        # Skip stale entries
        if pr != priority(v):
            continue

        # Skip if already colored (may happen if an earlier push colored it)
        if v in coloring:
            continue

        # Assign smallest available color (greedy)
        used = neighbor_colors[v]
        c = 0
        while c in used:
            c += 1
        coloring[v] = c

        # Update neighbors' saturation (and push updated priorities)
        for nbr in graph.get(v, ()):
            if nbr in coloring:
                continue

            if c not in neighbor_colors[nbr]:
                neighbor_colors[nbr].add(c)
                saturation[nbr] += 1

            # push updated priority for neighbor (lazy approach)
            heapq.heappush(heap, priority(nbr))

    return coloring
