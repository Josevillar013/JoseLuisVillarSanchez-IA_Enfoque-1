from collections import deque

class Graph:
    """
    Representa un grafo utilizando una lista de adyacencia.
    """
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, u, v):
        """
        Agrega una arista dirigida de u a v en el grafo.
        Para un grafo no dirigido, llame a add_edge(v, u) también.
        """
        self.adj_list.setdefault(u, []).append(v)

    def bfs(self, start):
        """
        Realiza una búsqueda en anchura (BFS) desde el nodo `start`.
        Retorna una lista con el orden de visita de los nodos.
        """
        visited = {start}
        queue = deque([start])
        order = []
        while queue:
            vertex = queue.popleft()
            order.append(vertex)
            for neighbor in self.adj_list.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start):
        """
        Realiza una búsqueda en profundidad (DFS) desde el nodo `start` de forma recursiva.
        Retorna una lista con el orden de visita de los nodos.
        """
        visited = set()
        order = []
        self._dfs_recursive(start, visited, order)
        return order

    def _dfs_recursive(self, u, visited, order):
        visited.add(u)
        order.append(u)
        for neighbor in self.adj_list.get(u, []):
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, order)

    def bidirectional_search(self, start, goal):
        """
        Realiza una búsqueda bidireccional entre `start` y `goal`.
        Retorna el camino encontrado o None si no existe.
        """
        if start == goal:
            return [start]

        # Fronteras y padres para ambos extremos
        visited_start = {start}
        visited_goal = {goal}
        queue_start = deque([start])
        queue_goal = deque([goal])
        parent_start = {start: None}
        parent_goal = {goal: None}

        meet_node = None
        # Alternar expansiones
        while queue_start and queue_goal:
            meet_node = self._search_step(queue_start, visited_start, parent_start, visited_goal)
            if meet_node:
                break
            meet_node = self._search_step(queue_goal, visited_goal, parent_goal, visited_start)
            if meet_node:
                break

        if not meet_node:
            return None

        # Reconstruir camino
        path_start = []
        node = meet_node
        while node is not None:
            path_start.append(node)
            node = parent_start[node]
        path_start.reverse()

        path_goal = []
        node = parent_goal[meet_node]
        while node is not None:
            path_goal.append(node)
            node = parent_goal[node]

        return path_start + path_goal

    def _search_step(self, queue, visited_this, parent_this, visited_other):
        """
        Expande un nivel de la frontera, devuelve el nodo de encuentro si existe.
        """
        current = queue.popleft()
        for neighbor in self.adj_list.get(current, []):
            if neighbor not in visited_this:
                visited_this.add(neighbor)
                parent_this[neighbor] = current
                queue.append(neighbor)
                if neighbor in visited_other:
                    return neighbor
        return None

if __name__ == "__main__":
    # Ejemplo de uso
    g = Graph()
    # Construir grafo
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'G')
    g.add_edge('D', 'H')

    start_node = 'A'
    goal_node = 'G'

    camino = g.bidirectional_search(start_node, goal_node)
    if camino:
        print(f"Camino encontrado entre '{start_node}' y '{goal_node}': {camino}")
    else:
        print(f"No existe camino entre '{start_node}' y '{goal_node}'")
