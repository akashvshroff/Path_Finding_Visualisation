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
        self.prev = {}
        self.prev_r = {}
        self.q = [(0, self.s)]
        self.q_r = [(0, self.t)]
        self.found_path = False
        self.path = []
        self.distance = None
        heapq.heapify(self.q)
        heapq.heapify(self.q_r)
        self.workset = set()
        self.reverse_graph()

    def reverse_graph(self):
        """
        Reverse adj and cost to get adj_r and cost_r.
        """
        self.adj_r = {node: [] for node in self.adj.keys()}
        self.cost_r = {node: [] for node in self.cost.keys()}
        for u in self.adj.keys():
            for id, v in enumerate(self.adj[u]):
                self.adj_r[v].append(u)
                self.cost_r[v].append(self.cost[u][id])

    def process(self, q, node, neighbours, costs, dist, prev):
        """
        Explores all the neighbours of a node and tries to relax the edges.
        """
        for id, vertex in enumerate(neighbours):
            if dist.get(vertex, float('inf')) > dist.get(node, float('inf')) + costs[id]:
                dist[vertex] = dist[node] + costs[id]
                prev[vertex] = node
                heapq.heappush(q, (dist[vertex], vertex))
            self.workset.add(vertex)

    def shortest_distance(self, vertex):
        """
        Calculates the shortest path from s to t.
        """
        try:
            self.distance = self.dist[vertex] + self.dist_r[vertex]
        except KeyError:
            return
        u_best = vertex  # middle node that is best
        for v in self.workset:
            dst = self.dist.get(v, float('inf')) + \
                self.dist_r.get(v, float('inf'))
            if dst < self.distance:
                u_best = v
                self.distance = dst
        last = u_best
        while last != self.s:
            self.path.append(last)
            last = self.prev[last]
        self.path.append(last)
        self.path.reverse()
        last = u_best
        while last != self.t:
            last = self.prev_r[last]
            self.path.append(last)
        self.found_path = True

    def solver(self):
        """
        The standard Bi-Dijkstra algorithm to find the shortest path.
        """
        while self.q and self.q_r:
            node = heapq.heappop(self.q)
            cost, node_id = node
            if not self.proc.get(node_id, False):
                self.process(
                    self.q, node_id, self.adj[node_id], self.cost[node_id], self.dist, self.prev)
                self.proc[node_id] = True
            if self.proc_r.get(node_id, False):
                self.shortest_distance(node_id)
                return
            node_r = heapq.heappop(self.q_r)
            cost, node_r_id = node_r
            if not self.proc_r.get(node_r_id, False):
                self.process(
                    self.q_r, node_r_id, self.adj_r[node_r_id], self.cost_r[node_r_id], self.dist_r, self.prev_r
                )
                self.proc_r[node_r_id] = True
            if self.proc.get(node_r_id, False):
                self.shortest_distance(node_r_id)
                return

    def solver_vis(self):
        """
        Modification of the bi-dijkstra algorithm that finds the shortest path from s to t
        by moving from s forwards and from t backwards. Here there is no while loop but rather
        a conditional since this is going to be housed in the visualiser event loop.
        """
        if self.q and self.q_r:
            node = heapq.heappop(self.q)
            cost, node_id = node
            if not self.proc.get(node_id, False):
                self.process(
                    self.q, node_id, self.adj[node_id], self.cost[node_id], self.dist, self.prev)
                self.proc[node_id] = True
            if self.proc_r.get(node_id, False):
                self.shortest_distance(node_id)
                return False
            node_r = heapq.heappop(self.q_r)
            cost, node_r_id = node_r
            if not self.proc_r.get(node_r_id, False):
                self.process(
                    self.q_r, node_r_id, self.adj_r[node_r_id], self.cost_r[node_r_id], self.dist_r, self.prev_r
                )
                self.proc_r[node_r_id] = True
            if self.proc.get(node_r_id, False):
                self.shortest_distance(node_r_id)
                return False
            return True
        else:
            return False
