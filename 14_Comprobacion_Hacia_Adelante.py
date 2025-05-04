def forward_checking_n_queens(n):
    """
    Resuelve el problema de las N reinas usando backtracking con Forward Checking.
    - n: número de reinas (y también el tamaño del tablero).
    """
    # Inicializar el dominio de cada columna: para cada columna, las filas posibles son 0 a n-1
    domains = {col: list(range(n)) for col in range(n)}
    assignment = {}  # Diccionario para almacenar la asignación de filas por columna (columna -> fila asignada)

    def is_consistent(col, row):
        """Comprueba que la asignación de (col, row) no entre en conflicto con ninguna reina ya asignada."""
        for c, r in assignment.items():
            # Verifica si hay conflicto en la misma fila o en la misma diagonal
            if r == row or abs(c - col) == abs(r - row):
                return False
        return True

    def forward_check(col, row, local_domains):
        """
        Realiza Forward Checking eliminando de los dominios de columnas futuras
        aquellos valores que entrarían en conflicto con (col, row).
        - col: columna actual.
        - row: fila de la reina en la columna actual.
        - local_domains: copia del dominio de todas las columnas.
        Retorna False si alguna columna futura no tiene valores posibles, True si no hay conflicto.
        """
        for c in range(col + 1, n):  # Iteramos por las columnas a la derecha de la columna actual
            new_domain = []  # Nueva lista de valores posibles para la columna c
            for r in local_domains[c]:
                # Mantener solo filas que no estén en la misma fila ni en la misma diagonal
                if r != row and abs(c - col) != abs(r - row):
                    new_domain.append(r)
            # Si no quedan valores válidos en el dominio de la columna c, retorna False
            if not new_domain:
                return False
            local_domains[c] = new_domain  # Actualiza el dominio de la columna c
        return True

    def backtrack(col, domains):
        """
        Función recursiva que realiza el backtracking para intentar encontrar una solución.
        - col: columna actual que estamos tratando de asignar una reina.
        - domains: los dominios de todas las columnas (que pueden ser modificados durante el proceso).
        """
        # Caso base: Si hemos asignado una reina a todas las columnas (col == n), hemos encontrado una solución
        if col == n:
            return True

        # Intentamos asignar una fila a la reina de la columna `col`
        for row in domains[col][:]:  # Recorre el dominio de la columna actual (hacemos una copia con [:])
            if is_consistent(col, row):  # Verifica si la asignación es consistente
                # Si es consistente, asignamos la fila al dominio de la columna
                assignment[col] = row
                # Hacemos una copia de los dominios actuales para continuar con el forward checking
                local_domains = {c: list(domains[c]) for c in domains}
                # Realizamos Forward Checking: eliminamos valores inconsistentes de los dominios futuros
                if forward_check(col, row, local_domains):
                    # Si no hay conflictos, intentamos asignar una reina a la siguiente columna
                    if backtrack(col + 1, local_domains):
                        return True
                # Si no encontramos solución, desasignamos la reina de la columna `col`
                del assignment[col]
        return False  # Si no encontramos ninguna solución, retornamos False

    # Comenzamos el backtracking desde la columna 0 con el dominio inicial
    if backtrack(0, domains):
        # Si encontramos una solución, retornamos la lista de posiciones de las reinas (una por columna)
        return [assignment[c] for c in range(n)]
    else:
        # Si no hay solución, retornamos None
        return None

# Bloque principal donde ejecutamos la función
if __name__ == "__main__":
    n = 8  # Número de reinas y tamaño del tablero
    solution = forward_checking_n_queens(n)
    if solution:
        # Si encontramos una solución, imprimimos las posiciones de las reinas (fila por columna)
        print(f"Solución para {n}-reinas (fila por columna): {solution}")
        # Mostrar el tablero con las reinas colocadas
        for r in solution:
            print(''.join('Q' if c == r else '.' for c in range(n)))
    else:
        print("No hay solución.")  # Si no se encuentra solución, mostramos este mensaje
