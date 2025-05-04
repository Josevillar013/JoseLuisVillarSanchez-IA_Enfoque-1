class Node:
    """
    Representa un nodo en un árbol de juego con chance.
    - type: tipo de nodo, que puede ser 'max', 'min', 'chance', o 'leaf'.
    - children: lista de nodos hijos (vacío para 'leaf').
    - prob: lista de probabilidades para cada hijo (solo para 'chance').
    - value: valor numérico para hojas (solo para 'leaf').
    """
    def __init__(self, node_type, children=None, prob=None, value=None):
        # Inicialización de los atributos del nodo.
        self.type = node_type  # Tipo de nodo: 'max', 'min', 'chance' o 'leaf'.
        self.children = children or []  # Lista de nodos hijos, vacía si no tiene hijos.
        self.prob = prob or []  # Lista de probabilidades, solo relevante para nodos 'chance'.
        self.value = value  # Valor numérico para nodos hoja.

def expectiminimax(node):
    """
    Algoritmo Expectiminimax (Minimax con nodos de chance).
    - max: maximiza el valor de la jugada.
    - min: minimiza el valor de la jugada.
    - chance: calcula el valor esperado según probabilidades de cada hijo.
    - leaf: retorna el valor numérico del nodo hoja.
    """
    if node.type == 'leaf':
        # Si el nodo es de tipo 'leaf', retornamos su valor numérico.
        return node.value
    elif node.type == 'max':
        # Si el nodo es de tipo 'max', maximiza el valor de los hijos.
        # Llama recursivamente a expectiminimax para cada hijo y devuelve el máximo.
        return max(expectiminimax(child) for child in node.children)
    elif node.type == 'min':
        # Si el nodo es de tipo 'min', minimiza el valor de los hijos.
        # Llama recursivamente a expectiminimax para cada hijo y devuelve el mínimo.
        return min(expectiminimax(child) for child in node.children)
    elif node.type == 'chance':
        # Si el nodo es de tipo 'chance', calcula el valor esperado considerando las probabilidades.
        expected = 0  # Inicializamos el valor esperado.
        for p, child in zip(node.prob, node.children):
            # Para cada hijo y su probabilidad, sumamos p * valor del hijo.
            expected += p * expectiminimax(child)
        return expected
    else:
        # Si el tipo de nodo no es reconocido, lanzamos una excepción.
        raise ValueError(f"Tipo de nodo desconocido: {node.type}")

if __name__ == "__main__":
    # Ejemplo de un árbol de juego con un nodo de chance y nodos max y min.

    # Crear los nodos hoja con sus valores respectivos.
    leaf1 = Node('leaf', value=3)  # Nodo hoja con valor 3.
    leaf2 = Node('leaf', value=5)  # Nodo hoja con valor 5.
    leaf3 = Node('leaf', value=2)  # Nodo hoja con valor 2.
    leaf4 = Node('leaf', value=9)  # Nodo hoja con valor 9.
    leaf5 = Node('leaf', value=0)  # Nodo hoja con valor 0.
    leaf6 = Node('leaf', value=7)  # Nodo hoja con valor 7.

    # Crear nodos 'min', que eligen el mínimo entre sus hijos.
    min1 = Node('min', children=[leaf1, leaf2])  # min{3, 5} = 3
    min2 = Node('min', children=[leaf3, leaf4])  # min{2, 9} = 2
    min3 = Node('min', children=[leaf5, leaf6])  # min{0, 7} = 0

    # Crear nodo 'chance' con probabilidades asociadas a sus hijos.
    chance = Node('chance', children=[min1, min2, min3], prob=[0.5, 0.25, 0.25])

    # Crear nodo 'max', que elige el máximo entre sus hijos (en este caso, es el nodo de 'chance').
    root = Node('max', children=[chance])

    # Calcular el valor Expectiminimax para la raíz del árbol (con el nodo 'max' alrededor del nodo 'chance').
    result = expectiminimax(root)

    # Imprimir el resultado final de la evaluación.
    print(f"Valor Expectiminimax de la raíz: {result}")
