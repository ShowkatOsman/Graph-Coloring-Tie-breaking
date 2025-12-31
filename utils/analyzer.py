import numpy as np

def evaluate_coloring(graph, coloring):
    # Normalize coloring to a dict {node: color}
    if isinstance(coloring, dict):
        coloring_dict = coloring
    elif isinstance(coloring, (np.ndarray, list)):
        coloring_dict = {node: color for node, color in enumerate(coloring)}
    else:
        raise TypeError(f"Unsupported coloring type: {type(coloring)}")

    # Extract colors excluding uncolored (-1)
    filtered_colors = [c for c in coloring_dict.values() if c != -1]
    used_colors = np.array(filtered_colors)

    max_color = np.max(used_colors) if used_colors.size > 0 else -1
    num_colors = max_color + 1

    conflicts = 0
    for node, neighbors in graph.items():
        node_color = coloring_dict.get(node, -1)
        if node_color == -1:
            continue
        for neighbor in neighbors:
            if neighbor == node:   # 🔒 safety: skip self-loops if any remain
                continue
            neighbor_color = coloring_dict.get(neighbor, -2)
            if node_color == neighbor_color:
                conflicts += 1

    conflicts = conflicts // 2  # Each conflict counted twice in undirected graph

    return num_colors, conflicts



def save_coloring(coloring, output_path):
    if isinstance(coloring, dict):
        items = coloring.items()
    elif isinstance(coloring, (list, np.ndarray)):
        items = enumerate(coloring)
    else:
        raise TypeError(f"Unsupported coloring type: {type(coloring)}")

    with open(output_path, "w") as f:
        for node, color in items:
            if color != -1:
                f.write(f"{node} {color}\n")


def graph_statistics(graph, self_loops=0, duplicates=0):
    num_nodes = len(graph)
    num_edges = sum(len(neighbors) for neighbors in graph.values()) // 2  # undirected edges counted twice
    degrees = [len(neighbors) for neighbors in graph.values()]
    max_degree = max(degrees) if degrees else 0
    avg_degree = sum(degrees) / num_nodes if num_nodes > 0 else 0
    return num_nodes, num_edges, max_degree, avg_degree   # self_loops, duplicates
