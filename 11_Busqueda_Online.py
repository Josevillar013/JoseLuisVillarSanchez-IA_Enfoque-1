import random  # Importa el módulo random para operaciones relacionadas con la aleatoriedad.

class Graph:
    """
    Grafo ponderado representado con una lista de adyacencia.
    """
    def __init__(self):
        # Inicializa el grafo como un diccionario vacío donde las claves son los nodos
        # y los valores son listas de tuplas (vecino, coste), que representan las aristas.
        self.adj_list = {}  # { nodo: [(vecino, costo), ...] }

    def add_edge(self, u, v, cost=1):
        """
        Agrega una arista dirigida desde el nodo `u` al nodo `v` con un coste `cost`.
        """
        # Si el nodo `u` no existe en el grafo, se crea una entrada para él.
        # Luego, se agrega la tupla (v, cost) a la lista de adyacencia de `u`.
        self.adj_list.setdefault(u, []).append((v, cost))

    def get_neighbors(self, u):
        """
        Devuelve la lista de vecinos (nodo, coste) de un nodo `u`.
        """
        # Obtiene los vecinos de `u` desde la lista de adyacencia. Si `u` no tiene vecinos, retorna una lista vacía.
        return self.adj_list.get(u, [])


def lrta_star(graph, start, goal, heuristic, max_steps=1000):
    """
    Algoritmo LRTA* (Learning Real-Time A*) para búsqueda en línea.

    Parámetros:
    - graph: instancia de la clase Graph, que representa el grafo.
    - start: nodo de inicio.
    - goal: nodo objetivo.
    - heuristic: diccionario con las estimaciones de la heurística h(n) para cada nodo.
    - max_steps: número máximo de pasos a ejecutar para evitar bucles infinitos.

    Retorna:
    - path: lista de nodos que representa el camino recorrido.
    """
    # Copia del diccionario de heurísticas para modificarlo sin afectar el original.
    H = dict(heuristic)
    # Inicializa el camino con el nodo de inicio.
    path = [start]
    # Inicializa el nodo actual como el nodo de inicio.
    current = start

    # Bucle principal, ejecuta el algoritmo hasta alcanzar el nodo objetivo o superar los pasos máximos.
    for step in range(max_steps):
        # Si hemos llegado al nodo objetivo, terminamos la búsqueda.
        if current == goal:
            break

        # Obtener los vecinos (sucesores) del nodo actual.
        neighbors = graph.get_neighbors(current)
        # Si no hay vecinos, significa que no se puede continuar, por lo que se termina la búsqueda.
        if not neighbors:
            print(f"No hay sucesores desde {current}, detenido.")
            break

        # Diccionario para almacenar los valores f = coste + heurística de los sucesores.
        f_values = {}
        for s2, cost in neighbors:
            # Calcula el valor f para cada vecino: coste del nodo + la heurística estimada.
            f_values[s2] = cost + H.get(s2, float('inf'))

        # Actualiza la heurística del nodo actual con el mínimo valor f encontrado en sus sucesores.
        min_f = min(f_values.values())
        H[current] = min_f

        # Elige el sucesor con el menor valor f (coste + heurística) para avanzar en el camino.
        next_state = min(f_values, key=lambda s: f_values[s])

        # Añade el sucesor elegido al camino y actualiza el nodo actual.
        path.append(next_state)
        current = next_state

    # Devuelve el camino recorrido, que es una lista de nodos.
    return path

if __name__ == "__main__":
    # Definir un grafo de ejemplo.
    g = Graph()
    # Añadir las aristas con sus respectivos costos.
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'D', 2)
    g.add_edge('B', 'E', 5)
    g.add_edge('C', 'F', 1)
    g.add_edge('D', 'G', 2)
    g.add_edge('E', 'G', 2)
    g.add_edge('F', 'G', 3)

    # Definir la heurística inicial (admisible), donde cada nodo tiene una estimación h(n).
    heuristic = {
        'A': 5,  # Heurística para el nodo A.
        'B': 4,  # Heurística para el nodo B.
        'C': 3,  # Heurística para el nodo C.
        'D': 2,  # Heurística para el nodo D.
        'E': 3,  # Heurística para el nodo E.
        'F': 2,  # Heurística para el nodo F.
        'G': 0   # Heurística para el nodo G (el nodo objetivo tiene h(n) = 0).
    }

    start, goal = 'A', 'G'  # Define el nodo de inicio y el nodo objetivo.
    # Ejecuta el algoritmo LRTA* para encontrar el camino desde `start` hasta `goal`.
    path = lrta_star(g, start, goal, heuristic)
    
    # Imprime el camino encontrado desde `start` hasta `goal`.
    print(f"Camino LRTA* desde {start} hasta {goal}: {path}")
