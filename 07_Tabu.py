import random                       # (No se usa en este código, pero sirve para futuras extensiones)
from collections import deque       # Importa deque para manejar la lista tabú con tamaño fijo
import heapq                        # (No se usa aquí directamente, útil en otras búsquedas como A*)

class Graph:
    def __init__(self):
        self.edges = {}  # Diccionario que almacena las aristas: {nodo: [(vecino, costo), ...]}

    def add_edge(self, u, v, cost=1):
        # Agrega una arista dirigida de u a v con un costo
        self.edges.setdefault(u, []).append((v, cost))

def tabu_search_graph(graph, start, goal, max_iterations=100, tabu_size=5):
    """
    Realiza búsqueda Tabú en un grafo para encontrar un camino de costo mínimo desde `start` hasta `goal`.
    - graph: el grafo sobre el que se busca.
    - start: nodo inicial.
    - goal: nodo objetivo.
    - max_iterations: número máximo de pasos permitidos.
    - tabu_size: tamaño de la lista tabú para evitar ciclos y soluciones repetidas.
    """
    current = start              # Nodo actual comienza en el nodo inicial
    path = [start]               # Se guarda el camino actual
    cost = 0                     # Acumulador del costo del camino actual
    tabu_list = deque(maxlen=tabu_size)  # Lista tabú con capacidad fija
    best_path = None             # El mejor camino encontrado
    best_cost = float('inf')     # Costo del mejor camino (inicialmente infinito)

    for _ in range(max_iterations):
        neighbors = graph.edges.get(current, [])  # Vecinos del nodo actual

        # Filtra vecinos que no están en la lista tabú y que no repiten nodos en el camino actual
        valid_moves = [(v, c) for v, c in neighbors if v not in tabu_list and v not in path]

        if not valid_moves:
            break  # Si no hay vecinos válidos, se termina la búsqueda

        # Selecciona el vecino con menor costo
        next_node, move_cost = min(valid_moves, key=lambda x: x[1])

        path.append(next_node)        # Añade el vecino al camino actual
        cost += move_cost             # Suma su costo al total
        tabu_list.append(current)     # Marca el nodo actual como tabú
        current = next_node           # Mueve al siguiente nodo

        # Si se alcanza el objetivo
        if current == goal:
            if cost < best_cost:           # Si el nuevo costo es mejor, lo guarda como el mejor
                best_path = list(path)
                best_cost = cost
            break                          # Finaliza la búsqueda al llegar al objetivo

    # Retorna el mejor camino y su costo total, o (None, None) si no se encontró camino
    return best_path, best_cost if best_path else (None, None)

# Ejemplo de uso
if __name__ == "__main__":
    # Crea el grafo y agrega aristas con sus respectivos costos
    g = Graph()
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 5)
    g.add_edge('B', 'D', 4)
    g.add_edge('B', 'E', 1)
    g.add_edge('C', 'F', 2)
    g.add_edge('D', 'G', 2)
    g.add_edge('E', 'G', 5)
    g.add_edge('F', 'G', 1)

    start_node = 'A'          # Nodo inicial
    goal_node = 'G'           # Nodo objetivo

    # Ejecuta la búsqueda tabú desde A hasta G
    path, total_cost = tabu_search_graph(g, start_node, goal_node, max_iterations=50, tabu_size=3)

    # Imprime el resultado si se encuentra camino
    if path:
        print(f"Camino encontrado: {path} con costo total: {total_cost}")
    else:
        print("No se encontró un camino.")
