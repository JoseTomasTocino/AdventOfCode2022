from collections import defaultdict
import logging
from queue import PriorityQueue

logger = logging.getLogger(__name__)

# Graph and Dijkstra's algorithm adapted from geeksforgeeks.org
class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = defaultdict(lambda: defaultdict(lambda: -1))
        self.vertices = set()
        self.visited = []

    def add_edge(self, u, v, weight=1):
        self.vertices.add(u)
        self.vertices.add(v)

        self.edges[u][v] = weight


    def dijkstra(self, start_vertex):
        self.visited = []
        
        D = {v: float("inf") for v in self.vertices}
        D[start_vertex] = 0

        pq = PriorityQueue()
        pq.put((0, start_vertex))

        while not pq.empty():
            (dist, current_vertex) = pq.get()

            self.visited.append(current_vertex)

            for neighbor in self.vertices:

                # Skip neighbor if it's not connected to the current vertex
                if self.edges[current_vertex][neighbor] == -1:
                    continue  

                # Also skip the neighbor if already visited
                if neighbor in self.visited:
                    continue

                distance = self.edges[current_vertex][neighbor]

                old_cost = D[neighbor]
                new_cost = D[current_vertex] + distance

                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    D[neighbor] = new_cost

        return D

    def closest_nodes(self, start_vertex):
        d = self.dijkstra(start_vertex)
        d = [x[0] for x in sorted(d.items(), key=lambda x: x[1])]

        d.remove(start_vertex)

        return d

