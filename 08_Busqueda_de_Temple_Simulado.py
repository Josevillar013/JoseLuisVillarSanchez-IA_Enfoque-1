import math                # Importa la biblioteca `math` para funciones matemáticas como `exp`.
import random              # Importa la biblioteca `random` para generar números aleatorios.

class Graph:
    """
    Representa un grafo ponderado mediante lista de adyacencia.
    Cada arista tiene un peso asociado.
    """
    def __init__(self):
        # Inicializa un diccionario de listas de adyacencia para almacenar el grafo.
        self.adj_list = {}  # { nodo: [(vecino, peso), ...] }

    def add_edge(self, u, v, weight=1):
        """
        Agrega una arista dirigida de u a v con costo `weight`.
        Para grafos no dirigidos, llamar también a add_edge(v, u, weight).
        """
        # Agrega un vecino `v` con su peso `weight` a la lista de adyacencia del nodo `u`.
        self.adj_list.setdefault(u, []).append((v, weight))

    def random_path(self, start, goal):
        """
        Genera un camino aleatorio de start a goal mediante random walk.
        """
        path = [start]          # El camino comienza con el nodo de inicio.
        current = start         # Establece el nodo actual como el de inicio.
        visited = {start}       # Crea un conjunto de nodos visitados para evitar ciclos.

        # Continúa el recorrido hasta llegar al nodo objetivo.
        while current != goal:
            # Obtiene los vecinos del nodo actual que no han sido visitados.
            neighbors = [v for v, _ in self.adj_list.get(current, []) if v not in visited]

            if not neighbors:
                # Si no hay vecinos no visitados, reinicia el camino.
                path = [start]
                current = start
                visited = {start}
                continue

            # Elige aleatoriamente un vecino para continuar el recorrido.
            next_node = random.choice(neighbors)
            path.append(next_node)  # Añade el vecino al camino.
            visited.add(next_node)  # Marca el vecino como visitado.
            current = next_node     # Avanza al siguiente nodo.

        return path  # Devuelve el camino completo desde start hasta goal.

    def path_cost(self, path):
        """
        Calcula el coste total de un camino dado.
        """
        cost = 0
        # Para cada par de nodos consecutivos en el camino, calcula el coste de la arista.
        for u, v in zip(path, path[1:]):
            # Busca la arista (u, v) en la lista de adyacencia de `u`.
            for nbr, w in self.adj_list.get(u, []):
                if nbr == v:  # Si el vecino es el destino `v`, añade su peso al coste.
                    cost += w
                    break
        return cost  # Retorna el coste total del camino.

def simulated_annealing_graph(graph, start, goal,
                               initial_temp=100.0,
                               cooling_rate=0.95,
                               max_iterations=1000):
    """
    Búsqueda de Temple Simulado en un grafo para aproximar un camino de mínimo coste.
    - graph: instancia de Graph.
    - start, goal: nodos de inicio y fin.
    - initial_temp: temperatura inicial.
    - cooling_rate: tasa de enfriamiento (0 < rate < 1).
    - max_iterations: número máximo de iteraciones.
    Devuelve (mejor_camino, coste).
    """
    # Genera un camino aleatorio inicial desde el nodo de inicio hasta el nodo objetivo.
    current_path = graph.random_path(start, goal)
    current_cost = graph.path_cost(current_path)  # Calcula el coste del camino inicial.
    
    best_path = list(current_path)  # Establece el camino inicial como el mejor hasta ahora.
    best_cost = current_cost       # Establece el coste inicial como el mejor coste hasta ahora.
    
    temp = initial_temp            # Establece la temperatura inicial.

    # Itera por un número máximo de veces, o hasta que la temperatura sea suficientemente baja.
    for i in range(max_iterations):
        if temp <= 1e-3:  # Si la temperatura es muy baja, termina el algoritmo.
            break

        # Genera un vecino: permuta dos nodos intermedios del camino.
        path = list(current_path)  # Copia el camino actual para modificarlo.
        if len(path) > 2:
            i1 = random.randint(1, len(path)-2)  # Selecciona aleatoriamente un índice para el primer nodo.
            i2 = random.randint(1, len(path)-2)  # Selecciona aleatoriamente otro índice para el segundo nodo.
            path[i1], path[i2] = path[i2], path[i1]  # Permuta los dos nodos seleccionados.

        new_cost = graph.path_cost(path)  # Calcula el coste del nuevo camino.

        delta = new_cost - current_cost  # Calcula la diferencia de coste entre el nuevo camino y el actual.
        
        # Si el nuevo camino tiene un coste menor, o se acepta de manera probabilística.
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_path = path  # Acepta el nuevo camino.
            current_cost = new_cost  # Actualiza el coste actual.
            
            # Si el nuevo coste es el mejor encontrado, lo guarda.
            if new_cost < best_cost:
                best_path = list(path)
                best_cost = new_cost

        # Enfría la temperatura de acuerdo con la tasa de enfriamiento.
        temp *= cooling_rate

    # Retorna el mejor camino encontrado y su coste total.
    return best_path, best_cost

if __name__ == "__main__":
    # Ejemplo de uso: Crear un grafo ponderado y aplicar Temple Simulado.
    g = Graph()
    # Definir grafo ponderado con nodos y aristas de diferentes costos.
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 5)
    g.add_edge('B', 'D', 4)
    g.add_edge('B', 'E', 1)
    g.add_edge('C', 'F', 2)
    g.add_edge('D', 'G', 2)
    g.add_edge('E', 'G', 5)
    g.add_edge('F', 'G', 1)

    start_node = 'A'  # Nodo de inicio.
    goal_node = 'G'   # Nodo de destino.

    # Ejecuta el algoritmo de Temple Simulado para encontrar un camino de coste mínimo.
    best_path, best_cost = simulated_annealing_graph(
        g, start_node, goal_node,
        initial_temp=50.0,   # Temperatura inicial.
        cooling_rate=0.9,    # Tasa de enfriamiento.
        max_iterations=500   # Número máximo de iteraciones.
    )
    # Imprime el mejor camino encontrado y su coste.
    print(f"Mejor camino aproximado: {best_path} con coste {best_cost}")
