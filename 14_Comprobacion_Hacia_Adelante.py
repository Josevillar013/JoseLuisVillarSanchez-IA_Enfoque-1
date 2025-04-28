def forward_checking_n_queens(n):
    """
    Resuelve el problema de las N reinas usando backtracking con Forward Checking.
    """
    # Dominio inicial: para cada columna, las filas posibles
    domains = {col: list(range(n)) for col in range(n)}
    assignment = {}  # columna -> fila asignada

    def is_consistent(col, row):
        """Comprueba que (col, row) no ataque a ninguna reina asignada."""
        for c, r in assignment.items():
            if r == row or abs(c - col) == abs(r - row):
                return False
        return True

    def forward_check(col, row, local_domains):
        """
        Realiza Forward Checking eliminando de los dominios de columnas futuras
        aquellos valores que entrarían en conflicto con (col,row).
        """
        for c in range(col + 1, n):
            new_domain = []
            for r in local_domains[c]:
                # Mantener solo filas no atacadas
                if r != row and abs(c - col) != abs(r - row):
                    new_domain.append(r)
            if not new_domain:
                return False
            local_domains[c] = new_domain
        return True

    def backtrack(col, domains):
        # Si todas las columnas asignadas, solución encontrada
        if col == n:
            return True

        for row in domains[col][:]:  # copia dominio actual
            if is_consistent(col, row):
                # Asignar
                assignment[col] = row
                # Copiar dominios para experimentar
                local_domains = {c: list(domains[c]) for c in domains}
                # Forward Checking
                if forward_check(col, row, local_domains):
                    # Continuar con la siguiente columna
                    if backtrack(col + 1, local_domains):
                        return True
                # Desasignar
                del assignment[col]
        return False

    if backtrack(0, domains):
        # Devolver lista de posiciones de reinas (fila por columna)
        return [assignment[c] for c in range(n)]
    else:
        return None

if __name__ == "__main__":
    n = 8
    solution = forward_checking_n_queens(n)
    if solution:
        print(f"Solución para {n}-reinas (fila por columna): {solution}")
        # Mostrar tablero
        for r in solution:
            print(''.join('Q' if c == r else '.' for c in range(n)))
    else:
        print("No hay solución.")
