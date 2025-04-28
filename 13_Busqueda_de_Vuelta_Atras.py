class Graph:
    """
    Representa un grafo usando lista de adyacencia.
    """
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, u, v):
        """Agrega arista dirigida de u a v."""
        self.adj_list.setdefault(u, []).append(v)

    def get_neighbors(self, u):
        return self.adj_list.get(u, [])


def backtracking_search(graph, current, goal, visited=None, path=None):
    """
    Realiza búsqueda con retroceso (backtracking) para hallar un camino de current a goal.
    - graph: instancia de Graph.
    - current: nodo actual.
    - goal: nodo objetivo.
    - visited: conjunto de nodos ya visitados.
    - path: lista del camino recorrido hasta ahora.
    Retorna lista con un camino válido o None si no existe.
    """
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(current)
    path.append(current)

    # Caso base: hemos llegado
    if current == goal:
        return list(path)

    # Explorar vecinos
    for neighbor in graph.get_neighbors(current):
        if neighbor not in visited:
            result = backtracking_search(graph, neighbor, goal, visited, path)
            if result is not None:
                return result

    # Backtrack: retirar el nodo actual
    path.pop()
    visited.remove(current)
    return None


def find_all_paths(graph, current, goal, visited=None, path=None, all_paths=None):
    """
    Encuentra todas las rutas posibles de current a goal usando backtracking.
    Retorna lista de caminos (cada camino es lista de nodos).
    """
    if visited is None:
        visited = set()
    if path is None:
        path = []
    if all_paths is None:
        all_paths = []

    visited.add(current)
    path.append(current)

    if current == goal:
        all_paths.append(list(path))
    else:
        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited:
                find_all_paths(graph, neighbor, goal, visited, path, all_paths)

    # Retroceder
    path.pop()
    visited.remove(current)
    return all_paths


if __name__ == "__main__":
    # Construir grafo de ejemplo
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'G')
    g.add_edge('D', 'G')
    g.add_edge('F', 'G')

    start, goal = 'A', 'G'

    # Búsqueda de un camino
    path = backtracking_search(g, start, goal)
    if path:
        print(f"Camino encontrado (backtracking): {path}")
    else:
        print("No existe camino.")

    # Encontrar todas las rutas
    paths = find_all_paths(g, start, goal)
    print(f"Todas las rutas de {start} a {goal}:")
    for p in paths:
        print(f"  {p}")
