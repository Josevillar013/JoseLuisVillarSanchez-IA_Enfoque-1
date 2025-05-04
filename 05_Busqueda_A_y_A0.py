from collections import deque  # Importa deque para colas eficientes (BFS, búsquedas bidireccionales)
import heapq  # Importa heapq para manejar colas de prioridad (Greedy, A*)

class Graph:
    """
    Representa un grafo ponderado mediante lista de adyacencia.
    Cada arista puede tener un peso (coste) asociado.
    """
    def __init__(self):
        # Diccionario: clave = nodo, valor = lista de tuplas (vecino, peso)
        self.adj_list = {}

    def add_edge(self, u, v, weight=1):
        """
        Agrega una arista dirigida de u a v con peso (coste).
        Para grafos no dirigidos, también se debe llamar a add_edge(v, u, weight).
        """
        self.adj_list.setdefault(u, []).append((v, weight))

    def bfs(self, start):
        """
        Búsqueda en anchura (ignora pesos de las aristas).
        Retorna una lista con el orden de visita de los nodos.
        """
        visited = {start}              # Conjunto de nodos visitados
        queue = deque([start])         # Cola FIFO con nodo inicial
        order = []                     # Lista del orden en que se visitan los nodos

        while queue:
            u = queue.popleft()        # Saca el primer nodo de la cola
            order.append(u)            # Añade al orden de visita
            for v, _ in self.adj_list.get(u, []):  # Itera sobre los vecinos (ignora pesos)
                if v not in visited:
                    visited.add(v)
                    queue.append(v)

        return order

    def dfs(self, start):
        """
        Búsqueda en profundidad (recursiva), también ignora pesos.
        """
        visited, order = set(), []

        def _dfs(u):
            visited.add(u)
            order.append(u)
            for v, _ in self.adj_list.get(u, []):
                if v not in visited:
                    _dfs(v)

        _dfs(start)
        return order

    def bidirectional_search(self, start, goal):
        """
        Búsqueda bidireccional (desde inicio y fin), ignora pesos.
        Devuelve el camino si lo encuentra, o None.
        """
        if start == goal:
            return [start]  # Caso trivial

        # Inicializa padres, fronteras y visitados desde ambos extremos
        parents_s = {start: None}
        parents_g = {goal: None}
        frontier_s = deque([start])
        frontier_g = deque([goal])
        visited_s = {start}
        visited_g = {goal}
        meet = None

        def _step(frontier, visited, parents, other_visited):
            # Expande un nodo de la frontera
            u = frontier.popleft()
            for v, _ in self.adj_list.get(u, []):
                if v not in visited:
                    visited.add(v)
                    parents[v] = u
                    frontier.append(v)
                    if v in other_visited:
                        return v  # Nodo de encuentro
            return None

        while frontier_s and frontier_g:
            meet = _step(frontier_s, visited_s, parents_s, visited_g)
            if meet: break
            meet = _step(frontier_g, visited_g, parents_g, visited_s)
            if meet: break

        if not meet:
            return None  # No se encontró camino

        # Reconstruye el camino desde el nodo de encuentro
        path_s, node = [], meet
        while node:
            path_s.append(node)
            node = parents_s[node]
        path_s.reverse()

        path_g, node = [], parents_g.get(meet)
        while node:
            path_g.append(node)
            node = parents_g[node]

        return path_s + path_g

    def greedy_search(self, start, goal, heuristic):
        """
        Búsqueda voraz basada en una heurística.
        Elige el siguiente nodo basado en la menor estimación heurística.
        """
        visited = {start}
        parents = {start: None}
        heap = [(heuristic.get(start, float('inf')), start)]  # (valor heurístico, nodo)

        while heap:
            _, u = heapq.heappop(heap)  # Extrae nodo con menor heurística
            if u == goal:
                break
            for v, _ in self.adj_list.get(u, []):
                if v not in visited:
                    visited.add(v)
                    parents[v] = u
                    heapq.heappush(heap, (heuristic.get(v, float('inf')), v))
        else:
            return None  # No se encontró camino

        # Reconstrucción del camino
        path, node = [], goal
        while node:
            path.append(node)
            node = parents[node]
        return path[::-1]  # Camino en orden correcto

    def a_star_search(self, start, goal, heuristic):
        """
        Búsqueda A* con heurística admisible.
        Usa f(n) = g(n) + h(n), donde:
        - g(n): coste desde el inicio hasta n
        - h(n): estimación heurística desde n hasta el objetivo
        """
        open_set = [(heuristic.get(start, float('inf')), 0, start)]  # (f, g, nodo)
        parents = {start: None}
        g_scores = {start: 0}  # Coste acumulado desde el inicio
        closed = set()         # Conjunto de nodos ya evaluados

        while open_set:
            f, g, u = heapq.heappop(open_set)  # Nodo con menor f(n)
            if u == goal:
                # Reconstrucción del camino
                path, node = [], goal
                while node:
                    path.append(node)
                    node = parents[node]
                return path[::-1], g  # Devuelve camino y coste total

            if u in closed:
                continue
            closed.add(u)

            for v, w in self.adj_list.get(u, []):  # Para cada vecino
                tentative_g = g + w  # Nuevo coste g(n)
                if v in closed and tentative_g >= g_scores.get(v, float('inf')):
                    continue
                if tentative_g < g_scores.get(v, float('inf')):
                    parents[v] = u
                    g_scores[v] = tentative_g
                    f_score = tentative_g + heuristic.get(v, float('inf'))
                    heapq.heappush(open_set, (f_score, tentative_g, v))

        return None  # Si no hay camino

    def a0_search(self, start, goal):
        """
        Búsqueda A* sin heurística (equivalente a Uniform Cost Search o Dijkstra).
        Se llama A0 porque la heurística es siempre 0.
        """
        return self.a_star_search(start, goal, heuristic={})  # Pasa heurística vacía

# BLOQUE PRINCIPAL: PRUEBA DE USO
if __name__ == "__main__":
    g = Graph()

    # Se agregan aristas con pesos
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'D', 2)
    g.add_edge('B', 'E', 5)
    g.add_edge('C', 'F', 1)
    g.add_edge('E', 'G', 3)
    g.add_edge('D', 'H', 1)

    # Estimación heurística de cada nodo al objetivo 'G'
    heuristic = {
        'A': 6,
        'B': 4,
        'C': 2,
        'D': 3,
        'E': 6,
        'F': 1,
        'G': 0,
        'H': 5
    }

    start, goal = 'A', 'G'

    # Búsqueda A* con heurística
    res_astar = g.a_star_search(start, goal, heuristic)

    # Búsqueda A* sin heurística (A0 / Uniform Cost)
    res_a0 = g.a0_search(start, goal)

    # Resultados
    if res_astar:
        path, cost = res_astar
        print(f"A* → Camino: {path}, Coste: {cost}")
    else:
        print("A*: Sin solución")

    if res_a0:
        path0, cost0 = res_a0
        print(f"A0 (UCS) → Camino: {path0}, Coste: {cost0}")
    else:
        print("A0: Sin solución")
