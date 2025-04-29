import math

# Tablero de Tic-Tac-Toe representado como lista de 9 celdas: 'X', 'O' o ' '
# Definimos una función de evaluación heurística para estados no terminales.

def imprimir_tablero(tablero):
    for i in range(3):
        print('|'.join(tablero[i*3:(i+1)*3]))
        if i < 2:
            print('-----')
    print()

# Chequeo de ganador o empate

def ganador(tablero):
    lineas = [(0,1,2),(3,4,5),(6,7,8),
              (0,3,6),(1,4,7),(2,5,8),
              (0,4,8),(2,4,6)]
    for a,b,c in lineas:
        if tablero[a] == tablero[b] == tablero[c] and tablero[a] != ' ':
            return tablero[a]
    return None

# Función heurística: valora posibles líneas

def evaluar(tablero):
    """
    Heurística simple:
    +10 por cada línea donde X pueda ganar (2 X y 0 O),
    +1 por cada casilla central ocupada por X,
    -10 por cada línea donde O pueda ganar,
    -1 por casilla central ocupada por O.
    """
    score = 0
    # líneas a evaluar
    lineas = [(0,1,2),(3,4,5),(6,7,8),
              (0,3,6),(1,4,7),(2,5,8),
              (0,4,8),(2,4,6)]
    for a,b,c in lineas:
        valores = [tablero[a], tablero[b], tablero[c]]
        if valores.count('X') == 2 and valores.count('O') == 0:
            score += 10
        elif valores.count('O') == 2 and valores.count('X') == 0:
            score -= 10
    # bonificación por centro
    if tablero[4] == 'X': score += 1
    elif tablero[4] == 'O': score -= 1
    return score

# Minimax con evaluación en profundidad limitada

def minimax(tablero, profundidad, es_max, alpha, beta):
    ganador_actual = ganador(tablero)
    if ganador_actual == 'X':
        return math.inf
    elif ganador_actual == 'O':
        return -math.inf
    if profundidad == 0 or ' ' not in tablero:
        return evaluar(tablero)

    if es_max:
        valor = -math.inf
        for i, casilla in enumerate(tablero):
            if casilla == ' ':
                tablero[i] = 'X'
                valor = max(valor, minimax(tablero, profundidad-1, False, alpha, beta))
                tablero[i] = ' '
                alpha = max(alpha, valor)
                if alpha >= beta:
                    break
        return valor
    else:
        valor = math.inf
        for i, casilla in enumerate(tablero):
            if casilla == ' ':
                tablero[i] = 'O'
                valor = min(valor, minimax(tablero, profundidad-1, True, alpha, beta))
                tablero[i] = ' '
                beta = min(beta, valor)
                if beta <= alpha:
                    break
        return valor

# Función para escoger mejor movimiento usando profundidad limitada

def mejor_movimiento(tablero, profundidad):
    mejor_valor = -math.inf
    movimiento = -1
    for i, casilla in enumerate(tablero):
        if casilla == ' ':
            tablero[i] = 'X'
            puntaje = minimax(tablero, profundidad-1, False, -math.inf, math.inf)
            tablero[i] = ' '
            if puntaje > mejor_valor:
                mejor_valor = puntaje
                movimiento = i
    return movimiento

if __name__ == "__main__":
    tablero = [' '] * 9
    turno = 'X'
    profundidad = 3  # límite para minimax

    while True:
        imprimir_tablero(tablero)
        if turno == 'X':
            mov = mejor_movimiento(tablero, profundidad)
            print(f"IA ('X') juega en: {mov}")
        else:
            mov = int(input("Tu turno ('O'), ingresa posición (0-8): "))
        if tablero[mov] == ' ':
            tablero[mov] = turno
            if ganador(tablero) or ' ' not in tablero:
                imprimir_tablero(tablero)
                break
            turno = 'O' if turno == 'X' else 'X'
        else:
            print("Casilla ocupada, elige otra.")
