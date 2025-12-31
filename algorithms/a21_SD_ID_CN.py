# algorithms/a21_SD_ID_CN.py
# DSATUR with tie-breakers: Saturation → Incidence Degree (ID) → Cone Number (CN) → Vertex ID
# CN is implemented as degree + 1 (consistent with your other CN variants and lightweight for memory).

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Parameters
    ----------
    graph : dict[int, Iterable[int]]
        Adjacency list dict: node -> iterable of neighbors
    max_node : int
        Highest node id (kept for interface compatibility; not required here)

    Returns
    -------
    dict[int, int]
        A mapping node -> color (0-based)
    """
    # ---- Setup (compact data structures, no NumPy) ----
    # Using plain dicts/lists to stay memory-light for ~1M edges
    coloring = {}                                # node -> color
    degrees = {v: len(neigh) for v, neigh in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}   # lightweight CN used elsewhere in your repo
    neighbor_colors = defaultdict(set)           # node -> set of colors in its neighborhood
    id_score = defaultdict(int)                  # node -> # already-colored neighbors
    saturation = defaultdict(int)                # node -> |neighbor_colors[node]|

    # Build initial heap: priority is (-sat, -ID, -CN, node)
    # We use negative values because heapq is a min-heap.
    heap = []
    for v in graph.keys():
        heap.append((
            0,                          # -saturation[v] initially 0 (we'll negate when pushing)
            0,                          # -id_score[v]
            -cone_numbers[v],           # -CN
            v                           # node id (tie-breaker)
        ))
    heapq.heapify(heap)

    # To avoid decrease-key, we push many entries per vertex and validate on pop
    # We'll consider an entry "stale" if its stored priority doesn't match current state.
    def current_priority(v):
        return (-saturation[v], -id_score[v], -cone_numbers[v], v)

    while heap:
        # Pop until we find a fresh (non-stale) entry
        neg_sat, neg_id, neg_cn, v = heapq.heappop(heap)
        if (neg_sat, neg_id, neg_cn, v) != current_priority(v):
            # Stale entry — skip
            continue

        if v in coloring:
            # Already colored due to a newer push — skip
            continue

        # ---- Choose the smallest available color for v (standard greedy assignment step) ----
        used = neighbor_colors[v]
        color = 0
        # Find smallest non-negative integer not in 'used'
        while color in used:
            color += 1
        coloring[v] = color

        # ---- Update neighbors (saturation, ID, neighbor_colors) and push new priorities ----
        for nbr in graph.get(v, ()):
            if nbr in coloring:
                continue

            # Update neighbor_colors and saturation if this is a new color they see
            if color not in neighbor_colors[nbr]:
                neighbor_colors[nbr].add(color)
                saturation[nbr] += 1

            # Incidence degree (already-colored neighbor count) always increases by 1 here
            id_score[nbr] += 1

            # Push updated priority for neighbor
            heapq.heappush(heap, current_priority(nbr))

    return coloring
