from collections import deque  # Importa deque, una estructura eficiente de cola para usar en BFS

class Graph:
    """
    Representa un grafo utilizando una lista de adyacencia.
    Cada nodo tiene una lista de nodos adyacentes (vecinos).
    """
    def __init__(self):
        # Inicializa el grafo como un diccionario vacío
        self.adj_list = {}

    def add_edge(self, u, v):
        """
        Agrega una arista dirigida de u a v en el grafo.
        Para un grafo no dirigido, también se debe llamar a add_edge(v, u).
        """
        # Si el nodo u no está en la lista, se crea una lista vacía y se agrega v a la lista
        self.adj_list.setdefault(u, []).append(v)

    def bfs(self, start):
        """
        Realiza una búsqueda en anchura (BFS) desde el nodo `start`.
        Retorna una lista con el orden en que se visitan los nodos.
        """
        visited = {start}          # Conjunto de nodos ya visitados; inicia con el nodo inicial
        queue = deque([start])     # Cola de nodos por visitar, inicia con el nodo inicial
        order = []                 # Lista que guarda el orden de visita de los nodos

        # Mientras haya nodos por visitar en la cola
        while queue:
            vertex = queue.popleft()     # Se extrae el nodo de la cabeza de la cola
            order.append(vertex)         # Se guarda el nodo visitado en el orden de recorrido

            # Itera sobre los vecinos del nodo actual
            for neighbor in self.adj_list.get(vertex, []):
                if neighbor not in visited:      # Si el vecino aún no ha sido visitado
                    visited.add(neighbor)       # Se marca como visitado
                    queue.append(neighbor)      # Se agrega a la cola para procesarlo luego

        return order  # Devuelve el recorrido en orden BFS

    def dfs(self, start):
        """
        Realiza una búsqueda en profundidad (DFS) desde el nodo `start` usando recursión.
        Retorna una lista con el orden en que se visitan los nodos.
        """
        visited = set()   # Conjunto para llevar registro de nodos visitados
        order = []        # Lista para registrar el orden de visita
        self._dfs_recursive(start, visited, order)  # Llama a la función recursiva auxiliar
        return order

    def _dfs_recursive(self, u, visited, order):
        """
        Función auxiliar recursiva para DFS.
        Visita el nodo `u`, marca como visitado, y recorre sus vecinos recursivamente.
        """
        visited.add(u)       # Marca el nodo actual como visitado
        order.append(u)      # Agrega el nodo actual al orden de visita

        # Recorre los vecinos del nodo actual
        for neighbor in self.adj_list.get(u, []):
            if neighbor not in visited:            # Si el vecino no ha sido visitado
                self._dfs_recursive(neighbor, visited, order)  # Llama recursivamente

# Bloque principal: se ejecuta si el script es el programa principal
if __name__ == "__main__":
    # Se crea una instancia del grafo
    g = Graph()

    # Se agregan aristas al grafo (dirigidas)
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'G')

    start_node = 'A'  # Nodo inicial desde el que se realizarán los recorridos

    # Ejecuta BFS desde el nodo A
    recorrido_bfs = g.bfs(start_node)

    # Ejecuta DFS desde el nodo A
    recorrido_dfs = g.dfs(start_node)

    # Imprime el orden de visita en cada recorrido
    print(f"Orden de visita en BFS desde '{start_node}': {recorrido_bfs}")
    print(f"Orden de visita en DFS desde '{start_node}': {recorrido_dfs}")
