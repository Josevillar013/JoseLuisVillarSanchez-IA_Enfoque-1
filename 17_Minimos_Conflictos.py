import random

class CSP:
    """
    Representa un problema de satisfacción de restricciones (CSP) genérico.
    - variables: lista de nombres de variables
    - domains: dict var -> lista de valores posibles
    - neighbors: dict var -> lista de variables con las que tiene restricciones
    - constraints: función(var1, val1, var2, val2) -> bool
    """
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = {v: list(domains[v]) for v in variables}
        self.neighbors = neighbors
        self.constraints = constraints

    def conflict_count(self, var, val, assignment):
        """
        Cuenta el número de conflictos si var = val dado assignment parcial.
        """
        count = 0
        for nbr in self.neighbors[var]:
            if nbr in assignment and not self.constraints(var, val, nbr, assignment[nbr]):
                count += 1
        return count


def min_conflicts(csp, max_steps=10000):
    """
    Algoritmo de Min-Conflicts para CSP.
    Inicia con asignación completa aleatoria y repara iterativamente.
    """
    # Inicialización: asignación completa aleatoria
    assignment = {var: random.choice(csp.domains[var]) for var in csp.variables}

    for step in range(max_steps):
        # Detectar variables en conflicto
        conflicted = [v for v in csp.variables
                      if csp.conflict_count(v, assignment[v], assignment) > 0]
        # Si no hay conflictos, solución encontrada
        if not conflicted:
            return assignment

        # Elegir variable al azar con conflicto
        var = random.choice(conflicted)

        # Elegir valor que minimiza conflictos
        domain = csp.domains[var]
        # Calcular número de conflictos para cada valor
        conflict_vals = []
        min_conf = float('inf')
        for val in domain:
            count = csp.conflict_count(var, val, assignment)
            if count < min_conf:
                min_conf = count
                conflict_vals = [val]
            elif count == min_conf:
                conflict_vals.append(val)

        # Asignar uno de los mejores valores
        assignment[var] = random.choice(conflict_vals)

    # Si se alcanza max_steps sin resolver, devolver None
    return None

if __name__ == "__main__":
    # Ejemplo: problema de las N reinas
    n = 8
    variables = list(range(n))  # columnas 0..n-1
    domains = {col: list(range(n)) for col in variables}  # filas 0..n-1
    # Vecinos: todas las demás columnas
    neighbors = {col: [c for c in variables if c != col] for col in variables}

    def queens_constraint(c1, r1, c2, r2):
        # No en misma fila ni diagonal
        return (r1 != r2) and (abs(c1 - c2) != abs(r1 - r2))

    csp = CSP(variables, domains, neighbors, queens_constraint)
    solution = min_conflicts(csp, max_steps=10000)

    if solution:
        print(f"Solución encontrada para {n}-reinas:")
        # Imprimir tablero
        for r in range(n):
            line = ''.join('Q' if solution[c] == r else '.' for c in range(n))
            print(line)
    else:
        print("No se encontró solución en el límite de pasos.")
