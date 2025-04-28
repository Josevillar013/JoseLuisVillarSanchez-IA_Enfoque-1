from collections import deque
 
 def bfs(graph, start):
     # Creamos una cola para almacenar los nodos que estamos explorando
     queue = deque([start])
     # Creamos un conjunto para mantener un registro de los nodos ya visitados
     visited = set()
     visited.add(start)
     
     # Mientras haya nodos en la cola
     while queue:
         # Sacamos el primer nodo de la cola
         node = queue.popleft()
         print("Nodo visitado:", node)
         # Para cada vecino del nodo actual
         for neighbor in graph[node]:
             # Si el vecino no ha sido visitado aún
             if neighbor not in visited:
                 # Lo marcamos como visitado
                 visited.add(neighbor)
                 # Lo añadimos a la cola para explorarlo en la siguiente iteración
                 queue.append(neighbor)
 
 # Ejemplo de uso
 graph = {
     'A': ['B', 'C'],
     'B': ['A', 'D', 'E'],
     'C': ['A', 'F'],
     'D': ['B'],
     'E': ['B', 'F'],
     'F': ['C', 'E']
 }
 start_node = 'A'
 print("Nodos alcanzables desde 'A':")
 bfs(graph, start_node)
 