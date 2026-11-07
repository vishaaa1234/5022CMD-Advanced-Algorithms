"""
graph.py - A generic, reusable unweighted DIRECTED graph (adjacency lists).

Vertices can be any hashable value (strings, ints, ...). This file contains
no code related to courses or any other domain, so it can be reused anywhere.

Two adjacency lists are kept:
    adjacency_list : vertex -> vertices it points TO      (outgoing edges)
    incoming_list  : vertex -> vertices that point to it  (incoming edges)
Keeping both makes listing incoming edges O(degree) instead of scanning
the whole graph (O(V + E)).
"""


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.incoming_list = {}

    # ------------------------------------------------------------ vertices
    def addVertex(self, vertex):
        """Add a new vertex. Returns False if it already exists."""
        if vertex in self.adjacency_list:
            return False
        self.adjacency_list[vertex] = []
        self.incoming_list[vertex] = []
        return True

    def removeVertex(self, vertex):
        """Remove a vertex and every edge connected to it."""
        if vertex not in self.adjacency_list:
            return False
        for destination in list(self.adjacency_list[vertex]):
            self.removeEdge(vertex, destination)
        for source in list(self.incoming_list[vertex]):
            self.removeEdge(source, vertex)
        del self.adjacency_list[vertex]
        del self.incoming_list[vertex]
        return True

    def hasVertex(self, vertex):
        return vertex in self.adjacency_list

    def getVertices(self):
        return list(self.adjacency_list)

    # --------------------------------------------------------------- edges
    def addEdge(self, source, destination):
        """Add a directed edge source -> destination.
        Returns False if a vertex is missing or the edge already exists."""
        if source not in self.adjacency_list or destination not in self.adjacency_list:
            return False
        if destination in self.adjacency_list[source]:
            return False
        self.adjacency_list[source].append(destination)
        self.incoming_list[destination].append(source)
        return True

    def removeEdge(self, source, destination):
        """Remove the edge source -> destination. Returns False if absent."""
        if not self.hasEdge(source, destination):
            return False
        self.adjacency_list[source].remove(destination)
        self.incoming_list[destination].remove(source)
        return True

    def hasEdge(self, source, destination):
        return (source in self.adjacency_list
                and destination in self.adjacency_list[source])

    # ------------------------------------------------------------- queries
    def listIncomingAdjacentVertex(self, vertex):
        """All vertices that have an edge INTO `vertex`."""
        return list(self.incoming_list.get(vertex, []))

    def listOutgoingAdjacentVertex(self, vertex):
        """All vertices that `vertex` has an edge TO."""
        return list(self.adjacency_list.get(vertex, []))

    def hasPath(self, start, goal):
        """True if `goal` can be reached from `start` (iterative DFS)."""
        if start not in self.adjacency_list or goal not in self.adjacency_list:
            return False
        visited = set()
        stack = [start]
        while stack:
            current = stack.pop()
            if current == goal:
                return True
            if current in visited:
                continue
            visited.add(current)
            stack.extend(self.adjacency_list[current])
        return False
