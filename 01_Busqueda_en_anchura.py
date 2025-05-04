from collections import deque  # Importa deque, una estructura de datos tipo cola con acceso rápido en ambos extremos

class Graph:
    """
    Representa un grafo utilizando una lista de adyacencia.
    """
    def __init__(self):
        # Inicializa el grafo con un diccionario vacío para la lista de adyacencia
        self.adj_list = {}

    def add_edge(self, u, v):
        """
        Agrega una arista dirigida de u a v en el grafo.
        Para un grafo no dirigido, llamar también a add_edge(v, u).
        """
        if u not in self.adj_list:
            # Si el nodo u no está en la lista, se agrega con una lista vacía
            self.adj_list[u] = []
        # Se agrega v a la lista de adyacencia del nodo u
        self.adj_list[u].append(v)

    def bfs(self, start):
        """
        Realiza una búsqueda en anchura (BFS) desde el nodo `start`.
        Retorna una lista con el orden de visita de los nodos.
        """
        visited = set()        # Conjunto para llevar registro de los nodos visitados
        queue = deque()        # Cola para procesar los nodos en orden BFS
        order = []             # Lista para almacenar el orden en que se visitan los nodos

        # Inicializa la BFS: marca el nodo inicial como visitado y lo agrega a la cola
        visited.add(start)
        queue.append(start)

        # Mientras haya nodos en la cola, continuar el recorrido
        while queue:
            vertex = queue.popleft()  # Saca el primer nodo de la cola
            order.append(vertex)      # Lo agrega al orden de visita

            # Explora todos los vecinos del nodo actual
            for neighbor in self.adj_list.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)    # Marca el vecino como visitado
                    queue.append(neighbor)   # Lo agrega a la cola para ser procesado

        return order  # Retorna la lista con el orden en que se visitaron los nodos

# Bloque principal para ejecutar el código si se corre directamente
if __name__ == "__main__":
    # Se crea una instancia del grafo
    g = Graph()
    # Se agregan aristas al grafo
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'G')

    start_node = 'A'  # Nodo inicial desde donde comienza la BFS
    recorrido = g.bfs(start_node)  # Se realiza la BFS desde el nodo A
    print(f"Orden de visita en BFS desde '{start_node}': {recorrido}")  # Se imprime el resultado
