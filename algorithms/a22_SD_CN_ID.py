# algorithms/a22_SD_CN_ID.py
# DSATUR with tie-breakers: Saturation → Cone Number (CN) → Incidence Degree (ID) → Degree → Vertex ID
# CN is implemented as degree + 1 (lightweight, consistent with your other CN variants).

from collections import defaultdict
import heapq

def color_graph(graph, max_node):
    """
    Parameters
    ----------
    graph : dict[int, Iterable[int]]
        Adjacency list dict: node -> iterable of neighbors
    max_node : int
        Highest node id (for interface compatibility; not required here)

    Returns
    -------
    dict[int, int]
        node -> color (0-based)
    """
    # ---- Lightweight structures (good for ~1M edges, 4 GB RAM) ----
    coloring = {}                                  # node -> color
    degrees = {v: len(neigh) for v, neigh in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}     # CN = deg + 1
    neighbor_colors = defaultdict(set)             # node -> set of seen neighbor colors
    id_score = defaultdict(int)                    # node -> # already-colored neighbors
    saturation = defaultdict(int)                  # node -> |neighbor_colors[node]|

    # Heap priority: (-sat, -CN, -ID, -deg, node)
    # Use negatives since heapq is a min-heap; we want max priority first.
    def priority(v):
        return (-saturation[v], -cone_numbers[v], -id_score[v], -degrees[v], v)

    heap = [priority(v) for v in graph.keys()]
    heapq.heapify(heap)

    # Lazy-heap approach: push updated entries; skip stale pops.
    while heap:
        neg_sat, neg_cn, neg_id, neg_deg, v = heapq.heappop(heap)
        if (neg_sat, neg_cn, neg_id, neg_deg, v) != priority(v):
            continue  # stale entry
        if v in coloring:
            continue  # already colored

        # ---- Assign smallest available color (greedy step) ----
        used = neighbor_colors[v]
        c = 0
        while c in used:
            c += 1
        coloring[v] = c

        # ---- Update neighbors ----
        for nbr in graph.get(v, ()):
            if nbr in coloring:
                continue

            # If this is a new color for nbr, update saturation
            if c not in neighbor_colors[nbr]:
                neighbor_colors[nbr].add(c)
                saturation[nbr] += 1

            # Increment incidence degree (already-colored neighbor count)
            id_score[nbr] += 1

            # Push updated priority for nbr
            heapq.heappush(heap, priority(nbr))

    return coloring
