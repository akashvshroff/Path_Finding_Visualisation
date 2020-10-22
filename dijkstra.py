import heapq


class DijkstraAlgorithm:
    def __init__(self, adj, cost, s, t):
        """
        Initialises all the data structures needed for the Djikstra algorithm.
        """
        self.adj = adj
        self.cost = cost
        self.s = s
        self.t = t
        self.dist = {}  # distances to each node
        self.dist[self.s] = 0
        self.proc = {}  # processed nodes
        self.prev = {}  # previous node to reconstruct path
        self.q = [(0, self.s)]  # queue for order of processing nodes
        self.path = []  # shortest path
        self.distance = None
        self.found_path = False
        heapq.heapify(self.q)

    def solver_vis(self):
        """
        Modification the Dijkstra's algorithm to allow for visualisation with pygame.
        Swaps the while self.q conditional for an if self.q since the entire function
        is stored within the event loop.
        """
        if self.q and not self.path:
            u = heapq.heappop(self.q)
            cost, node = u
            if not self.proc.get(node, False):
                self.proc[node] = True
                for id, vertex in enumerate(self.adj[node]):
                    # relax all outgoing edges
                    if self.dist.get(vertex, float('inf')) > cost + self.cost[node][id]:
                        self.dist[vertex] = cost + self.cost[node][id]
                        self.prev[vertex] = node
                        heapq.heappush(self.q, (self.dist[vertex], vertex))
            if node != self.t:
                return True
            else:
                self.found_path = True
                self.reconstruct_path()
                return False
        else:
            if self.proc.get(self.t, False):
                self.found_path = True
                self.reconstruct_path()
            return False

    def solver(self):
        """
        Implementation of Dijkstra's algorithm without any modification to allow vis.
        """
        while self.q:
            u = heapq.heappop(self.q)
            cost, node = u
            if not self.proc.get(node, False):
                self.proc[node] = True
                for id, vertex in enumerate(self.adj[node]):
                    # relax all outgoing edges
                    if self.dist.get(vertex, float('inf')) > cost + self.cost[node][id]:
                        self.dist[vertex] = cost + self.cost[node][id]
                        self.prev[vertex] = node
                        heapq.heappush(self.q, (self.dist[vertex], vertex))
            if node == self.t:
                break
        if self.proc.get(self.t, False):
            self.found_path = True
            self.reconstruct_path()

    def reconstruct_path(self):
        """
        Reconstructs the shortest path from start vertex to end vertex.
        """
        self.distance = self.dist[self.t]
        self.path.append(self.t)
        while self.path[-1] != self.s:
            self.path.append(self.prev[self.path[-1]])
        self.path.reverse()
