def conflict_directed_backjumping_n_queens(n):
    """
    Resuelve el problema de las N reinas usando Backjumping (salto atrás por conflicto).
    Retorna lista de filas asignadas a cada columna o None si no hay solución.
    """
    # Variables globales para la función recursiva
    assignment = [None] * n
    domains = [list(range(n)) for _ in range(n)]  # dominio de filas por columna

    def is_consistent(col, row):
        """Comprueba que (col,row) no entra en conflicto con asignaciones previas."""
        for c in range(col):
            r = assignment[c]
            if r == row or abs(c - col) == abs(r - row):
                return False
        return True

    def backjump(col):
        # Si todas las columnas están asignadas, éxito
        if col == n:
            return True, None

        # Mantener el set de variables conflictivas para esta columna
        conflict_set = set()

        for row in domains[col]:
            if is_consistent(col, row):
                assignment[col] = row
                success, conflict = backjump(col + 1)
                if success:
                    return True, None
                # Si conflict es None o mayor, propagar
                if conflict is not None:
                    if conflict < col:
                        # Conflicto en var anterior, podemos intentar otro valor
                        assignment[col] = None
                        return False, conflict
                    else:
                        # El conflicto está más allá, añadir a conflict_set
                        conflict_set.add(conflict)
                assignment[col] = None
            else:
                # Registrar conflicto directo con alguna columna anterior
                for c in range(col):
                    r = assignment[c]
                    if r is not None and (r == row or abs(c - col) == abs(r - row)):
                        conflict_set.add(c)
        # No hay fila válida, decidir a quién saltar
        if conflict_set:
            # Saltar a la columna más lejana en conflicto
            jump_to = max(conflict_set)
        else:
            jump_to = col - 1
        return False, jump_to

    success, _ = backjump(0)
    return assignment if success else None

if __name__ == "__main__":
    n = 8
    solution = conflict_directed_backjumping_n_queens(n)
    if solution:
        print(f"Solución N-Reinas (backjumping): {solution}")
        # Mostrar tablero
        for r in solution:
            print(''.join('Q' if c == r else '.' for c in range(n)))
    else:
        print("No se encontró solución.")
