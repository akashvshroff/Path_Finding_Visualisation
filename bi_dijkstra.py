import heapq


class BiDijkstraAlgorithm:
    def __init__(self, adj, cost, s, t):
        """
        Initialises the data structures needed for the bi-dijkstra algorithm
        as well as calls upon method to find the reverse graph.
        A _r suffix indicates a data structure used in the backward direction.
        """
        self.s = s
        self.t = t
        self.adj = adj
        self.cost = cost
        self.adj_r = None
        self.cost_r = None
        self.dist = {self.s: 0}
        self.dist_r = {self.t: 0}
        self.proc = {}
        self.proc_r = {}
        self.q = [(0, self.s)]
        self.q_r = [(0, self.t)]
        self.found_path = False
        heapq.heapify(self.q)
        heapq.heapify(self.q_r)
        self.reverse_graph()

    def reverse_graph(self):
        """
        Reverse adj and cost to get adj_r and cost_r.
        """
        self.adj_r = {node: [] for node in self.adj.keys()}
        self.cost_r = {node: [] for node in self.cost.keys()}
        for u in self.adj.keys:
            for id, v in enumerate(self.adj[u]):
                self.adj_r[v].append(u)
                self.cost_r[v].append(self.cost[u][id])

    def solver_vis(self):
