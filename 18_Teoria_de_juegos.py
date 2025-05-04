def find_pure_nash(actions, payoffs):
    """
    Encuentra los equilibrios de Nash puros en un juego normal de dos jugadores.
    - actions: lista de acciones para cada jugador, p.ej. ['A', 'B'].
    - payoffs: diccionario que mapea (a1, a2) -> (u1, u2).
    Retorna lista de tuplas (a1, a2) que son equilibrios de Nash.
    """
    # Se inicializa la lista que almacenará los equilibrios de Nash puros encontrados
    nash_equilibria = []
    
    # Se recorre cada combinación de acciones posibles (a1, a2) y sus pagos asociados (u1, u2)
    for (a1, a2), (u1, u2) in payoffs.items():
        # Verificar si (a1, a2) es un equilibrio de Nash puro
        # Jugador 1 revisa si tiene alguna mejor respuesta a la acción a2
        best_response_1 = True  # Asumimos que a1 es la mejor respuesta por defecto
        for a1_alt in actions:
            if a1_alt != a1:  # Compara a1 con cada acción alternativa de jugador 1
                u1_alt = payoffs[(a1_alt, a2)][0]  # Obtiene el pago del jugador 1 si escoge la acción alternativa
                if u1_alt > u1:  # Si alguna alternativa le da un mayor pago, no es la mejor respuesta
                    best_response_1 = False
                    break  # No es un equilibrio de Nash, se rompe el ciclo
        # Jugador 2 revisa si tiene alguna mejor respuesta a la acción a1
        best_response_2 = True  # Asumimos que a2 es la mejor respuesta por defecto
        for a2_alt in actions:
            if a2_alt != a2:  # Compara a2 con cada acción alternativa de jugador 2
                u2_alt = payoffs[(a1, a2_alt)][1]  # Obtiene el pago del jugador 2 si escoge la acción alternativa
                if u2_alt > u2:  # Si alguna alternativa le da un mayor pago, no es la mejor respuesta
                    best_response_2 = False
                    break  # No es un equilibrio de Nash, se rompe el ciclo
        # Si ambos jugadores están eligiendo sus mejores respuestas, entonces (a1, a2) es un equilibrio de Nash
        if best_response_1 and best_response_2:
            nash_equilibria.append((a1, a2))  # Se añade el equilibrio a la lista
    
    return nash_equilibria  # Retorna la lista de equilibrios de Nash puros

if __name__ == "__main__":
    # Ejemplo: juego de coordinación simple
    acciones = ['Cooperate', 'Defect']  # Las acciones posibles para los dos jugadores
    # Payoffs: (fila, columna) -> (u_fila, u_columna)
    pagos = {
        ('Cooperate', 'Cooperate'): (3, 3),  # Ambos cooperan, ambos reciben 3
        ('Cooperate', 'Defect'):    (0, 5),  # Jugador 1 coopera y jugador 2 defecta
        ('Defect',    'Cooperate'): (5, 0),  # Jugador 1 defecta y jugador 2 coopera
        ('Defect',    'Defect'):    (1, 1)   # Ambos defectan
    }

    # Llamada a la función para encontrar los equilibrios de Nash puros
    equilibrios = find_pure_nash(acciones, pagos)
    
    # Imprimir los equilibrios encontrados
    print("Equilibrios de Nash puros:")
    for eq in equilibrios:
        print(f"  {eq} con pagos {pagos[eq]}")
