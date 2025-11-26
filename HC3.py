import networkx as nx
import random
from collections import Counter

class HC3:
    def __init__(self, graph, max_iterations=100):
        self.graph = graph
        self.max_iterations = max_iterations
        # Initialize labels: each node has its own label initially
        self.labels = {node: node for node in self.graph.nodes()}
        # Variável para armazenar a partição (necessária para self.modularity() e __repr__)
        self.partition = []
        self.n_partitions = 0

    def _get_community_data(self, partition):
        """Calcula dados pré-processados para cálculo incremental de modularidade."""
        m = self.graph.number_of_edges()
        if m == 0:
            return {}, 0
        
        community_data = {}
        for comm in partition:
            nodes = set(comm)
            # Soma dos graus internos (grau(u) para u em C, arestas internas contadas 2x)
            dc = sum(self.graph.degree(u) for u in nodes)
            
            # Contagem das arestas internas (lc = L_c)
            lc = 0
            for u in nodes:
                for v in self.graph.neighbors(u):
                    if v in nodes:
                        lc += 1
            lc /= 2  # Cada aresta interna contada duas vezes
            
            # Armazena lc (arestas internas) e dc (soma dos graus)
            community_data[tuple(sorted(nodes))] = {'lc': lc, 'dc': dc}
            
        return community_data, m

    def _modularity_gain(self, node, old_comm_nodes, new_comm_nodes, community_data, m):
        """
        Calcula o ganho de modularidade (Delta Q) ao mover 'node' de 'old_comm' para 'new_comm'.
        O ganho é dado por: 
        Delta Q = [Q(new_comm_with_node) - Q(new_comm_without_node)] + [Q(old_comm_without_node) - Q(old_comm_with_node)]
        
        O cálculo utiliza as propriedades da modularidade:
        Q_c = (lc / m) - (dc / (2*m))^2
        Onde:
        - lc é o número de arestas internas
        - dc é a soma dos graus dos nós da comunidade
        """
        if m == 0:
            return 0.0

        # Propriedades do nó
        k_i = self.graph.degree(node) # Grau total do nó i
        
        # 1. Movimento de Saída (old_comm)
        k_i_in_old = 0
        for neighbor in self.graph.neighbors(node):
            if neighbor in old_comm_nodes:
                k_i_in_old += 1
        
        # A nova modularidade de 'old_comm' após a saída do nó i
        # É mais eficiente calcular o ganho:
        # Delta Q_out = [2 * k_i_in_old - k_i * dc_old / m] / (2 * m)
        # Onde:
        # k_i_in_old = número de arestas entre i e old_comm (antes da saída)
        # dc_old = soma dos graus da old_comm (antes da saída)
        dc_old = community_data[tuple(sorted(old_comm_nodes))]['dc']
        delta_Q_out = -(k_i_in_old / m) + (dc_old * k_i - k_i**2) / (2 * m**2)

        # 2. Movimento de Entrada (new_comm)
        k_i_in_new = 0
        for neighbor in self.graph.neighbors(node):
            if neighbor in new_comm_nodes:
                k_i_in_new += 1

        # A nova modularidade de 'new_comm' após a entrada do nó i
        # Delta Q_in = [2 * k_i_in_new - k_i * dc_new / m] / (2 * m)
        # Onde:
        # k_i_in_new = número de arestas entre i e new_comm (antes da entrada)
        # dc_new = soma dos graus da new_comm (antes da entrada)
        dc_new = community_data[tuple(sorted(new_comm_nodes))]['dc']
        delta_Q_in = (k_i_in_new / m) - (dc_new * k_i) / (2 * m**2)
        
        return delta_Q_in + delta_Q_out


    def remove_redundancy(self):
        """
        Versão Otimizada: Usa o cálculo de ganho de modularidade (Delta Q)
        para acelerar o processo de refinamento local.
        """
        m = self.graph.number_of_edges()
        if m == 0:
            return

        improved = True
        while improved:
            improved = False
            
            # --- 1. Inicialização da Iteração ---
            community_data, _ = self._get_community_data(self.partition)
            
            communities = {}
            for comm_list in self.partition:
                key = tuple(sorted(comm_list))
                communities[key] = set(comm_list)

            # --- 2. Iteração sobre os Nós ---
            for node in self.graph.nodes():
                old_comm_key = next(k for k, v in communities.items() if node in v)
                old_comm_nodes = communities[old_comm_key]
                
                neighbor_comm_keys = {
                    k for neighbor in self.graph.neighbors(node)
                    for k, v in communities.items() if neighbor in v and k != old_comm_key
                }
                
                best_key = old_comm_key
                max_delta_Q = 0.0

                for nc_key in neighbor_comm_keys:
                    new_comm_nodes = communities[nc_key]
                    
                    # Calcula o ganho de modularidade se o nó for movido
                    delta_Q = self._modularity_gain(
                        node, old_comm_nodes, new_comm_nodes, community_data, m
                    )
                    
                    if delta_Q > max_delta_Q:
                        max_delta_Q = delta_Q
                        best_key = nc_key
                        
                # --- 3. Movimento Bem-Sucedido (Refinamento) ---
                if max_delta_Q > 1e-6:
                    
                    # Dados do nó
                    k_i = self.graph.degree(node)
                    
                    # A comunidade antiga
                    old_data = community_data[old_comm_key]
                    k_i_in_old = sum(1 for neighbor in self.graph.neighbors(node) if neighbor in old_comm_nodes)
                    
                    # A nova comunidade
                    new_data = community_data[best_key]
                    k_i_in_new = sum(1 for neighbor in self.graph.neighbors(node) if neighbor in communities[best_key])
                    
                    # Executa o movimento
                    old_comm_nodes.remove(node)
                    communities[best_key].add(node)
                    improved = True

                    # --- CORREÇÃO: ATUALIZAÇÃO INCREMENTAL DOS DADOS ---
                    
                    # 1. Atualiza a comunidade que PERDEU o nó (old_comm_key)
                    old_data['lc'] -= k_i_in_old # Arestas internas reduzidas
                    old_data['dc'] -= k_i        # Soma dos graus reduzida
                    
                    # 2. Atualiza a comunidade que GANHOU o nó (best_key)
                    new_data['lc'] += k_i_in_new # Arestas internas aumentadas
                    new_data['dc'] += k_i        # Soma dos graus aumentada
                    
                    # 3. Gerencia as Chaves (Keys)
                    
                    # Se a comunidade antiga ficou vazia, ela é removida e sua chave deletada
                    if not old_comm_nodes:
                        del communities[old_comm_key]
                        del community_data[old_comm_key]
                    else:
                        # Se não ficou vazia, sua chave MUDA!
                        # Remove a chave antiga de ambos os dicionários
                        old_data = community_data.pop(old_comm_key)
                        communities.pop(old_comm_key)
                        
                        # Cria a nova chave e reatribui o conjunto de nós e os dados
                        new_old_key = tuple(sorted(old_comm_nodes))
                        communities[new_old_key] = old_comm_nodes
                        community_data[new_old_key] = old_data
                    
                    # A chave da comunidade que ganhou o nó TAMBÉM MUDA
                    # 
                    # Salva os dados atualizados antes de mudar a chave
                    new_data = community_data.pop(best_key)
                    
                    # Cria a nova chave e reatribui o conjunto de nós e os dados
                    new_new_key = tuple(sorted(communities[best_key]))
                    communities[new_new_key] = communities.pop(best_key) # Mudar a chave no dict 'communities'
                    community_data[new_new_key] = new_data
                    
                    # A partir daqui, as chaves de communities e community_data estão consistentes 
                    # com a nova partição.
            
            # Atualiza a partição para a próxima iteração do 'while improved'
            self.partition = [list(c) for c in communities.values() if c]
            
    # Os métodos 'modularity' e 'execute' permanecem os mesmos (exceto a inicialização de self.partition em __init__)
    def _modularity(self):
        m = self.graph.number_of_edges()
        Q = 0
        for community in self.partition:
            community_nodes = set(community)
            lc = 0 
            dc = 0 
            for u in community_nodes:
                dc += self.graph.degree(u)
                for v in self.graph.neighbors(u):
                    if v in community_nodes:
                        lc += 1
            lc /= 2
            if m > 0:
                Q += (lc / m) - (dc / (2 * m))**2
        return Q


    def execute(self, optmize=False):
        """Executes the Label Propagation Algorithm."""
        for i in range(self.max_iterations):
            nodes_to_process = list(self.graph.nodes())
            random.shuffle(nodes_to_process)
            
            labels_changed = False

            for node in nodes_to_process:
                if not self.graph.neighbors(node):
                    continue

                # Get labels of neighbors
                neighbor_labels = [self.labels[neighbor] for neighbor in self.graph.neighbors(node)]
                
                # Find the most frequent label among neighbors
                if not neighbor_labels:
                    continue
                
                label_counts = Counter(neighbor_labels)
                max_freq = max(label_counts.values())
                most_frequent_labels = [
                    label for label, count in label_counts.items() if count == max_freq
                ]
                
                # Randomly pick one in case of a tie
                new_label = random.choice(most_frequent_labels)
                
                if self.labels[node] != new_label:
                    self.labels[node] = new_label
                    labels_changed = True
            
            # If no labels changed in a full iteration, we have converged
            if not labels_changed:
                break
        
        # Group nodes by their final labels
        communities = {}
        for node, label in self.labels.items():
            if label not in communities:
                communities[label] = []
            communities[label].append(node)
        
        # Inicializa self.partition (correção do erro anterior)
        self.partition = list(communities.values())
        
        if optmize:
            self.remove_redundancy()
        
        self.n_partitions = len(self.partition)
        return list(communities.values())


    def __repr__(self):
        # Garante que 'self.partition' tenha sido inicializada, se 'execute' foi chamado
        if not self.partition:
            return "O algoritmo ainda não foi executado ou o grafo está vazio."

        return f"O algoritmo gerou {len(self.partition)} comunidades, com modularidade igual a {self._modularity()}"