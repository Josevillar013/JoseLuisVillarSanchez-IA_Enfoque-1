import math
import random

class Graph:
    """
    Representa un grafo ponderado mediante lista de adyacencia.
    Cada arista tiene un peso asociado.
    """
    def __init__(self):
        self.adj_list = {}  # { nodo: [(vecino, peso), ...] }

    def add_edge(self, u, v, weight=1):
        """
        Agrega una arista dirigida de u a v con costo `weight`.
        Para grafos no dirigidos, llamar también a add_edge(v, u, weight).
        """
        self.adj_list.setdefault(u, []).append((v, weight))

    def random_path(self, start, goal):
        """
        Genera un camino aleatorio de start a goal mediante random walk.
        """
        path = [start]
        current = start
        visited = {start}
        while current != goal:
            neighbors = [v for v, _ in self.adj_list.get(current, []) if v not in visited]
            if not neighbors:
                # Sin salida, reiniciar
                path = [start]
                current = start
                visited = {start}
                continue
            next_node = random.choice(neighbors)
            path.append(next_node)
            visited.add(next_node)
            current = next_node
        return path

    def path_cost(self, path):
        """
        Calcula el coste total de un camino dado.
        """
        cost = 0
        for u, v in zip(path, path[1:]):
            for nbr, w in self.adj_list.get(u, []):
                if nbr == v:
                    cost += w
                    break
        return cost


def simulated_annealing_graph(graph, start, goal,
                               initial_temp=100.0,
                               cooling_rate=0.95,
                               max_iterations=1000):
    """
    Búsqueda de Temple Simulado en un grafo para aproximar un camino de mínimo coste.
    - graph: instacia de Graph.
    - start, goal: nodos de inicio y fin.
    - initial_temp: temperatura inicial.
    - cooling_rate: tasa de enfriamiento (0 < rate < 1).
    - max_iterations: número máximo de iteraciones.
    Devuelve (mejor_camino, coste).
    """
    # Estado inicial: camino aleatorio
    current_path = graph.random_path(start, goal)
    current_cost = graph.path_cost(current_path)
    best_path = list(current_path)
    best_cost = current_cost
    temp = initial_temp

    for i in range(max_iterations):
        if temp <= 1e-3:
            break
        # Genera vecino: permuta dos nodos intermedios
        path = list(current_path)
        if len(path) > 2:
            i1 = random.randint(1, len(path)-2)
            i2 = random.randint(1, len(path)-2)
            path[i1], path[i2] = path[i2], path[i1]
        new_cost = graph.path_cost(path)

        delta = new_cost - current_cost
        # Aceptación
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_path = path
            current_cost = new_cost
            if new_cost < best_cost:
                best_path = list(path)
                best_cost = new_cost
        # Enfriar
        temp *= cooling_rate

    return best_path, best_cost

if __name__ == "__main__":
    # Ejemplo de uso
    g = Graph()
    # Definir grafo ponderado
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
    best_path, best_cost = simulated_annealing_graph(
        g, start_node, goal_node,
        initial_temp=50.0,
        cooling_rate=0.9,
        max_iterations=500
    )
    print(f"Mejor camino aproximado: {best_path} con coste {best_cost}")
