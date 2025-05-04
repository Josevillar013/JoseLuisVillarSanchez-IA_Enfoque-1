import random  # Importa el módulo random para generar números aleatorios.

class Graph:
    """
    Grafo ponderado representado con lista de adyacencia.
    Cada arista tiene un coste.
    """
    def __init__(self):
        # Inicializa el grafo como un diccionario vacío. Las claves son los nodos
        # y los valores son listas de tuplas (vecino, coste).
        self.adj_list = {}  # { nodo: [(vecino, costo), ...] }

    def add_edge(self, u, v, cost=1):
        """
        Agrega una arista dirigida de `u` a `v` con coste `cost`.
        Para grafos no dirigidos, llamar también a `add_edge(v, u, cost)`.
        """
        # Agrega una arista dirigida de `u` hacia `v` con un coste asociado.
        # Si el nodo `u` no existe en el grafo, se inicializa como una lista vacía.
        self.adj_list.setdefault(u, []).append((v, cost))

    def random_path(self, start, goal):
        """
        Genera un camino aleatorio de `start` a `goal` mediante random walk sin ciclos.
        """
        path = [start]  # El camino comienza con el nodo de inicio.
        visited = {start}  # El conjunto de nodos visitados para evitar ciclos.
        current = start  # Nodo actual de inicio.
        
        # Repite hasta llegar al nodo objetivo.
        while current != goal:
            # Encuentra los vecinos que no han sido visitados.
            nbrs = [v for v, _ in self.adj_list.get(current, []) if v not in visited]
            if not nbrs:
                # Si no hay vecinos no visitados, reinicia el camino.
                path = [start]
                visited = {start}
                current = start
                continue
            # Selecciona un vecino aleatorio entre los no visitados.
            next_node = random.choice(nbrs)
            path.append(next_node)  # Añade el nodo al camino.
            visited.add(next_node)  # Marca el nodo como visitado.
            current = next_node  # Actualiza el nodo actual.
        
        return path  # Retorna el camino encontrado.

    def path_cost(self, path):
        """
        Calcula el coste total de un camino.
        """
        total = 0  # Inicializa el coste total a cero.
        # Recorre los pares de nodos consecutivos en el camino.
        for u, v in zip(path, path[1:]):
            # Recorre los vecinos de `u` y encuentra el coste de la arista que va a `v`.
            for nbr, w in self.adj_list.get(u, []):
                if nbr == v:
                    total += w  # Añade el coste de la arista al total.
                    break
        return total  # Devuelve el coste total del camino.

# Operadores genéticos adaptados a caminos en grafos

def generate_initial_population(graph, start, goal, pop_size):
    """
    Genera una población inicial de caminos aleatorios desde start hasta goal.
    """
    return [graph.random_path(start, goal) for _ in range(pop_size)]  # Genera `pop_size` caminos aleatorios.

def fitness(path, graph):
    """Calcula la fitness del camino. Es inversamente proporcional al coste."""
    cost = graph.path_cost(path)  # Calcula el coste del camino.
    return 1.0 / (1 + cost)  # La fitness es inversamente proporcional al coste.

def tournament_selection(pop, fits, k=3):
    """
    Selección por torneo: selecciona el mejor camino entre `k` candidatos aleatorios.
    """
    selected = []  # Lista de caminos seleccionados para la siguiente generación.
    
    # Realiza la selección para cada individuo en la población.
    for _ in range(len(pop)):
        # Selecciona aleatoriamente `k` caminos y sus fitness correspondientes.
        aspirants = random.sample(list(zip(pop, fits)), k)
        # Elige el camino con la mejor fitness.
        winner = max(aspirants, key=lambda x: x[1])[0]
        selected.append(winner)  # Añade el camino ganador a la lista de seleccionados.
    
    return selected  # Devuelve la lista de caminos seleccionados.

def crossover(p1, p2):
    """Operación de crossover basada en un nodo común entre dos caminos."""
    # Convierte los caminos en conjuntos de nodos (excluyendo los nodos de inicio y fin).
    nodes1 = set(p1[1:-1])
    nodes2 = set(p2[1:-1])
    common = list(nodes1 & nodes2)  # Encuentra los nodos comunes entre los dos caminos.
    
    if not common:
        # Si no hay nodos comunes, realiza un crossover simple sin intercambiar partes.
        return p1[:], p2[:]
    
    # Selecciona aleatoriamente un nodo común para hacer el punto de crossover.
    cp = random.choice(common)
    i1, i2 = p1.index(cp), p2.index(cp)
    
    # Realiza el crossover creando dos nuevos caminos.
    c1 = p1[:i1] + p2[i2:]  # Camino 1: partes de `p1` antes del nodo común + parte de `p2` después del nodo común.
    c2 = p2[:i2] + p1[i1:]  # Camino 2: partes de `p2` antes del nodo común + parte de `p1` después del nodo común.
    
    return c1, c2  # Devuelve los dos caminos generados.

def mutate(path, graph, mutation_rate):
    """Mutación modificando un sufijo del camino a partir de un nodo aleatorio."""
    # Si la tasa de mutación se cumple y el camino tiene más de 2 nodos.
    if random.random() < mutation_rate and len(path) > 2:
        # Selecciona un índice aleatorio dentro del camino para modificar el sufijo.
        idx = random.randint(1, len(path) - 2)
        # Genera un nuevo camino aleatorio desde el nodo seleccionado hasta el nodo final.
        suffix = graph.random_path(path[idx], path[-1])[1:]
        # Combina la parte inicial del camino con el nuevo sufijo generado.
        path = path[:idx] + suffix
    
    return path  # Devuelve el camino mutado.

def genetic_algorithm_graph(graph, start, goal,
                             pop_size=20, generations=100,
                             crossover_rate=0.8, mutation_rate=0.1):
    """
    Algoritmo Genético para encontrar un camino de bajo coste en un grafo.
    """
    # Inicializa la población generando caminos aleatorios.
    population = generate_initial_population(graph, start, goal, pop_size)

    best_path = None  # Inicializa la mejor solución encontrada.
    best_cost = float('inf')  # Inicializa el mejor coste como infinito.

    # Ejecuta el algoritmo durante un número de generaciones.
    for gen in range(generations):
        # Calcula la fitness de cada camino en la población.
        fits = [fitness(p, graph) for p in population]

        # Actualiza la mejor solución global si se encuentra un mejor camino.
        for p, f in zip(population, fits):
            c = graph.path_cost(p)  # Calcula el coste del camino `p`.
            if c < best_cost:  # Si el coste es menor que el mejor coste encontrado.
                best_cost = c  # Actualiza el mejor coste.
                best_path = p[:]  # Actualiza el mejor camino.

        # Selección de los mejores caminos mediante torneo.
        selected = tournament_selection(population, fits)

        # Genera la siguiente generación mediante reproducción.
        next_pop = []
        while len(next_pop) < pop_size:
            p1, p2 = random.sample(selected, 2)  # Selecciona dos padres aleatorios.
            if random.random() < crossover_rate:
                c1, c2 = crossover(p1, p2)  # Realiza crossover con probabilidad `crossover_rate`.
            else:
                c1, c2 = p1[:], p2[:]  # Si no, simplemente copian a los padres.
            next_pop.extend([c1, c2])  # Añade los hijos a la población.

        # Actualiza la población con los nuevos caminos generados.
        population = next_pop[:pop_size]

        # Aplica la mutación a la población.
        population = [mutate(p, graph, mutation_rate) for p in population]

    return best_path, best_cost  # Devuelve el mejor camino encontrado y su coste.

if __name__ == "__main__":
    # Ejemplo en grafo
    g = Graph()  # Crea una instancia de un grafo vacío.
    
    # Añade las aristas al grafo con los respectivos costos.
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 5)
    g.add_edge('B', 'D', 4)
    g.add_edge('B', 'E', 1)
    g.add_edge('C', 'F', 2)
    g.add_edge('D', 'G', 2)
    g.add_edge('E', 'G', 5)
    g.add_edge('F', 'G', 1)

    start, goal = 'A', 'G'  # Define el nodo de inicio y el nodo objetivo.
    
    # Ejecuta el algoritmo genético para encontrar el mejor camino.
    path, cost = genetic_algorithm_graph(
        g, start, goal,
        pop_size=30, generations=50,
        crossover_rate=0.7, mutation_rate=0.05
    )
    
    # Imprime el mejor camino encontrado y su coste.
    if path:
        print(f"Mejor camino: {path} con coste: {cost}")
    else:
        print("No se encontró solución.")
