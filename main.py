import time
from utils.graph_loader import load_graph
from utils.analyzer import evaluate_coloring, graph_statistics

# Import renamed algorithms (all dict-based, heap-based)
from algorithms.a1_SD import color_graph as sd_color
from algorithms.a2_ID import color_graph as id_color
from algorithms.a3_LDF import color_graph as ldf_color
from algorithms.a4_SL import color_graph as sl_color
from algorithms.a5_SD_ID import color_graph as sdid_color
from algorithms.a6_ID_SD import color_graph as idsd_color
from algorithms.a7_SD_ID_LDF import color_graph as sdidldf_color
from algorithms.a8_ID_SD_LDF import color_graph as idsdldf_color
from algorithms.a9_SD_ID_LD_CN import color_graph as sdidldcn_color
from algorithms.a10_SD_ID_CN_LD import color_graph as sdidcnld_color
from algorithms.a11_SD_LD_ID_CN import color_graph as sdlidcn_color
from algorithms.a12_SD_LD_CN_ID import color_graph as sdlcnid_color
from algorithms.a13_SD_CN_ID_LD import color_graph as sdcnidld_color
from algorithms.a14_SD_CN_LD_ID import color_graph as sdcnldid_color
from algorithms.a15_ID_SD_LD_CN import color_graph as idsdldcn_color
from algorithms.a16_ID_SD_CN_LD import color_graph as idsdcnld_color
from algorithms.a17_ID_CN_SD_LD import color_graph as idcnsdld_color
from algorithms.a18_ID_CN_LD_SD import color_graph as idcnldsd_color
from algorithms.a19_ID_LD_CN_SD import color_graph as idldcnsd_color
from algorithms.a20_ID_LD_SD_CN import color_graph as idldsdcn_color
from algorithms.a21_SD_ID_CN import color_graph as sd_id_cn
from algorithms.a22_SD_CN_ID import color_graph as sd_cn_id
from algorithms.a23_SD_LD_CN import color_graph as sd_ld_cn_color
from algorithms.a24_SD_CN_LD import color_graph as sd_cn_ld
from algorithms.a25_ID_SD_CN import color_graph as id_sd_cn_color
from algorithms.a26_ID_CN_SD import color_graph as id_cn_sd_color
from algorithms.a27_ID_LD_CN import color_graph as id_ld_cn_color
from algorithms.a28_ID_CN_LD import color_graph as id_cn_ld_color


def main():
    # Load dict_graph, max_node, self_loops, duplicates
    dict_graph, max_node, self_loops, duplicates = load_graph(
        r"E:\CSE491 Project\Project-1_Graph_Coloring\Dataset\DataSet-Edges\5M-6\rgg_n_2_20_s0\rgg_n_2_20_s0.mtx"
  )

    # If want to keep self-loops:
    # dict_graph, max_node, self_loops, duplicates = load_graph("graph.mtx", remove_self_loops=False)

    # Compute graph statistics
    num_nodes, num_edges, max_degree, avg_degree = graph_statistics(dict_graph)

    algorithms = {
        
        
        "LDF": lambda _, m: ldf_color(dict_graph, m),
        "SL": lambda _, m: sl_color(dict_graph, m), 
        "SD": lambda _, m: sd_color(dict_graph, m),
        "SD+ID": lambda _, m: sdid_color(dict_graph, m),
        "SD+ID+LDF": lambda _, m: sdidldf_color(dict_graph, m),
        "SD+ID+CN": lambda _, m: sd_id_cn(dict_graph, m),
        "SD+CN+ID": lambda _, m: sd_cn_id(dict_graph, m),
        "SD+LD+CN": lambda _, m: sd_ld_cn_color(dict_graph, m),
        "SD+CN+LD": lambda _, m: sd_cn_ld(dict_graph, m),
        "SD+ID+LD+CN": lambda _, m: sdidldcn_color(dict_graph, m),
        "SD+ID+CN+LD": lambda _, m: sdidcnld_color(dict_graph, m),
        "SD+LD+ID+CN": lambda _, m: sdlidcn_color(dict_graph, m),
        "SD+LD+CN+ID": lambda _, m: sdlcnid_color(dict_graph, m),
        "SD+CN+ID+LD": lambda _, m: sdcnidld_color(dict_graph, m),
        "SD+CN+LD+ID": lambda _, m: sdcnldid_color(dict_graph, m),
        "ID": lambda _, m: id_color(dict_graph, m),
        "ID+SD": lambda _, m: idsd_color(dict_graph, m),  
        "ID+SD+LDF": lambda _, m: idsdldf_color(dict_graph, m),
        "ID+SD+CN": lambda _, m: id_sd_cn_color(dict_graph, m),
        "ID+CN+SD": lambda _, m: id_cn_sd_color(dict_graph, m),
        "ID+LD+CN": lambda _, m: id_ld_cn_color(dict_graph, m),
        "ID+CN+LD": lambda _, m: id_cn_ld_color(dict_graph, m),
        "ID+SD+LD+CN": lambda _, m: idsdldcn_color(dict_graph, m),
        "ID+SD+CN+LD": lambda _, m: idsdcnld_color(dict_graph, m),
        "ID+CN+SD+LD": lambda _, m: idcnsdld_color(dict_graph, m),
        "ID+CN+LD+SD": lambda _, m: idcnldsd_color(dict_graph, m),
        "ID+LD+CN+SD": lambda _, m: idldcnsd_color(dict_graph, m),
        "ID+LD+SD+CN": lambda _, m: idldsdcn_color(dict_graph, m),
    }

    summary_data = []

    for name, algo in algorithms.items():
        print(f"Running {name}...")
        start = time.time()
        coloring = algo(None, max_node)
        end = time.time()

        num_colors, num_conflicts = evaluate_coloring(dict_graph, coloring)
        elapsed = end - start

        summary_data.append((name, num_colors, num_conflicts, elapsed))

    # Write results to summary_report.txt
    with open("summary_report.txt", "w") as f:
        f.write(f"Graph Statistics:\n")
        f.write(f"Nodes       : {num_nodes}\n")
        f.write(f"Edges       : {num_edges}\n")
        f.write(f"Max Degree  : {max_degree}\n")
        f.write(f"Avg Degree  : {avg_degree:.2f}\n")
        f.write(f"Self-loops  : {self_loops}\n")
        f.write(f"Duplicates  : {duplicates}\n\n")

        f.write(f"{'Algorithm':<15} | {'Colors Used':<12} | {'Conflicts':<10} | {'Time (s)':<10}\n")
        f.write("-" * 60 + "\n")
        for name, colors, conflicts, seconds in summary_data:
            f.write(f"{name:<15} | {colors:<12} | {conflicts:<10} | {seconds:<10.4f}\n")


if __name__ == "__main__":
    main()
