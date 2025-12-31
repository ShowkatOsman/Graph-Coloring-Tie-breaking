# algorithms/a23_SD_CN_LD.py
# DSATUR with tie-breakers: Saturation → Cone Number (CN) → Largest Degree (LD) → Node ID
# CN is implemented as degree + 1 to keep memory and runtime low, matching your other CN variants.

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

    # --- Lightweight structures (scales to ~1M edges on 4 GB RAM) ---
    coloring = {}                                  # node -> color
    degrees = {v: len(neighs) for v, neighs in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}   # CN = deg + 1 (lightweight)
    neighbor_colors = defaultdict(set)             # node -> set of colors seen in neighbors
    saturation = defaultdict(int)                  # node -> |neighbor_colors[node]|

    # Priority: (-sat, -CN, -deg, node)
    # Use negatives for max behavior via Python's min-heap.
    def priority(v):
        return (-saturation[v], -cone_numbers[v], -degrees[v], v)

    # Build initial heap
    heap = [priority(v) for v in graph.keys()]
    heapq.heapify(heap)

    # Lazy-heap approach: push updated priorities; skip stale pops.
    while heap:
        pr = heapq.heappop(heap)
        v = pr[-1]
        if pr != priority(v):
            continue  # stale entry
        if v in coloring:
            continue  # already colored

        # --- Assign smallest available color to v ---
        used = neighbor_colors[v]
        c = 0
        while c in used:
            c += 1
        coloring[v] = c

        # --- Update neighbors and push new priorities ---
        for nbr in graph.get(v, ()):
            if nbr in coloring:
                continue
            if c not in neighbor_colors[nbr]:
                neighbor_colors[nbr].add(c)
                saturation[nbr] += 1
            # degrees[nbr] and cone_numbers[nbr] are static (by definition here)
            heapq.heappush(heap, priority(nbr))

    return coloring
