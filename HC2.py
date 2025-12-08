
import networkx as nx
from collections import defaultdict

class HC2:
    def __init__(self, graph):
        self.graph = graph
        self.partition = []
        self.n_partitions = 0

    def community_ratio(self, community):
        e_in=0
        e_out=0
        for node in community:
            for neighbor in self.graph.neighbors(node):
                if neighbor in community:
                    e_in += 1
                else:
                    e_out += 1
        e_in = e_in // 2
        return e_in / (e_out + 1)


    def _calculate_heuristic_gain(self, node, community):
        e_in=0
        e_out=0
        for neighbor in self.graph.neighbors(node):
            if neighbor in community:
                e_in += 1
            else:
                e_out += 1

        return e_in / (e_out + 1)
    
    def remove_redundancy(self):
        improved = True
        while improved:
            improved = False
            for node in self.graph.nodes():
                current_comm = next(c for c in self.partition if node in c)
                neighbor_comms = [c for c in self.partition if any(n in c for n in self.graph.neighbors(node)) and c != current_comm]
                
                best_comm = current_comm
                best_mod = self._modularity()
                
                for nc in neighbor_comms:
                    current_comm.remove(node)
                    nc.append(node)
                    new_mod = self._modularity()
                    
                    if new_mod > best_mod:
                        best_mod = new_mod
                        best_comm = nc
                        improved = True
                    
                    nc.remove(node)
                    current_comm.append(node)
                
                if best_comm is not current_comm:
                    current_comm.remove(node)
                    best_comm.append(node)


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
        sorted_nodes = sorted(self.graph.nodes(), key=self.graph.degree, reverse=True)
        unassigned_nodes = set(self.graph.nodes())

        for node in sorted_nodes:
            if node in unassigned_nodes:
                new_community = {node}
                unassigned_nodes.remove(node)
                
                candidate_set = {neighbor for neighbor in self.graph.neighbors(node) if neighbor in unassigned_nodes}
                
                current_ratio = self.community_ratio(new_community)

                while True:
                    best_candidate = None
                    best_gain = current_ratio
                    
                    for candidate in candidate_set:
                        gain = self._calculate_heuristic_gain(candidate, new_community)
                        if gain > best_gain:
                            best_gain = gain
                            best_candidate = candidate
                    
                    if best_candidate is None:
                        break
                        
                    new_community.add(best_candidate)
                    unassigned_nodes.remove(best_candidate)
                    candidate_set.remove(best_candidate)
                    
                    current_ratio = best_gain
                    
                    new_neigbors = {neighbor for neighbor in self.graph.neighbors(best_candidate) if neighbor in unassigned_nodes}
                    candidate_set.update(new_neigbors)
                
                self.partition.append(list(new_community))
        
        if optmize:
            self.remove_redundancy()
        
        self.n_partitions = len(self.partition)
        return self.partition
    
    def __repr__(self):
        return f"O algoritmo gerou {len(self.partition)} comunidades, com modularidade igual a {self._modularity()}"