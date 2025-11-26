import networkx as nx
import matplotlib.pyplot as plt
from scipy.io import mmread
from time import time
from tabulate import tabulate

import HC1, HC2, HC3, LocalSearch


def run_algorithm(alg_class, graph, name):
    """Executa algoritmo e retorna resultados em lista de dicts."""
    print(f"🔹 Executando algoritmo: {alg_class.__name__}")
    print(f"Rede: {name}")
    print(f"Nós: {graph.number_of_nodes()}")
    print(f"Arestas: {graph.number_of_edges()}")
    results = []
    for opt in [False, True]:
        algo = alg_class(graph)
        start = time()
        algo.execute(optmize=opt)
        duration = time() - start
        results.append({
            "Algoritmo": alg_class.__name__,
            "Rede": name,
            "Otimizado": "Sim" if opt else "Não",
            "Comunidades": getattr(algo, "n_partitions", None),
            "Modularidade": algo._modularity() if algo.partition else None,
            "Tempo (s)": round(duration, 4),
            "Objeto": algo
        })
    return results


def print_table(results):
    """Exibe resultados no terminal em formato de tabela."""
    print(results)
    table = [
        [r["Algoritmo"], r["Rede"], r["Otimizado"], r["Comunidades"],
        f"{r['Modularidade']:.4f}" if r["Modularidade"] is not None else "-",
        r["Tempo (s)"]]
        for r in results
    ]
    print(tabulate(
        table,
        headers=["Algoritmo", "Rede", "Otimizado", "Comunidades", "Modularidade", "Tempo (s)"],
        tablefmt="fancy_grid"
    ))


def plot_partition(graph, algo, title):
    """Plota grafo colorido conforme as comunidades encontradas."""
    node_colors = {}
    for i, comm in enumerate(algo.partition):
        for node in comm:
            node_colors[node] = f"C{i}"
    nx.set_node_attributes(graph, node_colors, "color")

    plt.figure(figsize=(6, 5))
    nx.draw(
        graph,
        node_color=list(nx.get_node_attributes(graph, "color").values()),
        with_labels=False,
        node_size=80,
    )
    plt.title(title)
    plt.savefig(f"{title}.png")
    plt.close()

def process_network(graph, name):
    """Executa todos os algoritmos e mostra resultados + plots."""
    print(f"\n🔹 Processando rede: {name}")
    partition = nx.community.greedy_modularity_communities(graph)
    modularity = nx.community.modularity(graph, partition)
    print(f"Greedy: {len(partition)} comunidades | modularidade = {modularity:.4f}\n")

    results = []
    for alg in [HC1.HC1, HC2.HC2, HC3.HC3]:
        results += run_algorithm(alg, graph, name)
        
    local_search_results = []
    for r in results:
        if r["Otimizado"] == "Sim":
            print(f"\n🔹 Executando Local Search para: {r['Algoritmo']} (Otimizado)")
            ls = LocalSearch.LocalSearch(r["Objeto"], network_name=name, original_modularity=r["Modularidade"])
            start = time()
            ls.run_local_search(r["Objeto"].partition)
            duration = time() - start
            
            local_search_results.append({
                "Algoritmo": f"{r['Algoritmo']} + Local Search",
                "Rede": name,
                "Otimizado": "Sim",
                "Comunidades": len(ls.best_partition),
                "Modularidade": ls.modularity(ls.h.graph, ls.best_partition),
                "Tempo (s)": round(duration, 4),
                "Objeto": ls
            })
    
    final_results = results + local_search_results
    print_table(final_results)

    # Mostrar gráficos
    for r in results:
        if r["Otimizado"] == "Sim":
            plot_partition(graph, r["Objeto"], f"{r['Rede']} - {r['Algoritmo']} (Otimizado)")
            continue
        if "Local Search" in r["Algoritmo"] :
            plot_partition(graph, r["Objeto"], f"{r['Rede']} - {r['Algoritmo']} (Local Search)")
            continue
        plot_partition(graph, r["Objeto"], f"{r['Rede']} - {r['Algoritmo']}")


    return final_results


# Redes
g_karate = nx.karate_club_graph()
g_golfinhos = nx.Graph(mmread("./soc-dolphins.mtx"))
g_futebol = nx.read_gml("./football.gml")

# Execução geral
results_all = []
results_all += process_network(g_karate, "Karatê")
# results_all += process_network(g_golfinhos, "Golfinhos")
# results_all += process_network(g_futebol, "Futebol Americano")

# Resumo final
print("\n📊 RESULTADOS FINAIS")
print_table(results_all)
