import networkx as nx

class HC1:
    def __init__(self, graph):
        self.graph = graph
        self.m = self.graph.number_of_edges()
        self.communities = {node: frozenset([node]) for node in self.graph.nodes()}
        self.partition = [[node] for node in self.graph.nodes()]
        self.n_partitions = len(self.partition)

        self.delta_q = {}
        for i in range(len(self.partition)):
            for j in range(i + 1, len(self.partition)):
                comm_i = self.partition[i]
                comm_j = self.partition[j] 
                
                if self._are_communities_adjacent(comm_i, comm_j):
                    dq = self._calculate_delta_q(comm_i, comm_j)
                    self.delta_q[tuple(sorted((frozenset(comm_i), frozenset(comm_j))))] = dq

    def _are_communities_adjacent(self, comm1, comm2):
        for node1 in comm1:
            for node2 in comm2:
                if self.graph.has_edge(node1, node2):
                    return True
        return False

    def _calculate_delta_q(self, comm1, comm2):
        """Calcula a variação de modularidade ao juntar comm1 e comm2.
        Usa a mesma convenção que modularity(): lc é contado uma vez, m = number_of_edges().
        """
        # soma dos graus em cada comunidade
        k_i = sum(self.graph.degree(node) for node in comm1)
        k_j = sum(self.graph.degree(node) for node in comm2)
        
        edges_between = 0
        for node1 in comm1:
            for node2 in comm2:
                if self.graph.has_edge(node1, node2):
                    edges_between += 1
                    
        # ΔQ = (edges_between / (2*m)) - ((k_i * k_j) / (4 * m**2))
        # Não multiplicamos por 2 aqui — manter consistência com modularity().
        delta_q = (edges_between / (2 * self.m)) - ((k_i * k_j) / (4 * self.m**2))
        return delta_q

    def _get_community_neighbors(self, community):
        """Find all communities adjacent to a given community."""
        neighbors = set()
        for i in range(len(self.partition)):
            other_comm = self.partition[i]
            if frozenset(community) != frozenset(other_comm):
                if self._are_communities_adjacent(community, other_comm):
                    neighbors.add(frozenset(other_comm))
        return neighbors

    def _modularity(self):
        """Computa modularidade com lc contado uma vez por aresta interna.
        Fórmula: Q = sum_c [ lc/(2m) - (dc/(2m))^2 ]
        """
        m = self.graph.number_of_edges()
        if m == 0:
            return 0.0

        Q = 0.0
        for community in self.partition:
            lc = 0 
            for u in community:
                for v in community:
                    # contar cada aresta interna uma vez
                    if u > v and self.graph.has_edge(u, v):
                        lc += self.graph[u][v].get('weight', 1)
            
            dc = sum(self.graph.degree(node) for node in community)
            # usar lc/(2*m) (pois lc foi contado uma vez)
            Q += (lc / (2 * m)) - (dc / (2 * m))**2
        return Q

    def remove_redundancy(self):
        """Remove vértices redundantes: para cada vértice na fronteira, testa realocação para comunidades vizinhas.
        Aceita mudança somente se modularidade aumentar. Repete até convergência.
        """
        improved = True
        # itera até não haver melhorias
        while improved:
            improved = False
            # percorre cópia dos nós (para evitar alterações durante iteração)
            for node in list(self.graph.nodes()):
                # encontra comunidade atual do nó
                current_comm = None
                for c in self.partition:
                    if node in c:
                        current_comm = c
                        break
                if current_comm is None:
                    continue

                # comunidades vizinhas (que possuem algum vizinho do node)
                neighbor_comms = []
                for c in self.partition:
                    if c is current_comm:
                        continue
                    # checa se c contém algum vizinho de node
                    if any(self.graph.has_edge(node, nbr) for nbr in c):
                        neighbor_comms.append(c)

                if not neighbor_comms:
                    continue

                best_mod = self._modularity()
                best_comm = current_comm

                # testar mover para cada comunidade vizinha
                for nc in neighbor_comms:
                    # aplica mudança temporária
                    current_comm.remove(node)
                    nc.append(node)

                    new_mod = self._modularity()

                    # desfaz mudança
                    nc.remove(node)
                    current_comm.append(node)

                    if new_mod > best_mod + 1e-12:  # tolerância numérica
                        best_mod = new_mod
                        best_comm = nc

                # se encontrou melhoria, aplica de verdade (primeira melhoria aceita)
                if best_comm is not current_comm:
                    current_comm.remove(node)
                    best_comm.append(node)
                    improved = True

    def execute(self, optmize=False):
        while self.delta_q and max(self.delta_q.values()) > 1e-12: # Usar tolerância numérica
            max_dq_pair, max_dq = max(self.delta_q.items(), key=lambda item: item[1])
            
            comm1_fs, comm2_fs = max_dq_pair
            
            # 1. Encontrar as instâncias de listas originais na partição
            comm1_original_list = None
            comm2_original_list = None
            
            partition_copy = list(self.partition) # Trabalhar em uma cópia para iterar
            
            for comm_list in partition_copy:
                if frozenset(comm_list) == comm1_fs:
                    comm1_original_list = comm_list
                elif frozenset(comm_list) == comm2_fs:
                    comm2_original_list = comm_list

            if comm1_original_list is None or comm2_original_list is None:
                # Se não encontrar, pode ter havido uma inconsistência; pular ou parar
                # Neste caso, vamos apenas parar
                break 

            # 2. Remover as instâncias de listas originais e criar a nova comunidade
            try:
                self.partition.remove(comm1_original_list)
                self.partition.remove(comm2_original_list)
            except ValueError:
                # Não deveríamos chegar aqui se a lógica acima estiver correta
                break

            new_comm = comm1_original_list + comm2_original_list
            self.partition.append(new_comm)

            # O resto da lógica de atualização do delta_q está correta para chaves frozenset
            keys_to_remove = []
            for pair in list(self.delta_q.keys()):
                if comm1_fs in pair or comm2_fs in pair:
                    keys_to_remove.append(pair)
            for key in keys_to_remove:
                self.delta_q.pop(key, None)

            new_comm_fs = frozenset(new_comm)
            
            # Recalcular apenas com comunidades que AINDA estão na partição
            for neighbor_list in self.partition:
                if neighbor_list is not new_comm:
                    neighbor_fs = frozenset(neighbor_list)
                    # Não é necessário checar adjacência, basta calcular o delta_q
                    dq = self._calculate_delta_q(new_comm, neighbor_list)
                    # Adicionar a nova tupla de frozenset como chave
                    key = tuple(sorted((new_comm_fs, neighbor_fs))) 
                    self.delta_q[key] = dq
                
        if optmize:
            self.remove_redundancy()
        
        self.n_partitions = len(self.partition)
        return self.partition

    def __repr__(self):
        return f"O algoritmo gerou {len(self.partition)} comunidades, com modularidade igual a {self._modularity()}"
