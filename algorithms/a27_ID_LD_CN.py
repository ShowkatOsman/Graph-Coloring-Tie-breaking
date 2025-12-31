# algorithms/a27_ID_LD_CN.py
# Incidence Degree (ID) primary (dynamic: #already-colored neighbors),
# tie-break with Largest Degree (LD), then Cone Number (CN = degree+1).
#
# Designed for memory-efficiency (no NumPy, lazy heap, small per-node sets).

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

    # --- Static precomputations (memory-light) ---
    degrees = {v: len(neighs) for v, neighs in graph.items()}
    cone_numbers = {v: degrees[v] + 1 for v in graph}   # CN = deg + 1 (lightweight)

    # --- Dynamic state ---
    coloring = {}                       # node -> color
    neighbor_colors = defaultdict(set)  # node -> set of distinct neighbor colors (keeps saturation if needed)
    id_score = defaultdict(int)         # node -> number of already-colored neighbors (Incidence Degree)
    # NOTE: id_score starts at 0 and increases as neighbors get colored.

    # Priority function:
    # Primary: ID (higher better) -> we store -id_score for max behavior
    # Tie1:  LD (degree) higher better -> -degrees[v]
    # Tie2:  CN (cone_numbers) higher better -> -cone_numbers[v]
    # Final fallback: node id for deterministic choice
    def priority(v):
        return (-id_score[v], -degrees[v], -cone_numbers[v], v)

    # Build initial heap (all id_score==0 initially)
    heap = [priority(v) for v in graph.keys()]
    heapq.heapify(heap)

    # Lazy-heap main loop
    while heap:
        pr = heapq.heappop(heap)
        v = pr[-1]

        # Skip stale entries
        if pr != priority(v):
            continue

        # If already colored (can happen due to lazy pushes), skip
        if v in coloring:
            continue

        # --- Greedy color assignment: smallest available color ---
        used = neighbor_colors[v]
        c = 0
        while c in used:
            c += 1
        coloring[v] = c

        # --- Update neighbors: id_score and neighbor_colors; push updated priorities ---
        for nbr in graph.get(v, ()):
            if nbr in coloring:
                continue

            # If this color is new to neighbor, update its neighbor_colors (keeps sizes small)
            if c not in neighbor_colors[nbr]:
                neighbor_colors[nbr].add(c)
                # We do not track saturation separately since it's not part of this priority;
                # but neighbor_colors is useful for greedy color checks.

            # Incidence degree: neighbor has one more colored neighbor now
            id_score[nbr] += 1

            # Push updated priority for neighbor (lazy)
            heapq.heappush(heap, priority(nbr))

    return coloring
