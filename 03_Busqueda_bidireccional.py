from collections import deque  # Importa deque, una estructura eficiente tipo cola para búsquedas como BFS

class Graph:
    """
    Representa un grafo dirigido utilizando una lista de adyacencia.
    """

    def __init__(self):
        # Inicializa el diccionario donde se almacenan los nodos y sus vecinos
        self.adj_list = {}

    def add_edge(self, u, v):
        """
        Agrega una arista dirigida del nodo `u` al nodo `v`.
        Para grafos no dirigidos, se debe agregar también la arista inversa: add_edge(v, u)
        """
        # Si el nodo `u` no existe, lo crea con una lista vacía y luego agrega `v`
        self.adj_list.setdefault(u, []).append(v)

    def bfs(self, start):
        """
        Realiza una búsqueda en anchura (BFS) desde el nodo `start`.
        Retorna una lista con el orden en el que se visitan los nodos.
        """
        visited = {start}         # Conjunto de nodos visitados, inicia con el nodo inicial
        queue = deque([start])    # Cola que contiene los nodos a visitar, inicia con `start`
        order = []                # Lista donde se almacenará el orden de visita

        while queue:
            vertex = queue.popleft()     # Saca el primer nodo de la cola
            order.append(vertex)         # Agrega el nodo visitado al orden

            # Recorre todos los vecinos del nodo actual
            for neighbor in self.adj_list.get(vertex, []):
                if neighbor not in visited:       # Si aún no ha sido visitado
                    visited.add(neighbor)         # Lo marca como visitado
                    queue.append(neighbor)        # Lo agrega a la cola

        return order  # Devuelve el recorrido completo en orden BFS

    def dfs(self, start):
        """
        Realiza una búsqueda en profundidad (DFS) desde el nodo `start`, usando recursión.
        Retorna una lista con el orden en el que se visitan los nodos.
        """
        visited = set()      # Conjunto de nodos visitados
        order = []           # Lista del orden de visita
        self._dfs_recursive(start, visited, order)  # Llama a la función auxiliar recursiva
        return order

    def _dfs_recursive(self, u, visited, order):
        """
        Función auxiliar recursiva para DFS.
        Marca el nodo `u` como visitado, lo agrega al orden, y explora sus vecinos.
        """
        visited.add(u)         # Marca el nodo como visitado
        order.append(u)        # Agrega el nodo al orden de visita

        # Recorre cada vecino del nodo actual
        for neighbor in self.adj_list.get(u, []):
            if neighbor not in visited:            # Si el vecino no fue visitado
                self._dfs_recursive(neighbor, visited, order)  # Llama recursivamente

    def bidirectional_search(self, start, goal):
        """
        Realiza una búsqueda bidireccional entre los nodos `start` y `goal`.
        Retorna una lista con el camino encontrado, o None si no existe.
        """
        if start == goal:
            return [start]  # Si el nodo inicial es el mismo que el final, se devuelve directamente

        # Inicialización: conjuntos de nodos visitados desde ambos extremos
        visited_start = {start}
        visited_goal = {goal}

        # Colas desde ambos extremos
        queue_start = deque([start])
        queue_goal = deque([goal])

        # Diccionarios para reconstruir el camino desde ambos extremos
        parent_start = {start: None}
        parent_goal = {goal: None}

        meet_node = None  # Nodo donde se encuentran ambas búsquedas

        # Alternancia entre los dos extremos mientras haya nodos por visitar
        while queue_start and queue_goal:
            # Expande un paso desde el inicio
            meet_node = self._search_step(queue_start, visited_start, parent_start, visited_goal)
            if meet_node:
                break  # Se encontró un punto de encuentro

            # Expande un paso desde el final
            meet_node = self._search_step(queue_goal, visited_goal, parent_goal, visited_start)
            if meet_node:
                break  # Se encontró un punto de encuentro

        if not meet_node:
            return None  # No se encontró camino entre los dos nodos

        # Reconstrucción del camino desde el inicio hasta el nodo de encuentro
        path_start = []
        node = meet_node
        while node is not None:
            path_start.append(node)
            node = parent_start[node]
        path_start.reverse()  # Se invierte para tener el camino en orden desde el inicio

        # Reconstrucción desde el nodo de encuentro hasta el destino
        path_goal = []
        node = parent_goal[meet_node]
        while node is not None:
            path_goal.append(node)
            node = parent_goal[node]

        # Se concatenan ambos caminos (sin repetir el nodo de encuentro)
        return path_start + path_goal

    def _search_step(self, queue, visited_this, parent_this, visited_other):
        """
        Expande un paso en la búsqueda bidireccional desde un lado.
        Devuelve el nodo de encuentro si se encuentra, o None si no.
        """
        current = queue.popleft()  # Saca el nodo actual de la cola

        # Explora los vecinos del nodo actual
        for neighbor in self.adj_list.get(current, []):
            if neighbor not in visited_this:  # Si aún no ha sido visitado desde este lado
                visited_this.add(neighbor)    # Marca como visitado
                parent_this[neighbor] = current  # Registra el padre del nodo
                queue.append(neighbor)        # Agrega a la cola

                # Si el vecino ya fue visitado desde el otro lado, hay un punto de encuentro
                if neighbor in visited_other:
                    return neighbor

        return None  # No se encontró punto de encuentro en este paso

# Ejecución del código como programa principal
if __name__ == "__main__":
    # Se crea un grafo de ejemplo
    g = Graph()

    # Se agregan aristas al grafo (dirigidas)
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'G')
    g.add_edge('D', 'H')

    start_node = 'A'  # Nodo inicial de búsqueda
    goal_node = 'G'   # Nodo objetivo

    # Se realiza la búsqueda bidireccional
    camino = g.bidirectional_search(start_node, goal_node)

    # Se imprime el resultado
    if camino:
        print(f"Camino encontrado entre '{start_node}' y '{goal_node}': {camino}")
    else:
        print(f"No existe camino entre '{start_node}' y '{goal_node}'")
