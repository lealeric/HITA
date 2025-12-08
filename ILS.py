import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import imageio
from random import choice, random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class ILS:
    def __init__(self, h, network_name: str, original_modularity: float, max_iterations=1000, k=5):
        """Executa o Iterated Local Search

        Args:
            h: Objeto que implementa a heurística
            network_name (str): Nome da rede
            original_modularity (float): Modularity inicial da rede
            max_iterations (int, optional): Número máximo de iterações. Defaults to 1000.
            k (int, optional): Quantidade de nós a serem trocados. Defaults to 5.
        """
        self.h = h
        self.network_name = network_name
        self.original_modularity = original_modularity
        self.max_iterations = max_iterations
        self.k = k
        self.frames = []
        self.pos = None
        self.node_colors = {}
        self.used_colors = set()
        self.best_partition = None

    def random_color(self):
        return (random(), random(), random())
        

    @staticmethod
    def draw_partition(graph, partition, title=""):
        plt.figure(figsize=(6, 6))
        
        pos = nx.spring_layout(graph, seed=42)

        colors = {}
        for i, comm in enumerate(partition):
            color = (random(), random(), random())
            for node in comm:
                colors[node] = color

        node_colors = [colors[node] for node in graph.nodes()]

        nx.draw_networkx(
            graph,
            pos=pos,
            node_color=node_colors,
            with_labels=True,
            node_size=500,
            font_color="white"
        )

        plt.title(title)
        plt.show()
    
    def modularity(self, graph, partition):
        m = graph.number_of_edges()
        Q = 0
        for community in partition:
            community_nodes = set(community)
            lc = 0 
            dc = 0 
            for u in community_nodes:
                dc += graph.degree(u)
                for v in graph.neighbors(u):
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


    def local_search(self, graph, partition):
        melhoria = True
        
        if not hasattr(self, "changed"):
            self.changed = set()
            
        while melhoria:
            melhoria = False
            for node in graph.nodes():
                current_comm = next(c for c in partition if node in c)
                neighbor_comms = [c for c in partition if any(n in c for n in graph.neighbors(node)) and c != current_comm]
                
                best_comm = current_comm
                best_mod = max(self.modularity(graph, partition), self.original_modularity)
                # print("🐍 File: HITA/ILS.py | Line: 127 | local_search ~ self.original_modularity",self.original_modularity)
                # print("🐍 File: HITA/ILS.py | Line: 127 | local_search ~ self.modularity(graph, partition",self.modularity(graph, partition))
                # print("🐍 File: HITA/ILS.py | Line: 127 | local_search ~ best_mod",best_mod)
                
                for nc in neighbor_comms:
                    current_comm.remove(node)
                    nc.append(node)
                    new_mod = self.modularity(graph, partition)
                    
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
    
    def disturb(self):
        chosen_nodes = []
        for _ in range(self.k):
            v = choice(list(self.h.graph.nodes()))
            while v in chosen_nodes:
                v = choice(list(self.h.graph.nodes()))
            chosen_nodes.append(v)
        
        for node in chosen_nodes:
            try:
                current_comm = next(c for c in self.h.partition if node in c)
                other_comms = [c for c in self.h.partition if c is not current_comm]

                if not other_comms:
                    continue

                current_comm.remove(node)
                
                new_comm = choice(other_comms)
                new_comm.append(node)

                self.h.partition = [c for c in self.h.partition if c]
            except StopIteration:
                continue

        return self.h.partition

    def save_images(self):
        plt.figure(figsize=(6,6))
        
        for comm in self.best_partition:
            color = self.random_color()
            self.used_colors.add(color)
            for node in comm:
                self.node_colors[node] = color
                
        nx.draw(
            self.h.graph,
            pos=self.pos,
            node_color=[self.node_colors[n] for n in self.h.graph.nodes()],
            with_labels=False,
            node_size=120
        )
        plt.title(f"Partição Final - {self.network_name}")
        final_png = f"Final_{self.network_name}_ILS.png"
        plt.savefig(final_png)
        plt.close()

        # GIF
        gif_name = f"ILS_{self.network_name}_{self.h.__class__.__name__}.gif"
        if len(self.frames) > 0:
            imageio.mimsave(gif_name, self.frames, fps=2)
            print(f"GIF salvo em: {gif_name}")
        else:
            print("Nenhum frame para salvar.")
        print(f"PNG salvo em: {final_png}")

    def run_algorithm(self):
        if self.pos is None:
            self.pos = nx.spring_layout(self.h.graph, seed=42)

        for comm in self.h.partition:
            color = self.random_color()
            self.used_colors.add(color)
            for node in comm:
                self.node_colors[node] = color
            
        partition = self.local_search(self.h.graph, self.h.partition)
        self.best_partition = partition
        
        # for i in range(self.max_iterations):
        #     print(f"Iteração {i+1}/{self.max_iterations}")
        #     new_partition = self.disturb()
        #     new_partition = self.local_search(self.h.graph, new_partition)
            
        #     if self.modularity(self.h.graph, new_partition) > self.modularity(self.h.graph, self.best_partition):
        #         self.best_partition = new_partition
                
        
        # plt.figure(figsize=(6,6))
        # nx.draw(
        #     self.h.graph,
        #     pos=self.pos,
        #     node_color=[self.node_colors[n] for n in self.h.graph.nodes()],
        #     with_labels=False,
        #     node_size=120
        # )
        # plt.title(f"Partição Final - {self.network_name}")
        # final_png = f"Final_{self.network_name}_ILS.png"
        # plt.savefig(final_png)
        # plt.close()

        # gif_name = f"ILS_{self.network_name}_{self.h.__class__.__name__}.gif"
        # imageio.mimsave(gif_name, self.frames, fps=2)

        # print(f"GIF salvo em: {gif_name}")
        # print(f"PNG salvo em: {final_png}")
        
        return self.best_partition
        
        