# Tablero como lista de 9 elementos (3x3)
# 'X' es el jugador Max, 'O' es el jugador Min

def imprimir_tablero(tablero):
    for i in range(3):
        print("|".join(tablero[i*3:(i+1)*3]))
        if i < 2:
            print("-" * 5)

def ganador(tablero):
    combinaciones = [(0,1,2), (3,4,5), (6,7,8),
                     (0,3,6), (1,4,7), (2,5,8),
                     (0,4,8), (2,4,6)]
    for a,b,c in combinaciones:
        if tablero[a] == tablero[b] == tablero[c] and tablero[a] != " ":
            return tablero[a]
    return None

def movimientos_disponibles(tablero):
    return [i for i, v in enumerate(tablero) if v == " "]

def minimax(tablero, es_max):
    gan = ganador(tablero)
    if gan == 'X':
        return 1
    elif gan == 'O':
        return -1
    elif not movimientos_disponibles(tablero):
        return 0

    if es_max:
        mejor = -float('inf')
        for i in movimientos_disponibles(tablero):
            tablero[i] = 'X'
            puntuacion = minimax(tablero, False)
            tablero[i] = ' '
            mejor = max(mejor, puntuacion)
        return mejor
    else:
        peor = float('inf')
        for i in movimientos_disponibles(tablero):
            tablero[i] = 'O'
            puntuacion = minimax(tablero, True)
            tablero[i] = ' '
            peor = min(peor, puntuacion)
        return peor

def mejor_movimiento(tablero):
    mejor_puntaje = -float('inf')
    movimiento = -1
    for i in movimientos_disponibles(tablero):
        tablero[i] = 'X'
        puntuacion = minimax(tablero, False)
        tablero[i] = ' '
        if puntuacion > mejor_puntaje:
            mejor_puntaje = puntuacion
            movimiento = i
    return movimiento

# Prueba
tablero = [" "] * 9
turno = 'X'

while True:
    imprimir_tablero(tablero)
    if turno == 'X':
        mov = mejor_movimiento(tablero)
        print(f"Jugador X (IA) elige: {mov}")
    else:
        mov = int(input("Elige movimiento (0-8): "))
    if tablero[mov] == " ":
        tablero[mov] = turno
        if ganador(tablero):
            imprimir_tablero(tablero)
            print(f"\n¡Ganador: {turno}!")
            break
        elif not movimientos_disponibles(tablero):
            imprimir_tablero(tablero)
            print("\n¡Empate!")
            break
        turno = 'O' if turno == 'X' else 'X'
    else:
        print("Movimiento inválido, intenta de nuevo.")
