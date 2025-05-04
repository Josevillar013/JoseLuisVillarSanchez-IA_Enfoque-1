class Graph:
    """
    Representa un grafo mediante lista de adyacencia.
    El grafo es representado como un diccionario donde las claves son los nodos 
    y los valores son las listas de nodos adyacentes.
    """
    def __init__(self):
        # Inicializa un diccionario vacío que representará la lista de adyacencia.
        self.adj = {}

    def add_edge(self, u, v):
        """
        Añade una arista dirigida desde el nodo u hacia el nodo v.
        Si u no tiene vecinos, se inicializa una lista vacía.
        """
        self.adj.setdefault(u, []).append(v)

    def neighbors(self, u):
        """
        Retorna la lista de nodos vecinos de u.
        Si u no tiene vecinos (no está en el grafo), retorna una lista vacía.
        """
        return self.adj.get(u, [])


# Resultado especial para Depth-Limited Search
CUTOFF = 'CUTOFF'  # Utilizado para indicar que la búsqueda se cortó debido al límite de profundidad
FAILURE = None      # Utilizado para indicar que la búsqueda falló (no se encontró el objetivo)

def depth_limited_search(graph, start, goal, limit):
    """
    Realiza una búsqueda con profundidad limitada (Depth-Limited Search).
    - graph: instancia del grafo.
    - start: nodo inicial desde donde comenzamos la búsqueda.
    - goal: nodo objetivo que queremos encontrar.
    - limit: profundidad máxima a explorar.
    Retorna el camino desde start a goal, o CUTOFF si se alcanza el límite de profundidad,
    o FAILURE si no se encuentra el objetivo.
    """
    def recursive_dls(node, goal, limit, path):
        """
        Función recursiva que implementa la búsqueda con profundidad limitada.
        - node: nodo actual en la recursión.
        - goal: nodo objetivo.
        - limit: profundidad restante.
        - path: camino actual recorrido.
        """
        if node == goal:
            # Si el nodo actual es el objetivo, retornamos el camino actual
            return path
        if limit == 0:
            # Si alcanzamos el límite de profundidad, retornamos CUTOFF
            return CUTOFF
        
        cutoff_occurred = False  # Variable para verificar si ocurrió un corte en algún hijo
        for child in graph.neighbors(node):
            # Recorremos todos los nodos vecinos del nodo actual
            if child not in path:
                # Evitamos ciclos: solo continuamos si el nodo no está en el camino actual
                result = recursive_dls(child, goal, limit - 1, path + [child])
                
                if result == CUTOFF:
                    # Si el resultado es CUTOFF, marcamos que ocurrió un corte
                    cutoff_occurred = True
                elif result is not FAILURE:
                    # Si encontramos un resultado válido (camino hacia el objetivo)
                    return result
        
        # Si ocurrió un corte, retornamos CUTOFF, de lo contrario retornamos FAILURE
        return CUTOFF if cutoff_occurred else FAILURE

    # Comienza la búsqueda desde el nodo inicial
    return recursive_dls(start, goal, limit, [start])


def iterative_deepening_search(graph, start, goal, max_horizon):
    """
    Realiza una búsqueda en profundidad de iteración profunda (IDDFS) con horizonte creciente.
    - max_horizon: la profundidad máxima que exploraremos en el grafo.
    Retorna el primer camino encontrado hacia el objetivo o FAILURE si no se encuentra.
    """
    for limit in range(max_horizon + 1):
        # Realiza una búsqueda con profundidad limitada para cada nivel desde 0 hasta max_horizon
        result = depth_limited_search(graph, start, goal, limit)
        if result is not CUTOFF:
            # Si la búsqueda no fue cortada (es decir, encontramos el objetivo), retornamos el camino
            return result
    
    # Si no se encuentra un camino dentro de los límites dados, retornamos FAILURE
    return FAILURE

if __name__ == "__main__":
    # Creamos un grafo de ejemplo con varios nodos y aristas.
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('C', 'E')
    g.add_edge('D', 'F')
    g.add_edge('E', 'G')

    start, goal = 'A', 'G'  # Definimos el nodo de inicio y el objetivo
    horizon = 3  # Establecemos el límite de profundidad para la búsqueda con profundidad limitada
    print(f"Depth-Limited Search con horizonte={horizon}:")
    # Ejecutamos la búsqueda con profundidad limitada con el horizonte definido
    path = depth_limited_search(g, start, goal, horizon)
    print(path)  # Mostramos el camino encontrado o el resultado (CUTOFF/FAILURE)

    print("\nIterative Deepening hasta horizonte=5:")
    # Ejecutamos la búsqueda en profundidad de iteración profunda con un horizonte máximo de 5
    path_iddfs = iterative_deepening_search(g, start, goal, 5)
    print(path_iddfs)  # Mostramos el primer camino encontrado o FAILURE
