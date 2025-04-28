import random

class Graph:
    """
    Grafo ponderado representado con lista de adyacencia.
    Cada arista tiene un coste.
    """
    def __init__(self):
        self.adj_list = {}  # { nodo: [(vecino, coste), ...] }

    def add_edge(self, u, v, cost=1):
        self.adj_list.setdefault(u, []).append((v, cost))

    def random_path(self, start, goal):
        """
        Genera un camino aleatorio de start a goal mediante random walk sin ciclos.
        """
        path = [start]
        visited = {start}
        current = start
        while current != goal:
            nbrs = [v for v, _ in self.adj_list.get(current, []) if v not in visited]
            if not nbrs:
                # reiniciar si se bloquea
                path = [start]
                visited = {start}
                current = start
                continue
            next_node = random.choice(nbrs)
            path.append(next_node)
            visited.add(next_node)
            current = next_node
        return path

    def path_cost(self, path):
        """
        Calcula el coste total de un camino.
        """
        total = 0
        for u, v in zip(path, path[1:]):
            for nbr, w in self.adj_list.get(u, []):
                if nbr == v:
                    total += w
                    break
        return total

# Operadores genéticos adaptados a caminos en grafos
def generate_initial_population(graph, start, goal, pop_size):
    return [graph.random_path(start, goal) for _ in range(pop_size)]

def fitness(path, graph):
    """Fitness inversamente proporcional al coste."""
    cost = graph.path_cost(path)
    return 1.0 / (1 + cost)

def tournament_selection(pop, fits, k=3):
    selected = []
    for _ in range(len(pop)):
        aspirants = random.sample(list(zip(pop, fits)), k)
        winner = max(aspirants, key=lambda x: x[1])[0]
        selected.append(winner)
    return selected

def crossover(p1, p2):
    """Crossover basado en un nodo común."""
    nodes1 = set(p1[1:-1])
    nodes2 = set(p2[1:-1])
    common = list(nodes1 & nodes2)
    if not common:
        return p1[:], p2[:]
    cp = random.choice(common)
    i1, i2 = p1.index(cp), p2.index(cp)
    c1 = p1[:i1] + p2[i2:]
    c2 = p2[:i2] + p1[i1:]
    return c1, c2

def mutate(path, graph, mutation_rate):
    """Mutación modificando un sufijo desde un nodo aleatorio."""
    if random.random() < mutation_rate and len(path) > 2:
        idx = random.randint(1, len(path) - 2)
        suffix = graph.random_path(path[idx], path[-1])[1:]
        path = path[:idx] + suffix
    return path


def genetic_algorithm_graph(graph, start, goal,
                             pop_size=20, generations=100,
                             crossover_rate=0.8, mutation_rate=0.1):
    # Inicialización
    population = generate_initial_population(graph, start, goal, pop_size)

    best_path = None
    best_cost = float('inf')

    for gen in range(generations):
        # Evaluar fitness
        fits = [fitness(p, graph) for p in population]

        # Actualizar mejor global
        for p, f in zip(population, fits):
            c = graph.path_cost(p)
            if c < best_cost:
                best_cost = c
                best_path = p[:]

        # Selección
        selected = tournament_selection(population, fits)

        # Reproducción
        next_pop = []
        while len(next_pop) < pop_size:
            p1, p2 = random.sample(selected, 2)
            if random.random() < crossover_rate:
                c1, c2 = crossover(p1, p2)
            else:
                c1, c2 = p1[:], p2[:]
            next_pop.extend([c1, c2])
        population = next_pop[:pop_size]

        # Mutación
        population = [mutate(p, graph, mutation_rate) for p in population]

    return best_path, best_cost

if __name__ == "__main__":
    # Ejemplo en grafo
    g = Graph()
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 5)
    g.add_edge('B', 'D', 4)
    g.add_edge('B', 'E', 1)
    g.add_edge('C', 'F', 2)
    g.add_edge('D', 'G', 2)
    g.add_edge('E', 'G', 5)
    g.add_edge('F', 'G', 1)

    start, goal = 'A', 'G'
    path, cost = genetic_algorithm_graph(
        g, start, goal,
        pop_size=30, generations=50,
        crossover_rate=0.7, mutation_rate=0.05
    )
    if path:
        print(f"Mejor camino: {path} con coste: {cost}")
    else:
        print("No se encontró solución.")
