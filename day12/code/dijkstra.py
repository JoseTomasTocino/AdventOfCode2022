import logging
from queue import PriorityQueue

logger = logging.getLogger(__name__)

# Graph and Dijkstra's algorithm adapted from geeksforgeeks.org
class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight

    def dijkstra(self, start_vertex):
        D = {v: float('inf') for v in range(self.v)}
        D[start_vertex] = 0

        pq = PriorityQueue()
        pq.put((0, start_vertex))

        while not pq.empty():
            (dist, current_vertex) = pq.get()

            self.visited.append(current_vertex)

            for neighbor in range(self.v):

                # Skip neighbor if it's not connected to the current vertex
                if self.edges[current_vertex][neighbor] == -1:
                    continue  # If there's an edge between the current vertex and the neighbor

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
