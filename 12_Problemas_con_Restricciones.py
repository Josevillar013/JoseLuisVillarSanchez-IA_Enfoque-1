class CSP:
    """
    Clase genérica para resolver Problemas de Satisfacción de Restricciones (CSP) mediante backtracking
    con Forward Checking y heurística MRV (Minimum Remaining Values).
    """
    def __init__(self, variables, domains, neighbors, constraints):
        """
        Inicializa un problema CSP.
        - `variables`: Lista de variables del CSP (por ejemplo, regiones a colorear).
        - `domains`: Diccionario donde cada variable tiene un dominio de valores posibles.
        - `neighbors`: Diccionario de vecinos de cada variable (es decir, variables que están conectadas entre sí).
        - `constraints`: Función que determina si una asignación de valores a dos variables es válida.
        """
        self.variables = variables  # Lista de todas las variables del CSP.
        # Crea una copia de los dominios de cada variable, asegurando que los valores de cada dominio sean listas.
        self.domains = {v: list(domains[v]) for v in variables}
        self.neighbors = neighbors  # Diccionario de vecinos de cada variable.
        self.constraints = constraints  # Función que define las restricciones entre dos variables.

    def assign(self, var, val, assignment):
        """Asigna un valor `val` a la variable `var` en el diccionario `assignment`."""
        assignment[var] = val

    def unassign(self, var, assignment):
        """Elimina la asignación de la variable `var` en el diccionario `assignment`."""
        if var in assignment:
            del assignment[var]

    def consistent(self, var, val, assignment):
        """
        Comprueba si la asignación de `val` a la variable `var` es consistente con las restricciones 
        del problema, es decir, que no viole ninguna restricción con las variables ya asignadas.
        """
        # Revisa las variables vecinas de `var` para ver si alguna tiene una asignación incompatible.
        for other in self.neighbors[var]:
            if other in assignment and not self.constraints(var, val, other, assignment[other]):
                return False
        return True

    def forward_check(self, var, val, assignment, removed):
        """
        Realiza un Forward Checking: elimina valores inconsistentes de los dominios de los vecinos
        no asignados de `var` y actualiza el diccionario `removed` con los valores eliminados.
        """
        # Para cada vecino no asignado de `var`, verifica si alguna de sus posibles asignaciones
        # es inconsistente con la asignación actual.
        for nbr in self.neighbors[var]:
            if nbr not in assignment:
                for v2 in self.domains[nbr][:]:  # Hacemos una copia para evitar modificar la lista mientras iteramos.
                    if not self.constraints(var, val, nbr, v2):
                        self.domains[nbr].remove(v2)  # Elimina el valor inconsistente.
                        removed.setdefault(nbr, []).append(v2)  # Guarda los valores eliminados en `removed`.
                # Si el dominio de algún vecino queda vacío, significa que no hay soluciones posibles.
                if not self.domains[nbr]:
                    return False
        return True

    def select_unassigned_variable(self, assignment):
        """
        Heurística MRV (Minimum Remaining Values): selecciona la variable sin asignar con el dominio más pequeño.
        """
        # Encuentra las variables que aún no están asignadas.
        unassigned = [v for v in self.variables if v not in assignment]
        # Devuelve la variable con el dominio más pequeño (menor número de valores posibles).
        return min(unassigned, key=lambda v: len(self.domains[v]))

    def order_domain_values(self, var, assignment):
        """
        Ordena los valores del dominio de una variable `var` (en este caso se podrían usar otras heurísticas,
        como el Least Constraining Value, pero se devuelve el dominio tal cual aquí).
        """
        # Simplemente devuelve los valores del dominio de `var`.
        return list(self.domains[var])

    def backtrack(self, assignment):
        """
        Función principal de backtracking que intenta asignar valores a las variables de acuerdo con las restricciones.
        """
        # Si todas las variables están asignadas, hemos encontrado una solución.
        if len(assignment) == len(self.variables):
            return assignment

        # Selecciona una variable sin asignar utilizando la heurística MRV.
        var = self.select_unassigned_variable(assignment)

        # Recorre los valores del dominio de `var` en orden.
        for val in self.order_domain_values(var, assignment):
            # Verifica si la asignación de `val` a `var` es consistente con las restricciones.
            if self.consistent(var, val, assignment):
                self.assign(var, val, assignment)  # Asigna el valor a la variable en el diccionario.
                removed = {}  # Diccionario para almacenar valores eliminados durante Forward Checking.

                # Realiza Forward Checking, y si no se encuentran inconsistencias, sigue con el backtracking.
                if self.forward_check(var, val, assignment, removed):
                    result = self.backtrack(assignment)  # Llamada recursiva para asignar el siguiente valor.
                    if result is not None:  # Si se encontró una solución, la devuelve.
                        return result

                # Si no se encontró solución, restaura los dominios eliminados por Forward Checking.
                for v, vals in removed.items():
                    self.domains[v].extend(vals)

                self.unassign(var, assignment)  # Desasigna la variable y prueba con el siguiente valor.

        return None  # Si no se encuentra solución, retorna None.

    def solve(self):
        """Inicia el proceso de resolución utilizando backtracking."""
        return self.backtrack({})  # Inicia con un diccionario vacío para las asignaciones.

# Ejemplo: coloreado de mapa de Australia (un problema CSP típico).
if __name__ == "__main__":
    # Variables: las regiones de Australia.
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    
    # Dominios: cada región puede ser de color 'rojo', 'verde' o 'azul'.
    domains = {v: ['red', 'green', 'blue'] for v in variables}
    
    # Vecinos: regiones que comparten frontera.
    neighbors = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'],
        'V': ['SA', 'NSW'],
        'T': []
    }

    # Restricción: dos regiones no pueden tener el mismo color.
    def constraint(a, va, b, vb):
        return va != vb  # La restricción es que los colores de dos regiones vecinas deben ser diferentes.

    # Crear una instancia del problema CSP con las variables, dominios, vecinos y restricciones.
    csp = CSP(variables, domains, neighbors, constraint)
    
    # Intentar resolver el problema CSP.
    solution = csp.solve()
    
    # Si se encuentra una solución, imprimir los colores asignados a cada región.
    if solution:
        print("Solución encontrada:")
        for region in variables:
            print(f"  {region}: {solution[region]}")
    else:
        print("No existe solución.")  # Si no se encuentra solución, indicar que no es posible.
