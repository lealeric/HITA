# import networkx as nx
# import matplotlib.pyplot as plt
# from scipy.io import mmread
# from time import time
# import HC1, HC2, HC3

# # Rede do clube de Karatê
# g_karate = nx.karate_club_graph()

# partition = nx.community.greedy_modularity_communities(g_karate)
# print(f"O algoritmo gerou {len(partition)} comunidades, com modularidade igual a {nx.community.modularity(g_karate, partition)}")

# t0 = time()
# h1_karate = HC1.HC1(g_karate)
# h1_karate.execute()
# print(f"Processado em {time() - t0} segundos")
# print(h1_karate)

# t0 = time()
# h1_karate_optimal = HC1.HC1(g_karate)
# h1_karate_optimal.execute(optmize=True)
# print(f"Processado em {time() - t0} segundos")
# print(h1_karate_optimal)

# t0 = time()
# h2_karate = HC2.HC2(g_karate)
# h2_karate.execute()
# print(f"Processado em {time() - t0} segundos")
# print(h2_karate)

# t0 = time()
# h2_karate_optimal = HC2.HC2(g_karate)
# h2_karate_optimal.execute(optmize=True)
# print(f"Processado em {time() - t0} segundos")
# print(h2_karate_optimal)

# t0 = time()
# h3_karate = HC3.HC3(g_karate)
# h3_karate.execute()
# print(f"Processado em {time() - t0} segundos")
# print(h3_karate)

# t0 = time()
# h3_karate_optimal = HC3.HC3(g_karate)
# h3_karate_optimal.execute(optmize=True)
# print(f"Processado em {time() - t0} segundos")
# print(h3_karate_optimal)


# # Rede de interação dos golfinhos
# g_golfinhos = nx.Graph(mmread('./soc-dolphins.mtx'))

# partition_golfinhos = nx.community.greedy_modularity_communities(g_golfinhos)
# print(f"O algoritmo gerou {len(partition_golfinhos)} comunidades, com modularidade igual a {nx.community.modularity(g_golfinhos, partition_golfinhos)}")

# t0 = time()
# h1_golfinhos = HC1.HC1(g_golfinhos)
# h1_golfinhos.execute()
# print(f"Processado em {time() - t0} segundos")
# print(h1_golfinhos)

# t0 = time()
# h1_golfinhos_optimal = HC1.HC1(g_golfinhos)
# h1_golfinhos_optimal.execute(optmize=True)
# print(f"Processado em {time() - t0} segundos")
# print(h1_golfinhos_optimal)

# t0 = time()
# h2_golfinhos = HC2.HC2(g_golfinhos)
# h2_golfinhos.execute()
# print(f"Processado em {time() - t0} segundos")
# print(h2_golfinhos)

# t0 = time()
# h2_golfinhos_optimal = HC2.HC2(g_golfinhos)
# h2_golfinhos_optimal.execute(optmize=True)
# print(f"Processado em {time() - t0} segundos")
# print(h2_golfinhos_optimal)

# t0 = time()
# h3_golfinhos = HC3.HC3(g_golfinhos)
# h3_golfinhos.execute()
# print(f"Processado em {time() - t0} segundos")
# print(h3_golfinhos)

# t0 = time()
# h3_golfinhos_optimal = HC3.HC3(g_golfinhos)
# h3_golfinhos_optimal.execute(optmize=True)
# print(f"Processado em {time() - t0} segundos")
# print(h3_golfinhos_optimal)



# # Rede Futebol Americano
# g_futebol = nx.read_gml('./football.gml')

# partition_futebol = nx.community.greedy_modularity_communities(g_futebol)
# print(f"O algoritmo gerou {len(partition_futebol)} comunidades, com modularidade igual a {nx.community.modularity(g_futebol, partition_futebol)}")

# t0 = time()
# h1_futebol = HC1.HC1(g_futebol)
# h1_futebol.execute()
# print(f"Processado em {time() - t0} segundos")
# print(h1_futebol)

# t0 = time()
# h1_futebol_optimal = HC1.HC1(g_futebol)
# h1_futebol_optimal.execute(optmize=True)
# print(f"Processado em {time() - t0} segundos")
# print(h1_futebol_optimal)

# t0 = time()
# h2_futebol = HC2.HC2(g_futebol)
# h2_futebol.execute()
# print(f"Processado em {time() - t0} segundos")
# print(h2_futebol)

# t0 = time()
# h2_futebol_optimal = HC2.HC2(g_futebol)
# h2_futebol_optimal.execute(optmize=True)
# print(f"Processado em {time() - t0} segundos")
# print(h2_futebol_optimal)

# t0 = time()
# h3_futebol = HC3.HC3(g_futebol)
# h3_futebol.execute()
# print(f"Processado em {time() - t0} segundos")
# print(h3_futebol)

# t0 = time()
# h3_futebol_optimal = HC3.HC3(g_futebol)
# h3_futebol_optimal.execute(optmize=True)
# print(f"Processado em {time() - t0} segundos")
# print(h3_futebol_optimal)


# # Plotando as redes

# node_colors_karate = {}

# for i, comm in enumerate(h1_karate_optimal.partition):
#     for node in comm:
#         node_colors_karate[node] = f'C{i}'

# nx.set_node_attributes(g_karate, node_colors_karate, 'color')

# node_colors_golfinhos = {}

# for i, comm in enumerate(h1_golfinhos_optimal.partition):
#     for node in comm:
#         node_colors_golfinhos[node] = f'C{i}'

# nx.set_node_attributes(g_golfinhos, node_colors_golfinhos, 'color')

# node_colors_futebol = {}

# for i, comm in enumerate(h1_futebol_optimal.partition):
#     for node in comm:
#         node_colors_futebol[node] = f'C{i}'

# nx.set_node_attributes(g_futebol, node_colors_futebol, 'color')

# plt.figure(figsize=(12, 10))

# ax1 = plt.subplot(2, 2, 1)
# nx.draw(g_karate, node_color=list(nx.get_node_attributes(g_karate, 'color').values()), ax=ax1)
# ax1.set_title('Karate Club')

# ax2 = plt.subplot(2, 2, 2)
# nx.draw(g_golfinhos, node_color=list(nx.get_node_attributes(g_golfinhos, 'color').values()), ax=ax2)
# ax2.set_title('Golfinhos')

# ax3 = plt.subplot(2, 2, 3)
# nx.draw(g_futebol, node_color=list(nx.get_node_attributes(g_futebol, 'color').values()), ax=ax3)
# ax3.set_title('Futebol Americano')

# plt.tight_layout()
# plt.show()


import networkx as nx
import matplotlib.pyplot as plt
from scipy.io import mmread
from time import time
from tabulate import tabulate

import HC1, HC2, HC3, ILS


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

    ils_results = []
    ils_durations = []
    print("🐍 File: HITA/Entrega1.py | Line: 263 | process_network ~ results",len(results))
    for r in results:
        if r["Otimizado"] == "Não":
            continue
        ils = ILS.ILS(r['Objeto'], max_iterations=100, network_name=name, original_modularity=r["Modularidade"]) # Altera aqui o max_iter, nome da rede e o parâmetro k
        start = time()
        new_partition = ils.run_algorithm()
        ils_durations.append(time() - start)
        duration = sum(ils_durations) / len(ils_durations)
        
        ils_result = {
            "Algoritmo": f"ILS({r['Algoritmo']})",
            "Rede": name,
            "Otimizado": r["Otimizado"],
            "Comunidades": len(new_partition),
            "Modularidade": ils.modularity(graph, new_partition),
            "Tempo (s)": round(duration, 4),
            "Objeto": r['Objeto'] 
        }
        ils_results.append(ils_result)
        
    ils.save_images()

    print_table(results + ils_results)

    # Mostrar gráficos
    for r in results:
        if r["Otimizado"] == "Sim":
            plot_partition(graph, r["Objeto"], f"{r['Rede']} - {r['Algoritmo']} (Otimizado)")
            continue
        if "ILS" in r["Algoritmo"] :
            plot_partition(graph, r["Objeto"], f"{r['Rede']} - {r['Algoritmo']} (ILS)")
            continue
        plot_partition(graph, r["Objeto"], f"{r['Rede']} - {r['Algoritmo']}")


    return results + ils_results


# Redes
g_karate = nx.karate_club_graph()
g_golfinhos = nx.Graph(mmread("./soc-dolphins.mtx"))
g_futebol = nx.read_gml("./football.gml")
g_miseraveis = nx.les_miserables_graph()
g_florentine = nx.florentine_families_graph()
g_erdos_100 = nx.erdos_renyi_graph(100, 0.01, seed=42)
print("Grafos Erdos 100 gerados com sucesso")
g_erdos_500 = nx.erdos_renyi_graph(500, 0.01, seed=42)
print("Grafos Erdos 500 gerados com sucesso")
g_erdos_1000 = nx.erdos_renyi_graph(1000, 0.01, seed=42)
print("Grafos Erdos 1000 gerados com sucesso")

print("Grafos gerados com sucesso")

# Execução geral
results_all = []
results_all += process_network(g_karate, "Karatê")
results_all += process_network(g_golfinhos, "Golfinhos")
results_all += process_network(g_futebol, "Futebol Americano")
results_all += process_network(g_miseraveis, "Les Miserables")
results_all += process_network(g_florentine, "Florentine")
results_all += process_network(g_erdos_100, "Erdos 100")
results_all += process_network(g_erdos_500, "Erdos 500")
results_all += process_network(g_erdos_1000, "Erdos 1000")

# Resumo final
print("\n📊 RESULTADOS FINAIS")
print_table(results_all)
