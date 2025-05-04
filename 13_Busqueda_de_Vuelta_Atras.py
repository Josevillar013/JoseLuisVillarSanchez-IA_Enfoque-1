class Graph:
    """
    Representa un grafo utilizando lista de adyacencia.
    """
    def __init__(self):
        """Inicializa el grafo con un diccionario vacío de lista de adyacencia."""
        self.adj_list = {}

    def add_edge(self, u, v):
        """Agrega una arista dirigida desde el nodo `u` al nodo `v`."""
        # Usamos `setdefault` para asegurarnos de que el nodo `u` tiene una lista de vecinos,
        # si no existe, se inicializa con una lista vacía.
        self.adj_list.setdefault(u, []).append(v)

    def get_neighbors(self, u):
        """Devuelve la lista de vecinos del nodo `u`."""
        # Retorna los vecinos de `u` o una lista vacía si `u` no tiene vecinos registrados.
        return self.adj_list.get(u, [])


def backtracking_search(graph, current, goal, visited=None, path=None):
    """
    Realiza búsqueda con retroceso (backtracking) para hallar un camino desde `current` a `goal`.
    - graph: instancia de la clase `Graph`.
    - current: nodo actual (punto de inicio).
    - goal: nodo objetivo (meta).
    - visited: conjunto de nodos ya visitados (para evitar ciclos).
    - path: lista que contiene el camino recorrido hasta el momento.
    Retorna una lista con un camino válido o None si no existe un camino.
    """
    if visited is None:
        # Si `visited` no ha sido proporcionado, inicializamos un conjunto vacío para llevar registro de nodos visitados.
        visited = set()
    if path is None:
        # Si `path` no ha sido proporcionado, inicializamos una lista vacía para el camino recorrido.
        path = []

    visited.add(current)  # Marcamos el nodo actual como visitado.
    path.append(current)  # Agregamos el nodo actual al camino recorrido.

    # Caso base: Si hemos llegado al nodo objetivo (goal), retornamos el camino recorrido.
    if current == goal:
        return list(path)

    # Explorar los vecinos del nodo actual.
    for neighbor in graph.get_neighbors(current):
        # Solo exploramos los vecinos que no hemos visitado aún.
        if neighbor not in visited:
            result = backtracking_search(graph, neighbor, goal, visited, path)
            # Si encontramos un camino válido, lo retornamos.
            if result is not None:
                return result

    # Backtrack: Si no encontramos un camino, eliminamos el nodo actual del camino y de los nodos visitados.
    path.pop()  # Quitamos el nodo actual del camino.
    visited.remove(current)  # Desmarcamos el nodo actual como visitado.
    return None  # Si no encontramos un camino, retornamos None.


def find_all_paths(graph, current, goal, visited=None, path=None, all_paths=None):
    """
    Encuentra todas las rutas posibles de `current` a `goal` usando backtracking.
    Retorna una lista de caminos (cada camino es una lista de nodos).
    """
    if visited is None:
        # Si `visited` no ha sido proporcionado, inicializamos un conjunto vacío para llevar registro de nodos visitados.
        visited = set()
    if path is None:
        # Si `path` no ha sido proporcionado, inicializamos una lista vacía para el camino recorrido.
        path = []
    if all_paths is None:
        # Si `all_paths` no ha sido proporcionado, inicializamos una lista vacía para almacenar todas las rutas.
        all_paths = []

    visited.add(current)  # Marcamos el nodo actual como visitado.
    path.append(current)  # Agregamos el nodo actual al camino recorrido.

    # Caso base: Si hemos llegado al nodo objetivo (goal), agregamos el camino actual a la lista de caminos.
    if current == goal:
        all_paths.append(list(path))  # Guardamos una copia del camino.

    else:
        # Si no hemos llegado al objetivo, exploramos los vecinos del nodo actual.
        for neighbor in graph.get_neighbors(current):
            # Solo exploramos los vecinos que no hemos visitado aún.
            if neighbor not in visited:
                find_all_paths(graph, neighbor, goal, visited, path, all_paths)

    # Retroceder: Al final de la exploración de un vecino, eliminamos el nodo actual del camino y de los nodos visitados.
    path.pop()  # Quitamos el nodo actual del camino.
    visited.remove(current)  # Desmarcamos el nodo actual como visitado.

    # Retornamos la lista de todas las rutas encontradas.
    return all_paths


if __name__ == "__main__":
    # Construir un grafo de ejemplo con algunos nodos y aristas.
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'G')
    g.add_edge('D', 'G')
    g.add_edge('F', 'G')

    start, goal = 'A', 'G'  # Establecemos los nodos de inicio y objetivo.

    # Realizamos la búsqueda de un solo camino utilizando backtracking.
    path = backtracking_search(g, start, goal)
    if path:
        print(f"Camino encontrado (backtracking): {path}")
    else:
        print("No existe camino.")

    # Encontramos todas las rutas posibles de `start` a `goal`.
    paths = find_all_paths(g, start, goal)
    print(f"Todas las rutas de {start} a {goal}:")
    for p in paths:
        print(f"  {p}")
