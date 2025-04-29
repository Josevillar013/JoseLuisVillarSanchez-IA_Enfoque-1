class Node:
    """
    Representa un nodo en un árbol de juego con chance.
    - type: 'max', 'min', 'chance', o 'leaf'
    - children: lista de nodos hijos (vacío para 'leaf')
    - prob: lista de probabilidades para cada hijo (solo para 'chance')
    - value: valor numérico para hojas
    """
    def __init__(self, node_type, children=None, prob=None, value=None):
        self.type = node_type
        self.children = children or []
        self.prob = prob or []
        self.value = value


def expectiminimax(node):
    """
    Algoritmo Expectiminimax (Minimax con nodos de chance).
    - max: maximiza el valor
    - min: minimiza el valor
    - chance: calcula el valor esperado según probabilidades
    - leaf: retorna el valor
    """
    if node.type == 'leaf':
        return node.value
    elif node.type == 'max':
        return max(expectiminimax(child) for child in node.children)
    elif node.type == 'min':
        return min(expectiminimax(child) for child in node.children)
    elif node.type == 'chance':
        expected = 0
        for p, child in zip(node.prob, node.children):
            expected += p * expectiminimax(child)
        return expected
    else:
        raise ValueError(f"Tipo de nodo desconocido: {node.type}")

if __name__ == "__main__":
    # Ejemplo de árbol:
    #        C
    #      / | \
    #     /  |  \
    #    M   M   M   (chance con 3 hijos prob 0.5,0.25,0.25)
    #   / \  |\  |\
    #  L  L  L L L L (hojas con valores)

    # Hojas
    leaf1 = Node('leaf', value=3)
    leaf2 = Node('leaf', value=5)
    leaf3 = Node('leaf', value=2)
    leaf4 = Node('leaf', value=9)
    leaf5 = Node('leaf', value=0)
    leaf6 = Node('leaf', value=7)

    # Nodos min
    min1 = Node('min', children=[leaf1, leaf2])  # min{3,5} = 3
    min2 = Node('min', children=[leaf3, leaf4])  # min{2,9} = 2
    min3 = Node('min', children=[leaf5, leaf6])  # min{0,7} = 0

    # Nodo chance (probabilidades deben sumar 1)
    chance = Node('chance', children=[min1, min2, min3], prob=[0.5, 0.25, 0.25])

    # Raíz minimax con un max alrededor del chance
    root = Node('max', children=[chance])

    # Calcular expectiminimax
    result = expectiminimax(root)
    print(f"Valor Expectiminimax de la raíz: {result}")
