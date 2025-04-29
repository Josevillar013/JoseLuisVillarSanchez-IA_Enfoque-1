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
    # Caso base: nodo hoja (entero) o profundidad agotada
    if depth == 0 or not isinstance(node, list):
        return node

    if maximizing_player:
        value = -math.inf
        for child in node:
            value = max(value, alpha_beta(child, depth-1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                # Poda beta: ya no interesa explorar más hijos
                break
        return value
    else:
        value = math.inf
        for child in node:
            value = min(value, alpha_beta(child, depth-1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                # Poda alfa: no interesa explorar más hijos
                break
        return value

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
        node=game_tree,
        depth=3,
        alpha=-math.inf,
        beta=math.inf,
        maximizing_player=True
    )

    print(f"Valor minimax con poda alfa-beta: {best_value}")
