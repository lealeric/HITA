
import networkx as nx
import matplotlib.pyplot as plt
import HC3
from time import time
import random

# Stochastic Model setup from Entrega1.py
sizes = [75, 75, 300]
probs = [[0.25, 0.05, 0.02], [0.05, 0.35, 0.07], [0.02, 0.07, 0.40]]
g_estocastico = nx.stochastic_block_model(sizes, probs, seed=0)


output_file = "check_results.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"Stochastic Graph: {g_estocastico.number_of_nodes()} nodes, {g_estocastico.number_of_edges()} edges\n")

    # Run HC3 (Algorithm 3)
    f.write("Running HC3 (Label Propagation)...\n")
    hc3 = HC3.HC3(g_estocastico, max_iterations=100)
    start = time()
    partition = hc3.execute(optmize=False)
    duration = time() - start

    f.write(f"Time: {duration:.4f}s\n")
    f.write(f"Number of communities: {len(partition)}\n")
    f.write(f"Modularity: {hc3._modularity()}\n")
    sizes_found = [len(c) for c in partition]
    f.write(f"Partition sizes: {sizes_found}\n")

    # Run with optimization
    f.write("\nRunning HC3 (Label Propagation) with Optimization...\n")
    hc3_opt = HC3.HC3(g_estocastico, max_iterations=100)
    start = time()
    partition_opt = hc3_opt.execute(optmize=True)
    duration = time() - start

    f.write(f"Time: {duration:.4f}s\n")
    f.write(f"Number of communities (Optimized): {len(partition_opt)}\n")
    f.write(f"Modularity (Optimized): {hc3_opt._modularity()}\n")
    sizes_found_opt = [len(c) for c in partition_opt]
    f.write(f"Partition sizes (Optimized): {sizes_found_opt}\n")

print(f"Results written to {output_file}")

