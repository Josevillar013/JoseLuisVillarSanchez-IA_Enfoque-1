import random

class Graph:
    """
    Grafo ponderado con lista de adyacencia.
    """
    def __init__(self):
        self.adj_list = {}  # { nodo: [(vecino, coste), ...] }

    def add_edge(self, u, v, cost=1):
        """Agrega arista dirigida de u a v con coste."""
        self.adj_list.setdefault(u, []).append((v, cost))

    def get_neighbors(self, u):
        """Devuelve lista de tuplas (vecino, coste)."""
        return self.adj_list.get(u, [])


def lrta_star(graph, start, goal, heuristic, max_steps=1000):
    """
    Algoritmo LRTA* (Learning Real-Time A*) para búsqueda en línea.

    - graph: instancia de Graph.
    - start, goal: nodos inicio y meta.
    - heuristic: dict con estimaciones h(n).
    - max_steps: tope de pasos para evitar bucles infinitos.

    Retorna el camino recorrido.
    """
    H = dict(heuristic)  # Copia de heurística
    path = [start]
    current = start

    for step in range(max_steps):
        if current == goal:
            break

        # Obtener sucesores y valores f = cost + H
        neighbors = graph.get_neighbors(current)
        if not neighbors:
            print(f"No hay sucesores desde {current}, detenido.")
            break

        # Calcular C(s, s') + H[s'] para cada vecino
        f_values = {}
        for s2, cost in neighbors:
            f_values[s2] = cost + H.get(s2, float('inf'))

        # Actualizar H(current)
        min_f = min(f_values.values())
        H[current] = min_f

        # Elegir s' con menor f
        next_state = min(f_values, key=lambda s: f_values[s])

        # Avanzar
        path.append(next_state)
        current = next_state

    return path

if __name__ == "__main__":
    # Definir grafo de ejemplo
    g = Graph()
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'D', 2)
    g.add_edge('B', 'E', 5)
    g.add_edge('C', 'F', 1)
    g.add_edge('D', 'G', 2)
    g.add_edge('E', 'G', 2)
    g.add_edge('F', 'G', 3)

    # Heurística inicial (admisible)
    heuristic = {
        'A': 5,
        'B': 4,
        'C': 3,
        'D': 2,
        'E': 3,
        'F': 2,
        'G': 0
    }

    start, goal = 'A', 'G'
    path = lrta_star(g, start, goal, heuristic)
    print(f"Camino LRTA* desde {start} hasta {goal}: {path}")
