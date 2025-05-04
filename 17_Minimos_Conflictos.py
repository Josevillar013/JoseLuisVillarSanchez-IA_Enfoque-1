import random  # Importa el módulo random para elegir valores aleatorios

class CSP:
    """
    Representa un problema de satisfacción de restricciones (CSP) genérico.
    - variables: lista de nombres de variables
    - domains: dict var -> lista de valores posibles
    - neighbors: dict var -> lista de variables con las que tiene restricciones
    - constraints: función(var1, val1, var2, val2) -> bool
    """
    def __init__(self, variables, domains, neighbors, constraints):
        # Inicializa el CSP con las variables, dominios, vecinos y restricciones
        self.variables = variables  # Lista de variables (por ejemplo, las columnas de un tablero de N reinas)
        # Crea un diccionario de dominios, donde para cada variable (columna), se asigna una lista de posibles valores (filas)
        self.domains = {v: list(domains[v]) for v in variables}
        # Los vecinos son un diccionario que mapea cada variable a las otras variables con las que tiene restricciones
        self.neighbors = neighbors
        # La función constraints define las restricciones entre las variables (por ejemplo, no pueden estar en la misma fila o diagonal)
        self.constraints = constraints

    def conflict_count(self, var, val, assignment):
        """
        Cuenta el número de conflictos si var = val dado assignment parcial.
        """
        count = 0  # Inicializa el contador de conflictos en 0
        # Recorre todos los vecinos de la variable actual
        for nbr in self.neighbors[var]:
            # Si el vecino ya está asignado y la asignación actual no satisface la restricción, se cuenta como un conflicto
            if nbr in assignment and not self.constraints(var, val, nbr, assignment[nbr]):
                count += 1
        return count  # Devuelve el número total de conflictos

def min_conflicts(csp, max_steps=10000):
    """
    Algoritmo de Min-Conflicts para CSP.
    Inicia con asignación completa aleatoria y repara iterativamente.
    """
    # Inicialización: asignación completa aleatoria para cada variable
    assignment = {var: random.choice(csp.domains[var]) for var in csp.variables}

    # Itera hasta el número máximo de pasos
    for step in range(max_steps):
        # Detectar las variables que están en conflicto (tienen asignaciones que no cumplen las restricciones)
        conflicted = [v for v in csp.variables
                      if csp.conflict_count(v, assignment[v], assignment) > 0]
        
        # Si no hay conflictos, solución encontrada
        if not conflicted:
            return assignment  # Si no hay conflictos, retorna la asignación como solución

        # Elegir una variable aleatoria que esté en conflicto
        var = random.choice(conflicted)

        # Elegir el valor para la variable que minimiza los conflictos
        domain = csp.domains[var]  # Obtiene los posibles valores (dominio) para la variable
        # Inicializa la lista de valores que minimizan los conflictos y el conteo mínimo de conflictos
        conflict_vals = []
        min_conf = float('inf')  # Usa infinito como valor inicial para encontrar el mínimo

        # Recorre todos los valores del dominio de la variable
        for val in domain:
            count = csp.conflict_count(var, val, assignment)  # Cuenta los conflictos para el valor actual
            # Si el valor actual minimiza los conflictos, lo actualiza
            if count < min_conf:
                min_conf = count
                conflict_vals = [val]
            elif count == min_conf:
                conflict_vals.append(val)  # Si hay empate en el número de conflictos, agrega el valor al conjunto

        # Asigna un valor aleatorio de los que minimizan los conflictos
        assignment[var] = random.choice(conflict_vals)

    # Si se alcanza el número máximo de pasos sin resolver, retorna None
    return None

if __name__ == "__main__":
    # Ejemplo: problema de las N reinas
    n = 8  # Número de reinas y el tamaño del tablero (8x8)
    variables = list(range(n))  # Las variables son las columnas del tablero (0..n-1)
    # El dominio de cada columna es el rango de filas posibles (0..n-1)
    domains = {col: list(range(n)) for col in variables}
    
    # Definimos los vecinos: cada columna tiene como vecinos todas las demás columnas
    neighbors = {col: [c for c in variables if c != col] for col in variables}

    # La función de restricciones para las reinas: no pueden estar en la misma fila ni en la misma diagonal
    def queens_constraint(c1, r1, c2, r2):
        return (r1 != r2) and (abs(c1 - c2) != abs(r1 - r2))

    # Creamos una instancia del problema CSP para las N reinas
    csp = CSP(variables, domains, neighbors, queens_constraint)
    # Llamamos al algoritmo Min-Conflicts con un límite de 10000 pasos
    solution = min_conflicts(csp, max_steps=10000)

    if solution:
        # Si se encuentra una solución, imprimir la asignación de las reinas
        print(f"Solución encontrada para {n}-reinas:")
        # Imprime el tablero con las reinas en las posiciones correspondientes
        for r in range(n):
            line = ''.join('Q' if solution[c] == r else '.' for c in range(n))
            print(line)
    else:
        print("No se encontró solución en el límite de pasos.")  # Si no hay solución, imprimir mensaje
