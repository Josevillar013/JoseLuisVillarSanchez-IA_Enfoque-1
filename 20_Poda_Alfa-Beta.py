import math

def alpha_beta(node, depth, alpha, beta, maximizing_player):
    """
    Búsqueda minimax con poda alfa-beta.
    - node: árbol de juego representado como listas anidadas; las hojas son valores numéricos.
    - depth: profundidad restante (0 en las hojas).
    - alpha, beta: parámetros de poda.
    - maximizing_player: True si es el turno del jugador maximizador, False para el minimizador.
    Retorna el valor minimax con poda alfa-beta.
    """
    # Caso base: si la profundidad es 0 o el nodo es una hoja (valor numérico)
    if depth == 0 or not isinstance(node, list):
        return node  # Devuelve el valor del nodo (hoja) en el árbol

    if maximizing_player:
        # Si es el turno del jugador maximizador, inicializamos el valor con -infinito
        value = -math.inf
        for child in node:
            # Evaluamos cada hijo del nodo actual recursivamente con poda alfa-beta
            value = max(value, alpha_beta(child, depth-1, alpha, beta, False))
            # Actualizamos el valor de alpha, que es el valor máximo encontrado hasta el momento
            alpha = max(alpha, value)
            # Poda beta: si alpha >= beta, ya no necesitamos explorar más hijos
            if alpha >= beta:
                break  # Salimos del ciclo ya que no vale la pena seguir explorando

        return value  # Retorna el valor máximo encontrado

    else:
        # Si es el turno del jugador minimizador, inicializamos el valor con +infinito
        value = math.inf
        for child in node:
            # Evaluamos cada hijo del nodo actual recursivamente con poda alfa-beta
            value = min(value, alpha_beta(child, depth-1, alpha, beta, True))
            # Actualizamos el valor de beta, que es el valor mínimo encontrado hasta el momento
            beta = min(beta, value)
            # Poda alfa: si beta <= alpha, ya no necesitamos explorar más hijos
            if beta <= alpha:
                break  # Salimos del ciclo ya que no vale la pena seguir explorando

        return value  # Retorna el valor mínimo encontrado

if __name__ == "__main__":
    # Ejemplo de árbol de juego (3 niveles de profundidad):
    # Raíz tiene 2 hijos; cada hijo tiene 2 hijos; cada nieto es un valor numérico.
    game_tree = [
        [   # Subárbol 1
            [3, 5],   # Hoja: 3, 5
            [6, 9]
        ],
        [   # Subárbol 2
            [1, -1],
            [0, 4]
        ]
    ]

    # Ejecutar alpha-beta desde la raíz
    best_value = alpha_beta(
        node=game_tree,  # El árbol de juego
        depth=3,         # La profundidad máxima del árbol
        alpha=-math.inf, # Valor inicial de alpha (más bajo posible)
        beta=math.inf,   # Valor inicial de beta (más alto posible)
        maximizing_player=True  # Inicia con el jugador maximizador
    )

    # Imprime el valor minimax calculado con poda alfa-beta
    print(f"Valor minimax con poda alfa-beta: {best_value}")
