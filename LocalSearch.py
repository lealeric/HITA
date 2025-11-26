from random import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import imageio

class LocalSearch:
    def __init__(self, h, network_name: str, original_modularity: float):
        self.best_partition = None
        self.h = h
        self.network_name = network_name
        self.original_modularity = original_modularity
        self.frames = []
        self.pos = None
        self.node_colors = {}
        self.used_colors = set()
        self.best_partition = None
        
    def random_color(self):
        return (random(), random(), random())
        
    def modularity(self, partition):
        m = self.h.graph.number_of_edges()
        Q = 0
        for community in partition:
            community_nodes = set(community)
            lc = 0
            dc = 0
            for u in community_nodes:
                dc += self.h.graph.degree(u)
                for v in self.h.graph.neighbors(u):
                    if v in community_nodes:
                        lc += 1
            lc /= 2
            if m > 0:
                Q += (lc / m) - (dc / (2 * m))**2
        return Q
        
    def save_frame(self, title=""):
        """Captura o frame atual do grafo para gerar o GIF"""

        fig = plt.figure(figsize=(6, 6))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        node_colors = [self.node_colors[node] for node in self.h.graph.nodes()]

        nx.draw(
            self.h.graph,
            pos=self.pos,
            node_color=node_colors,
            with_labels=False,
            node_size=120,
            ax=ax
        )

        ax.set_title(title)
        canvas.draw()

        # compatibilidade RGB / ARGB
        try:
            buf = canvas.tostring_rgb()
            frame = np.frombuffer(buf, dtype="uint8")
            frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        except AttributeError:
            buf = canvas.tostring_argb()
            frame = np.frombuffer(buf, dtype="uint8")
            frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (4,))
            frame = frame[:, :, 1:]  # ARGB → RGB

        self.frames.append(frame)
        plt.close(fig)

    def run_local_search(self, partition):
        melhoria = True
        
        if not hasattr(self, "changed"):
            self.changed = set()
            
        while melhoria:
            melhoria = False
            for node in self.h.graph.nodes():
                current_comm = next(c for c in partition if node in c)
                neighbor_comms = [c for c in partition if any(
                    n in c for n in self.h.graph.neighbors(node))
                    and c != current_comm]
                
                best_comm = current_comm
                best_mod = max(self.modularity(partition),
                               self.original_modularity)
                
                for nc in neighbor_comms:
                    current_comm.remove(node)
                    nc.append(node)
                    new_mod = self.modularity(partition)
                    
                    if new_mod > best_mod:
                        best_mod = new_mod
                        best_comm = nc
                        melhoria = True
                    
                    nc.remove(node)
                    current_comm.append(node)
                    
                if best_comm is not current_comm:
                    current_comm.remove(node)
                    best_comm.append(node)
                    
                    if node not in self.changed:

                        new_color = self.random_color()

                        while new_color in self.used_colors:
                            new_color = self.random_color()

                        self.used_colors.add(new_color)
                        self.node_colors[node] = new_color
                        self.changed.add(node)
                    
                    # ILS.draw_partition(graph, partition, title=f"Nó {node} movido")
                    self.save_frame(title=f"Nó {node} movido")
                    
        return partition