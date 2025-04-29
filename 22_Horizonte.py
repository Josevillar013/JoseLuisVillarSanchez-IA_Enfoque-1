class Graph:
    """
    Representa un grafo mediante lista de adyacencia.
    """
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        self.adj.setdefault(u, []).append(v)

    def neighbors(self, u):
        return self.adj.get(u, [])

# Resultado especial para Depth-Limited Search
CUTOFF = 'CUTOFF'
FAILURE = None


def depth_limited_search(graph, start, goal, limit):
    """
    Búsqueda con profundidad limitada (Depth-Limited Search).
    - graph: instancia de Graph.
    - start: nodo inicial.
    - goal: nodo objetivo.
    - limit: horizonte máximo (profundidad).
    Retorna camino de start a goal, o CUTOFF si se cortó, o FAILURE si falló.
    """
    def recursive_dls(node, goal, limit, path):
        if node == goal:
            return path
        if limit == 0:
            return CUTOFF
        cutoff_occurred = False
        for child in graph.neighbors(node):
            if child not in path:
                result = recursive_dls(child, goal, limit - 1, path + [child])
                if result == CUTOFF:
                    cutoff_occurred = True
                elif result is not FAILURE:
                    return result
        return CUTOFF if cutoff_occurred else FAILURE

    return recursive_dls(start, goal, limit, [start])


def iterative_deepening_search(graph, start, goal, max_horizon):
    """
    Búsqueda en profundidad de iteración profunda (IDDFS) usando horizonte creciente.
    - max_horizon: profundidad máxima a explorar.
    Retorna el primer camino encontrado o FAILURE.
    """
    for limit in range(max_horizon + 1):
        result = depth_limited_search(graph, start, goal, limit)
        if result is not CUTOFF:
            return result
    return FAILURE

if __name__ == "__main__":
    # Ejemplo de grafo
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('C', 'E')
    g.add_edge('D', 'F')
    g.add_edge('E', 'G')

    start, goal = 'A', 'G'
    horizon = 3
    print(f"Depth-Limited Search con horizonte={horizon}:")
    path = depth_limited_search(g, start, goal, horizon)
    print(path)

    print("\nIterative Deepening hasta horizonte=5:")
    path_iddfs = iterative_deepening_search(g, start, goal, 5)
    print(path_iddfs)
