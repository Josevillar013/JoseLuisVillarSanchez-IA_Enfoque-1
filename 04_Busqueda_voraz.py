from collections import deque  # Importa deque para usar colas eficientes (útil en BFS)
import heapq                  # Importa heapq para manejar una cola de prioridad (útil en greedy search)

class Graph:
    """
    Representa un grafo utilizando una lista de adyacencia (diccionario de listas).
    """
    def __init__(self):
        self.adj_list = {}  # Diccionario para guardar los nodos y sus vecinos

    def add_edge(self, u, v):
        """
        Agrega una arista dirigida del nodo u al nodo v.
        Para un grafo no dirigido, se debe agregar también la arista inversa con add_edge(v, u).
        """
        self.adj_list.setdefault(u, []).append(v)  # Si u no existe, se inicializa su lista y se agrega v

    def bfs(self, start):
        """
        Búsqueda en anchura (Breadth-First Search) desde el nodo `start`.
        Devuelve el orden en que se visitan los nodos.
        """
        visited = {start}             # Conjunto de nodos visitados
        queue = deque([start])        # Cola para BFS, iniciando con el nodo inicial
        order = []                    # Lista para registrar el orden de visita

        while queue:
            vertex = queue.popleft()  # Se saca el primer nodo de la cola
            order.append(vertex)      # Se registra su visita
            for neighbor in self.adj_list.get(vertex, []):  # Recorre los vecinos del nodo actual
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order  # Devuelve el recorrido BFS completo

    def dfs(self, start):
        """
        Búsqueda en profundidad (Depth-First Search) desde el nodo `start`.
        Utiliza recursión. Devuelve el orden de visita.
        """
        visited = set()    # Conjunto de nodos visitados
        order = []         # Lista del orden de visita
        self._dfs_recursive(start, visited, order)  # Llama a la función auxiliar recursiva
        return order

    def _dfs_recursive(self, u, visited, order):
        visited.add(u)      # Marca el nodo como visitado
        order.append(u)     # Registra el nodo en el orden
        for neighbor in self.adj_list.get(u, []):  # Recorre sus vecinos
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, order)  # Llama recursivamente

    def bidirectional_search(self, start, goal):
        """
        Búsqueda bidireccional entre `start` y `goal`.
        Devuelve una lista con el camino si se encuentra, o None si no existe.
        """
        if start == goal:
            return [start]  # Caso especial: origen y destino son iguales

        # Inicialización de los conjuntos y colas para ambas direcciones
        visited_start = {start}
        visited_goal = {goal}
        queue_start = deque([start])
        queue_goal = deque([goal])
        parent_start = {start: None}
        parent_goal = {goal: None}
        meet_node = None

        # Alterna entre expansiones desde ambos extremos
        while queue_start and queue_goal:
            # Paso desde el inicio
            meet_node = self._search_step(queue_start, visited_start, parent_start, visited_goal)
            if meet_node:
                break
            # Paso desde el final
            meet_node = self._search_step(queue_goal, visited_goal, parent_goal, visited_start)
            if meet_node:
                break

        if not meet_node:
            return None  # No hay conexión entre start y goal

        # Reconstrucción del camino desde start al nodo de encuentro
        path_start = []
        node = meet_node
        while node is not None:
            path_start.append(node)
            node = parent_start[node]
        path_start.reverse()  # Invierte el camino de start al punto de encuentro

        # Reconstrucción del camino desde el nodo de encuentro a goal
        path_goal = []
        node = parent_goal[meet_node]
        while node is not None:
            path_goal.append(node)
            node = parent_goal[node]

        return path_start + path_goal  # Une ambos caminos en uno solo

    def _search_step(self, queue, visited_this, parent_this, visited_other):
        """
        Realiza un paso de búsqueda desde un lado (start o goal).
        Devuelve el nodo de encuentro si se detecta intersección entre lados.
        """
        current = queue.popleft()  # Extrae el nodo actual
        for neighbor in self.adj_list.get(current, []):  # Recorre vecinos
            if neighbor not in visited_this:
                visited_this.add(neighbor)
                parent_this[neighbor] = current
                queue.append(neighbor)
                if neighbor in visited_other:  # Si el vecino ya fue visto desde el otro lado
                    return neighbor  # Se encontró el punto de encuentro
        return None

    def greedy_search(self, start, goal, heuristic):
        """
        Búsqueda voraz (Greedy Best-First Search).
        Utiliza una heurística para decidir qué nodo visitar a continuación.
        `heuristic` es un diccionario que asigna a cada nodo un valor estimado de cercanía al objetivo.
        """
        visited = {start}              # Conjunto de nodos visitados
        parent = {start: None}         # Diccionario para reconstruir el camino
        queue = [(heuristic.get(start, float('inf')), start)]  # Cola de prioridad por heurística

        while queue:
            _, current = heapq.heappop(queue)  # Extrae el nodo con menor heurística
            if current == goal:
                # Se llegó al objetivo; reconstruye el camino
                path = []
                node = current
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return path[::-1]  # Devuelve el camino en orden correcto

            for neighbor in self.adj_list.get(current, []):  # Recorre vecinos
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    heapq.heappush(queue, (heuristic.get(neighbor, float('inf')), neighbor))  # Inserta con prioridad

        return None  # Si se agotaron los nodos y no se llegó al destino

# Bloque principal
if __name__ == "__main__":
    g = Graph()  # Crea instancia del grafo

    # Agrega aristas al grafo (dirigidas)
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'G')
    g.add_edge('D', 'H')

    # Heurística estimada hacia el objetivo 'G' para cada nodo
    heuristic = {
        'A': 5,
        'B': 4,
        'C': 2,
        'D': 3,
        'E': 6,
        'F': 1,
        'G': 0,
        'H': 7
    }

    start_node = 'A'
    goal_node = 'G'

    # Ejecuta búsqueda voraz desde A hasta G
    camino_voraz = g.greedy_search(start_node, goal_node, heuristic)

    # Imprime el camino si se encuentra
    if camino_voraz:
        print(f"Camino voraz encontrado de '{start_node}' a '{goal_node}': {camino_voraz}")
    else:
        print(f"No existe camino voraz entre '{start_node}' y '{goal_node}'")
