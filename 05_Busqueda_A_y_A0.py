from collections import deque
import heapq

class Graph:
    """
    Representa un grafo ponderado mediante lista de adyacencia.
    Cada arista puede tener un peso (coste) asociado.
    """
    def __init__(self):
        # adj_list[u] = [(v, peso), ...]
        self.adj_list = {}

    def add_edge(self, u, v, weight=1):
        """
        Agrega una arista dirigida de u a v con coste `weight`.
        Para grafos no dirigidos, llame también a add_edge(v, u, weight).
        """
        self.adj_list.setdefault(u, []).append((v, weight))

    def bfs(self, start):
        """
        Búsqueda en anchura (ignora pesos).
        """
        visited = {start}
        queue = deque([start])
        order = []
        while queue:
            u = queue.popleft()
            order.append(u)
            for v, _ in self.adj_list.get(u, []):
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        return order

    def dfs(self, start):
        """
        Búsqueda en profundidad (recursiva, ignora pesos).
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
        Búsqueda bidireccional (ignora pesos).
        Devuelve el camino si lo encuentra.
        """
        if start == goal:
            return [start]
        parents_s = {start: None}
        parents_g = {goal: None}
        frontier_s = deque([start])
        frontier_g = deque([goal])
        visited_s = {start}
        visited_g = {goal}

        meet = None
        def _step(frontier, visited, parents, other_visited):
            u = frontier.popleft()
            for v, _ in self.adj_list.get(u, []):
                if v not in visited:
                    visited.add(v)
                    parents[v] = u
                    frontier.append(v)
                    if v in other_visited:
                        return v
            return None

        while frontier_s and frontier_g:
            meet = _step(frontier_s, visited_s, parents_s, visited_g)
            if meet: break
            meet = _step(frontier_g, visited_g, parents_g, visited_s)
            if meet: break

        if not meet:
            return None

        # Reconstuir camino
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
        Búsqueda voraz (Greedy Best-First Search).
        `heuristic` es dict: nodo -> estimación coste a meta.
        """
        visited = {start}
        parents = {start: None}
        heap = [(heuristic.get(start, float('inf')), start)]
        while heap:
            _, u = heapq.heappop(heap)
            if u == goal:
                break
            for v, _ in self.adj_list.get(u, []):
                if v not in visited:
                    visited.add(v)
                    parents[v] = u
                    heapq.heappush(heap, (heuristic.get(v, float('inf')), v))
        else:
            return None
        # Reconstrucción
        path, node = [], goal
        while node:
            path.append(node)
            node = parents[node]
        return path[::-1]

    def a_star_search(self, start, goal, heuristic):
        """
        Búsqueda A* con heurística admisible.
        Devuelve (camino, coste total) o None si no hay solución.
        """
        open_set = [(heuristic.get(start, float('inf')), 0, start)]  # (f, g, nodo)
        parents = {start: None}
        g_scores = {start: 0}
        closed = set()

        while open_set:
            f, g, u = heapq.heappop(open_set)
            if u == goal:
                # Reconstruir
                path, node = [], goal
                while node:
                    path.append(node)
                    node = parents[node]
                return path[::-1], g

            if u in closed:
                continue
            closed.add(u)

            for v, w in self.adj_list.get(u, []):
                tentative_g = g + w
                if v in closed and tentative_g >= g_scores.get(v, float('inf')):
                    continue
                if tentative_g < g_scores.get(v, float('inf')):
                    parents[v] = u
                    g_scores[v] = tentative_g
                    f_score = tentative_g + heuristic.get(v, float('inf'))
                    heapq.heappush(open_set, (f_score, tentative_g, v))

        return None

    def a0_search(self, start, goal):
        """
        Búsqueda A* sin heurística (A0), equivalente a Uniform-Cost Search.
        Devuelve (camino, coste total) o None.
        """
        return self.a_star_search(start, goal, heuristic={})

if __name__ == "__main__":
    # Ejemplo de uso
    g = Graph()
    # Agregar aristas ponderadas
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'D', 2)
    g.add_edge('B', 'E', 5)
    g.add_edge('C', 'F', 1)
    g.add_edge('E', 'G', 3)
    g.add_edge('D', 'H', 1)

    # Heurística estimada a 'G'
    heuristic = {'A':6,'B':4,'C':2,'D':3,'E':6,'F':1,'G':0,'H':5}

    start, goal = 'A', 'G'
    res_astar = g.a_star_search(start, goal, heuristic)
    res_a0 = g.a0_search(start, goal)

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
