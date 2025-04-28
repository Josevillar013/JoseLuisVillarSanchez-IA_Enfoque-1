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
        if u not in self.adj_list:
            self.adj_list[u] = []
        self.adj_list[u].append(v)

    def bfs(self, start):
        """
        Realiza una búsqueda en anchura (BFS) desde el nodo `start`.
        Retorna una lista con el orden de visita de los nodos.
        """
        visited = set()
        queue = deque()
        order = []

        # Inicialización
        visited.add(start)
        queue.append(start)

        while queue:
            vertex = queue.popleft()
            order.append(vertex)

            # Explorar vecinos
            for neighbor in self.adj_list.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

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
    recorrido = g.bfs(start_node)
    print(f"Orden de visita en BFS desde '{start_node}': {recorrido}")

