import math

# Tablero de Tic-Tac-Toe representado como lista de 9 celdas: 'X', 'O' o ' '
# Definimos una función de evaluación heurística para estados no terminales.

def imprimir_tablero(tablero):
    """
    Imprime el tablero de Tic-Tac-Toe.
    Divide el tablero en 3 filas y las imprime con separadores entre las celdas.
    """
    for i in range(3):
        # Imprime una fila del tablero uniendo las 3 celdas con '|'
        print('|'.join(tablero[i*3:(i+1)*3]))
        if i < 2:
            # Imprime separador entre las filas (cuando no es la última fila)
            print('-----')
    print()  # Salto de línea al final

# Chequeo de ganador o empate

def ganador(tablero):
    """
    Chequea si hay un ganador en el tablero.
    Retorna 'X' si X ha ganado, 'O' si O ha ganado, o None si no hay ganador.
    """
    # Combinaciones de celdas que forman líneas ganadoras (horizontal, vertical, diagonal)
    lineas = [(0,1,2),(3,4,5),(6,7,8),
              (0,3,6),(1,4,7),(2,5,8),
              (0,4,8),(2,4,6)]
    # Recorremos todas las combinaciones de celdas que forman una línea
    for a,b,c in lineas:
        # Si todas las celdas en una línea tienen el mismo valor y no están vacías
        if tablero[a] == tablero[b] == tablero[c] and tablero[a] != ' ':
            return tablero[a]  # Retorna el valor ('X' o 'O') que ha ganado
    return None  # Si no hay ganador, retorna None

# Función heurística: valora posibles líneas

def evaluar(tablero):
    """
    Heurística simple para evaluar el estado del tablero:
    +10 por cada línea donde X pueda ganar (2 X y 0 O),
    +1 por cada casilla central ocupada por X,
    -10 por cada línea donde O pueda ganar,
    -1 por casilla central ocupada por O.
    """
    score = 0  # Variable para almacenar la puntuación total
    # Combinaciones de líneas a evaluar (horizontal, vertical, diagonal)
    lineas = [(0,1,2),(3,4,5),(6,7,8),
              (0,3,6),(1,4,7),(2,5,8),
              (0,4,8),(2,4,6)]
    # Recorremos todas las combinaciones de celdas que forman una línea
    for a,b,c in lineas:
        valores = [tablero[a], tablero[b], tablero[c]]  # Los valores de las 3 celdas de la línea
        # Si hay 2 X y 0 O en la línea, significa que X está cerca de ganar
        if valores.count('X') == 2 and valores.count('O') == 0:
            score += 10  # Añadimos 10 puntos
        # Si hay 2 O y 0 X en la línea, significa que O está cerca de ganar
        elif valores.count('O') == 2 and valores.count('X') == 0:
            score -= 10  # Restamos 10 puntos
    # Bonificación por centro: evaluamos la casilla central (índice 4)
    if tablero[4] == 'X': score += 1  # Si X ocupa el centro, sumamos 1 punto
    elif tablero[4] == 'O': score -= 1  # Si O ocupa el centro, restamos 1 punto
    return score  # Retornamos la puntuación total

# Minimax con evaluación en profundidad limitada

def minimax(tablero, profundidad, es_max, alpha, beta):
    """
    Función recursiva que implementa el algoritmo Minimax con poda alfa-beta.
    - profundidad: cuántos niveles de profundidad aún quedan por explorar.
    - es_max: True si el jugador actual es el maximizador (X), False si es el minimizador (O).
    - alpha: valor máximo conocido para el maximizador.
    - beta: valor mínimo conocido para el minimizador.
    Retorna el valor de la mejor jugada según Minimax con poda alfa-beta.
    """
    ganador_actual = ganador(tablero)  # Comprobamos si hay un ganador
    if ganador_actual == 'X':
        return math.inf  # Si X ganó, retornamos un valor positivo muy alto
    elif ganador_actual == 'O':
        return -math.inf  # Si O ganó, retornamos un valor negativo muy bajo
    if profundidad == 0 or ' ' not in tablero:
        return evaluar(tablero)  # Si alcanzamos la profundidad máxima o el tablero está lleno, evaluamos el estado

    if es_max:  # Si es el turno del jugador maximizador (X)
        valor = -math.inf  # Iniciamos con el valor más bajo posible
        for i, casilla in enumerate(tablero):
            if casilla == ' ':  # Si la casilla está vacía
                tablero[i] = 'X'  # El maximizador (X) realiza un movimiento
                valor = max(valor, minimax(tablero, profundidad-1, False, alpha, beta))  # Recursión minimax para el siguiente jugador (O)
                tablero[i] = ' '  # Revertimos el movimiento
                alpha = max(alpha, valor)  # Actualizamos el valor de alpha
                if alpha >= beta:  # Poda beta: si el valor de alpha es mayor o igual a beta, dejamos de explorar
                    break
        return valor  # Retornamos el valor máximo encontrado

    else:  # Si es el turno del jugador minimizador (O)
        valor = math.inf  # Iniciamos con el valor más alto posible
        for i, casilla in enumerate(tablero):
            if casilla == ' ':  # Si la casilla está vacía
                tablero[i] = 'O'  # El minimizador (O) realiza un movimiento
                valor = min(valor, minimax(tablero, profundidad-1, True, alpha, beta))  # Recursión minimax para el siguiente jugador (X)
                tablero[i] = ' '  # Revertimos el movimiento
                beta = min(beta, valor)  # Actualizamos el valor de beta
                if beta <= alpha:  # Poda alfa: si el valor de beta es menor o igual a alpha, dejamos de explorar
                    break
        return valor  # Retornamos el valor mínimo encontrado

# Función para escoger mejor movimiento usando profundidad limitada

def mejor_movimiento(tablero, profundidad):
    """
    Calcula el mejor movimiento para el jugador maximizador (X) usando el algoritmo Minimax con poda alfa-beta.
    """
    mejor_valor = -math.inf  # Inicializamos el valor más bajo posible
    movimiento = -1  # Inicializamos el índice del mejor movimiento
    for i, casilla in enumerate(tablero):
        if casilla == ' ':  # Si la casilla está vacía
            tablero[i] = 'X'  # Realizamos el movimiento de X en esa casilla
            puntaje = minimax(tablero, profundidad-1, False, -math.inf, math.inf)  # Evaluamos el movimiento
            tablero[i] = ' '  # Revertimos el movimiento
            if puntaje > mejor_valor:  # Si este movimiento tiene una mejor puntuación
                mejor_valor = puntaje  # Actualizamos el valor del mejor movimiento
                movimiento = i  # Guardamos el índice de la mejor casilla
    return movimiento  # Retornamos el índice de la mejor casilla

if __name__ == "__main__":
    tablero = [' '] * 9  # Inicializamos el tablero vacío
    turno = 'X'  # El jugador X comienza
    profundidad = 3  # Definimos la profundidad máxima para el algoritmo minimax

    while True:
        imprimir_tablero(tablero)  # Imprimimos el estado actual del tablero
        if turno == 'X':  # Si es el turno de la IA (X)
            mov = mejor_movimiento(tablero, profundidad)  # Calculamos el mejor movimiento
            print(f"IA ('X') juega en: {mov}")  # Mostramos el movimiento de la IA
        else:  # Si es el turno del jugador humano (O)
            mov = int(input("Tu turno ('O'), ingresa posición (0-8): "))  # Pedimos al jugador que ingrese un movimiento
        if tablero[mov] == ' ':  # Verificamos si la casilla está vacía
            tablero[mov] = turno  # Realizamos el movimiento en el tablero
            if ganador(tablero) or ' ' not in tablero:  # Si hay un ganador o el tablero está lleno
                imprimir_tablero(tablero)  # Imprimimos el tablero final
                break  # Terminamos el juego
            turno = 'O' if turno == 'X' else 'X'  # Cambiamos el turno entre los jugadores
        else:
            print("Casilla ocupada, elige otra.")  # Si la casilla está ocupada, pedimos un nuevo movimiento
