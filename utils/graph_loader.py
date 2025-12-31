from collections import defaultdict

def load_graph(file_path, remove_self_loops=True):
    graph_dict = defaultdict(set)  # use set to avoid duplicate edges
    max_node = 0
    self_loops = 0
    duplicates = 0
    seen_edges = set()

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('%'):
                continue

            parts = line.split(',') if ',' in line else line.split()
            if len(parts) < 2:
                continue

            try:
                u = int(parts[0])
                v = int(parts[1])
            except ValueError:
                continue

            # Self-loop check
            if u == v:
                self_loops += 1
                if remove_self_loops:
                    continue

            # Normalize edge (smallest first) to detect duplicates
            edge = (min(u, v), max(u, v))
            if edge in seen_edges:
                duplicates += 1
            else:
                seen_edges.add(edge)

            # Add undirected edge
            graph_dict[u].add(v)
            graph_dict[v].add(u)
            max_node = max(max_node, u, v)

    # Ensure all nodes exist up to max_node
    for i in range(max_node + 1):
        if i not in graph_dict:
            graph_dict[i] = set()

    # Convert sets back to lists for compatibility
    graph_dict = {node: list(neighbors) for node, neighbors in graph_dict.items()}

    return graph_dict, max_node, self_loops, duplicates
