from collections import deque  # Importa la clase deque, que se usa para gestionar colas de manera eficiente.

class Graph:
    """
    Representa un grafo ponderado mediante lista de adyacencia.
    Cada arista tiene un costo asociado.
    """
    def __init__(self):
        # Inicializa el grafo como un diccionario vacío donde las claves son los nodos
        # y los valores son listas de tuplas (vecino, costo).
        self.adj_list = {}  # { nodo: [(vecino, costo), ...] }

    def add_edge(self, u, v, cost=1):
        """
        Agrega una arista dirigida de u a v con coste `cost`.
        Para grafos no dirigidos, llamar también a add_edge(v, u, cost).
        """
        # Agrega una arista dirigida desde el nodo `u` hacia el nodo `v` con el costo `cost`.
        # Si el nodo `u` no existe en la lista de adyacencia, lo inicializa.
        self.adj_list.setdefault(u, []).append((v, cost))

    def path_cost(self, path):
        """
        Calcula el coste total de un camino dado.
        """
        total = 0  # Inicializa el coste total en 0.
        # Itera sobre cada par de nodos consecutivos en el camino.
        for u, v in zip(path, path[1:]):
            # Recorre la lista de vecinos de `u` buscando a `v`.
            for nbr, w in self.adj_list.get(u, []):
                if nbr == v:
                    total += w  # Si encuentra a `v`, agrega el costo `w` al total.
                    break
        return total  # Devuelve el coste total del camino.


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
    # Inicializa el haz con el camino inicial, que contiene solo el nodo de inicio.
    beam = [[start]]
    best_path = None  # Variable para almacenar el mejor camino encontrado.
    best_cost = float('inf')  # Inicializa el mejor coste como infinito.

    # Itera hasta el número máximo de iteraciones.
    for _ in range(max_iterations):
        candidates = []  # Lista para almacenar los caminos candidatos junto con sus costes.

        # Expande cada camino en el haz (expande todos los caminos actuales).
        for path in beam:
            last = path[-1]  # Obtiene el último nodo del camino actual.
            # Itera sobre los vecinos del nodo `last`.
            for neighbor, cost in graph.adj_list.get(last, []):
                if neighbor not in path:  # Evita ciclos (el vecino no debe estar en el camino).
                    new_path = path + [neighbor]  # Crea un nuevo camino agregando el vecino.
                    c = graph.path_cost(new_path)  # Calcula el coste del nuevo camino.
                    candidates.append((c, new_path))  # Agrega el nuevo camino y su coste a los candidatos.

        if not candidates:
            break  # Si no hay más caminos válidos, termina la búsqueda.

        # Ordena los caminos candidatos por coste de menor a mayor.
        candidates.sort(key=lambda x: x[0])
        # Mantiene solo los `beam_width` caminos más baratos.
        beam = [path for cost, path in candidates[:beam_width]]

        # Actualiza el mejor camino global si se encuentra un camino que termina en el objetivo.
        for cost, path in candidates:
            if path[-1] == goal and cost < best_cost:
                best_cost = cost  # Actualiza el mejor coste.
                best_path = path  # Actualiza el mejor camino.

    return best_path, best_cost if best_path is not None else (None, None)  # Devuelve el mejor camino encontrado.

if __name__ == "__main__":
    # Ejemplo de uso
    g = Graph()  # Crea una instancia de un grafo vacío.
    
    # Añade las aristas al grafo con sus respectivos costos.
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
    beam_width = 2    # Establece el ancho del haz, es decir, la cantidad de caminos a mantener.

    # Ejecuta la búsqueda por haz local para encontrar el mejor camino desde `start_node` hasta `goal_node`.
    best_path, best_cost = local_beam_search_graph(
        g, start_node, goal_node, beam_width, max_iterations=50
    )

    # Imprime el mejor camino y su coste si se encuentra un camino válido.
    if best_path:
        print(f"Mejor camino encontrado: {best_path} con coste: {best_cost}")
    else:
        print("No se encontró un camino al objetivo.")
