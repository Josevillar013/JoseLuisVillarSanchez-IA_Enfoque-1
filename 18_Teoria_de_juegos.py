def find_pure_nash(actions, payoffs):
    """
    Encuentra los equilibrios de Nash puros en un juego normal de dos jugadores.
    - actions: lista de acciones para cada jugador, p.ej. ['A', 'B'].
    - payoffs: diccionario que mapea (a1, a2) -> (u1, u2).
    Retorna lista de tuplas (a1, a2) que son equilibrios de Nash.
    """
    nash_equilibria = []
    for (a1, a2), (u1, u2) in payoffs.items():
        # Verificar desviaciones unilaterales
        # Jugador 1
        best_response_1 = True
        for a1_alt in actions:
            if a1_alt != a1:
                u1_alt = payoffs[(a1_alt, a2)][0]
                if u1_alt > u1:
                    best_response_1 = False
                    break
        # Jugador 2
        best_response_2 = True
        for a2_alt in actions:
            if a2_alt != a2:
                u2_alt = payoffs[(a1, a2_alt)][1]
                if u2_alt > u2:
                    best_response_2 = False
                    break
        if best_response_1 and best_response_2:
            nash_equilibria.append((a1, a2))
    return nash_equilibria

if __name__ == "__main__":
    # Ejemplo: juego de coordinación simple
    acciones = ['Cooperate', 'Defect']
    # Payoffs: (fila, columna) -> (u_fila, u_columna)
    pagos = {
        ('Cooperate', 'Cooperate'): (3, 3),
        ('Cooperate', 'Defect'):    (0, 5),
        ('Defect',    'Cooperate'): (5, 0),
        ('Defect',    'Defect'):    (1, 1)
    }

    equilibrios = find_pure_nash(acciones, pagos)
    print("Equilibrios de Nash puros:")
    for eq in equilibrios:
        print(f"  {eq} con pagos {pagos[eq]}")
