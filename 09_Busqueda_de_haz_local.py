from collections import deque

class Graph:
    """
    Representa un grafo ponderado mediante lista de adyacencia.
    Cada arista tiene un costo asociado.
    """
    def __init__(self):
        self.adj_list = {}  # { nodo: [(vecino, costo), ...] }

    def add_edge(self, u, v, cost=1):
        """
        Agrega una arista dirigida de u a v con coste `cost`.
        Para grafos no dirigidos, llamar también a add_edge(v, u, cost).
        """
        self.adj_list.setdefault(u, []).append((v, cost))

    def path_cost(self, path):
        """
        Calcula el coste total de un camino dado.
        """
        total = 0
        for u, v in zip(path, path[1:]):
            for nbr, w in self.adj_list.get(u, []):
                if nbr == v:
                    total += w
                    break
        return total


def local_beam_search_graph(graph, start, goal, beam_width, max_iterations=100):
    """
    Búsqueda por Haz Local en grafos para encontrar un camino de bajo coste.

    Parámetros:
    - graph: instancia de Graph.
    - start: nodo inicial.
    - goal: nodo meta.
    - beam_width: ancho del haz (número de caminos a mantener).
    - max_iterations: iteraciones máximas.

    Retorna:
    - best_path: mejor camino encontrado (list de nodos) o None.
    - best_cost: coste del mejor camino o None.
    """
    # Inicializar haz con el camino inicial
    beam = [[start]]
    best_path = None
    best_cost = float('inf')

    for _ in range(max_iterations):
        candidates = []  # [(coste, camino), ...]

        # Expandir cada camino en el haz
        for path in beam:
            last = path[-1]
            for neighbor, cost in graph.adj_list.get(last, []):
                if neighbor not in path:  # evita ciclos
                    new_path = path + [neighbor]
                    c = graph.path_cost(new_path)
                    candidates.append((c, new_path))

        if not candidates:
            break

        # Seleccionar los top beam_width caminos de menor coste
        candidates.sort(key=lambda x: x[0])
        beam = [path for cost, path in candidates[:beam_width]]

        # Actualizar mejor global si llegan al goal
        for cost, path in candidates:
            if path[-1] == goal and cost < best_cost:
                best_cost = cost
                best_path = path

    return best_path, best_cost if best_path is not None else (None, None)

if __name__ == "__main__":
    # Ejemplo de uso
    g = Graph()
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 5)
    g.add_edge('B', 'D', 4)
    g.add_edge('B', 'E', 1)
    g.add_edge('C', 'F', 2)
    g.add_edge('D', 'G', 2)
    g.add_edge('E', 'G', 5)
    g.add_edge('F', 'G', 1)

    start_node = 'A'
    goal_node = 'G'
    beam_width = 2

    best_path, best_cost = local_beam_search_graph(
        g, start_node, goal_node, beam_width, max_iterations=50
    )

    if best_path:
        print(f"Mejor camino encontrado: {best_path} con coste: {best_cost}")
    else:
        print("No se encontró un camino al objetivo.")
