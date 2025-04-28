from collections import deque

class Graph:
    """
    Representa un grafo utilizando una lista de adyacencia.
    """
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, u, v):
        """
        Agrega una arista dirigida de u a v en el grafo.
        Para un grafo no dirigido, llame a add_edge(v, u) también.
        """
        self.adj_list.setdefault(u, []).append(v)

    def bfs(self, start):
        """
        Realiza una búsqueda en anchura (BFS) desde el nodo `start`.
        Retorna una lista con el orden de visita de los nodos.
        """
        visited = {start}
        queue = deque([start])
        order = []

        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbor in self.adj_list.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start):
        """
        Realiza una búsqueda en profundidad (DFS) desde el nodo `start` de forma recursiva.
        Retorna una lista con el orden de visita de los nodos.
        """
        visited = set()
        order = []
        self._dfs_recursive(start, visited, order)
        return order

    def _dfs_recursive(self, u, visited, order):
        visited.add(u)
        order.append(u)
        for neighbor in self.adj_list.get(u, []):
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, order)

if __name__ == "__main__":
    # Ejemplo de uso
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'G')

    start_node = 'A'
    recorrido_bfs = g.bfs(start_node)
    recorrido_dfs = g.dfs(start_node)

    print(f"Orden de visita en BFS desde '{start_node}': {recorrido_bfs}")
    print(f"Orden de visita en DFS desde '{start_node}': {recorrido_dfs}")
