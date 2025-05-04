def conflict_directed_backjumping_n_queens(n):
    """
    Resuelve el problema de las N reinas usando Backjumping (salto atrás por conflicto).
    Retorna lista de filas asignadas a cada columna o None si no hay solución.
    """
    # Variables globales para la función recursiva
    assignment = [None] * n  # Inicializa un arreglo con None, representando que ninguna reina ha sido asignada a las columnas
    domains = [list(range(n)) for _ in range(n)]  # El dominio de cada columna es un rango de filas posibles (0 a n-1)

    def is_consistent(col, row):
        """Comprueba que (col,row) no entra en conflicto con asignaciones previas."""
        for c in range(col):  # Recorre todas las columnas previas a la actual
            r = assignment[c]  # Obtiene la fila asignada en la columna c
            # Verifica si hay conflicto en filas o diagonales
            if r == row or abs(c - col) == abs(r - row):
                return False  # Conflicto si las filas son iguales o están en la misma diagonal
        return True  # No hay conflicto

    def backjump(col):
        # Si todas las columnas están asignadas, hemos encontrado una solución
        if col == n:
            return True, None

        # Mantener el set de variables conflictivas para esta columna
        conflict_set = set()  # Este set guarda las columnas que tienen conflicto con la columna actual

        for row in domains[col]:  # Recorre todas las filas posibles para la columna actual
            if is_consistent(col, row):  # Verifica si no hay conflicto con asignaciones previas
                assignment[col] = row  # Asigna la fila a la columna
                success, conflict = backjump(col + 1)  # Llama recursivamente para la siguiente columna
                if success:
                    return True, None  # Si la recursión fue exitosa, retorna True (solución encontrada)
                
                # Si se encontró un conflicto
                if conflict is not None:
                    if conflict < col:
                        # Si el conflicto está en una columna anterior, podemos intentar otro valor
                        assignment[col] = None  # Desasignamos la columna actual
                        return False, conflict  # Retornamos el conflicto para intentar solucionarlo
                    else:
                        # Si el conflicto está más allá, lo añadimos al conjunto de conflictos
                        conflict_set.add(conflict)
                assignment[col] = None  # Desasigna la columna si el valor no funcionó
            else:
                # Si hay conflicto directo con alguna columna anterior, lo agregamos al conjunto de conflictos
                for c in range(col):  # Recorre las columnas previas
                    r = assignment[c]
                    if r is not None and (r == row or abs(c - col) == abs(r - row)):
                        conflict_set.add(c)  # Agrega la columna a conflict_set

        # Si no hay fila válida para asignar, decidir a qué columna saltar
        if conflict_set:
            # Si el set de conflictos no está vacío, saltamos a la columna más lejana en conflicto
            jump_to = max(conflict_set)  # Elige la columna con el índice más alto
        else:
            # Si no hay conflictos, saltamos a la columna anterior
            jump_to = col - 1

        return False, jump_to  # Retorna el salto hacia la columna con conflicto

    success, _ = backjump(0)  # Llama a la función backjump para empezar desde la primera columna
    return assignment if success else None  # Si la solución es exitosa, retorna la asignación de las reinas, si no, None

if __name__ == "__main__":
    n = 8  # Número de reinas (tablero 8x8)
    solution = conflict_directed_backjumping_n_queens(n)  # Llama a la función para resolver el problema
    if solution:
        print(f"Solución N-Reinas (backjumping): {solution}")
        # Mostrar el tablero con las reinas colocadas
        for r in solution:
            print(''.join('Q' if c == r else '.' for c in range(n)))  # Imprime 'Q' para la reina y '.' para espacios vacíos
    else:
        print("No se encontró solución.")  # Si no hay solución, imprime un mensaje
