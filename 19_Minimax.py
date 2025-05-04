# Tablero como lista de 9 elementos (3x3)
# 'X' es el jugador Max, 'O' es el jugador Min

def imprimir_tablero(tablero):
    # Esta función imprime el tablero de 3x3 en forma de rejilla.
    for i in range(3):
        # Imprime cada fila del tablero separada por "|"
        print("|".join(tablero[i*3:(i+1)*3]))
        # Si no es la última fila, imprime una línea separadora
        if i < 2:
            print("-" * 5)

def ganador(tablero):
    # Esta función determina si hay un ganador en el tablero.
    # Define todas las combinaciones ganadoras (filas, columnas, diagonales)
    combinaciones = [(0,1,2), (3,4,5), (6,7,8),
                     (0,3,6), (1,4,7), (2,5,8),
                     (0,4,8), (2,4,6)]
    # Revisa todas las combinaciones ganadoras
    for a,b,c in combinaciones:
        # Si tres posiciones consecutivas son iguales y no están vacías, se ha encontrado un ganador
        if tablero[a] == tablero[b] == tablero[c] and tablero[a] != " ":
            return tablero[a]  # Devuelve el ganador ('X' o 'O')
    return None  # Si no hay ganador, devuelve None

def movimientos_disponibles(tablero):
    # Devuelve una lista con los índices de los espacios vacíos en el tablero
    return [i for i, v in enumerate(tablero) if v == " "]

def minimax(tablero, es_max):
    # Función recursiva que implementa el algoritmo Minimax para evaluar los movimientos.
    gan = ganador(tablero)
    # Si hay un ganador, devuelve la puntuación:
    # 1 para ganar con 'X', -1 para ganar con 'O'
    if gan == 'X':
        return 1
    elif gan == 'O':
        return -1
    # Si el tablero está lleno (empate), devuelve 0
    elif not movimientos_disponibles(tablero):
        return 0

    # Si es el turno de 'X' (Max), buscamos el mejor movimiento posible
    if es_max:
        mejor = -float('inf')  # Inicializa el valor de la mejor puntuación como el más bajo posible
        # Recorre todos los movimientos disponibles
        for i in movimientos_disponibles(tablero):
            tablero[i] = 'X'  # Realiza el movimiento de 'X'
            puntuacion = minimax(tablero, False)  # Llama recursivamente para el turno de 'O'
            tablero[i] = ' '  # Deshace el movimiento
            mejor = max(mejor, puntuacion)  # Actualiza la mejor puntuación encontrada
        return mejor  # Devuelve la mejor puntuación para 'X'

    # Si es el turno de 'O' (Min), buscamos el peor movimiento posible para 'X'
    else:
        peor = float('inf')  # Inicializa el valor de la peor puntuación como el más alto posible
        # Recorre todos los movimientos disponibles
        for i in movimientos_disponibles(tablero):
            tablero[i] = 'O'  # Realiza el movimiento de 'O'
            puntuacion = minimax(tablero, True)  # Llama recursivamente para el turno de 'X'
            tablero[i] = ' '  # Deshace el movimiento
            peor = min(peor, puntuacion)  # Actualiza la peor puntuación encontrada
        return peor  # Devuelve la peor puntuación para 'O'

def mejor_movimiento(tablero):
    # Esta función calcula el mejor movimiento para 'X' (IA) usando el algoritmo Minimax.
    mejor_puntaje = -float('inf')  # Inicializa la mejor puntuación como el valor más bajo posible
    movimiento = -1  # Inicializa el índice del mejor movimiento

    # Recorre todos los movimientos disponibles en el tablero
    for i in movimientos_disponibles(tablero):
        tablero[i] = 'X'  # Realiza el movimiento de 'X'
        puntuacion = minimax(tablero, False)  # Evalúa la puntuación del movimiento para 'X'
        tablero[i] = ' '  # Deshace el movimiento
        # Si el puntaje de este movimiento es mejor que el anterior, actualiza el mejor movimiento
        if puntuacion > mejor_puntaje:
            mejor_puntaje = puntuacion
            movimiento = i
    return movimiento  # Devuelve el índice del mejor movimiento para 'X'

# Prueba del juego (simula una partida entre el jugador 'X' (IA) y el jugador 'O' humano)
tablero = [" "] * 9  # Inicializa el tablero vacío (una lista de 9 espacios vacíos)
turno = 'X'  # Comienza el turno del jugador 'X' (IA)

while True:
    imprimir_tablero(tablero)  # Muestra el tablero actualizado
    if turno == 'X':
        # Si es el turno de 'X' (IA), la IA elige el mejor movimiento
        mov = mejor_movimiento(tablero)
        print(f"Jugador X (IA) elige: {mov}")
    else:
        # Si es el turno de 'O' (jugador humano), pide al jugador que elija un movimiento
        mov = int(input("Elige movimiento (0-8): "))  # El jugador ingresa un número entre 0 y 8

    # Si el movimiento es válido (el espacio está vacío), se realiza el movimiento
    if tablero[mov] == " ":
        tablero[mov] = turno  # Se actualiza el tablero con el movimiento
        # Si hay un ganador, imprime el tablero y muestra quién ha ganado
        if ganador(tablero):
            imprimir_tablero(tablero)
            print(f"\n¡Ganador: {turno}!")
            break  # Termina el juego
        # Si ya no hay más movimientos disponibles (empate), muestra el tablero y termina el juego
        elif not movimientos_disponibles(tablero):
            imprimir_tablero(tablero)
            print("\n¡Empate!")
            break  # Termina el juego
        # Cambia el turno al otro jugador
        turno = 'O' if turno == 'X' else 'X'
    else:
        print("Movimiento inválido, intenta de nuevo.")  # Si el movimiento no es válido, pide uno nuevo
