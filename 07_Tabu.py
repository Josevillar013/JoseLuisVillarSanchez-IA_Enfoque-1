import random
from collections import deque
import heapq

class Graph:
    def __init__(self):
        self.edges = {}  # {nodo: [(vecino, costo), ...]}

    def add_edge(self, u, v, cost=1):
        self.edges.setdefault(u, []).append((v, cost))

def tabu_search_graph(graph, start, goal, max_iterations=100, tabu_size=5):
    """
    Búsqueda Tabú en un grafo para encontrar un camino de mínimo coste de start a goal.
    """
    current = start
    path = [start]
    cost = 0
    tabu_list = deque(maxlen=tabu_size)
    best_path = None
    best_cost = float('inf')

    for _ in range(max_iterations):
        neighbors = graph.edges.get(current, [])
        # Filtramos los vecinos que están en la lista tabú o que nos hacen ciclo en el camino
        valid_moves = [(v, c) for v, c in neighbors if v not in tabu_list and v not in path]

        if not valid_moves:
            break  # No hay más movimientos válidos

        # Elegir el vecino con el menor costo
        next_node, move_cost = min(valid_moves, key=lambda x: x[1])
        
        path.append(next_node)
        cost += move_cost
        tabu_list.append(current)  # Marcar el actual como tabú
        current = next_node

        if current == goal:
            if cost < best_cost:
                best_path = list(path)
                best_cost = cost
            break  # Hemos llegado a la meta

    return best_path, best_cost if best_path else (None, None)

# Ejemplo de uso
if __name__ == "__main__":
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
    path, total_cost = tabu_search_graph(g, start_node, goal_node, max_iterations=50, tabu_size=3)

    if path:
        print(f"Camino encontrado: {path} con costo total: {total_cost}")
    else:
        print("No se encontró un camino.")
