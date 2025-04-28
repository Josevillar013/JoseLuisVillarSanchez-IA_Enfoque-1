class CSP:
    """
    Clase genérica para resolver Problemas de Satisfacción de Restricciones (CSP) mediante backtracking con Forward Checking y heurística MRV.
    """
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = {v: list(domains[v]) for v in variables}
        self.neighbors = neighbors
        self.constraints = constraints  # función(var1, val1, var2, val2) -> bool

    def assign(self, var, val, assignment):
        assignment[var] = val

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def consistent(self, var, val, assignment):
        """Comprueba que `val` en `var` no viole ninguna restricción con variables ya asignadas."""
        for other in self.neighbors[var]:
            if other in assignment and not self.constraints(var, val, other, assignment[other]):
                return False
        return True

    def forward_check(self, var, val, assignment, removed):
        """Elimina valores inconsistentes de los dominios de los vecinos no asignados."""
        for nbr in self.neighbors[var]:
            if nbr not in assignment:
                for v2 in self.domains[nbr][:]:
                    if not self.constraints(var, val, nbr, v2):
                        self.domains[nbr].remove(v2)
                        removed.setdefault(nbr, []).append(v2)
                if not self.domains[nbr]:
                    return False
        return True

    def select_unassigned_variable(self, assignment):
        """Heurística MRV: elige variable sin asignar con dominio más pequeño."""
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda v: len(self.domains[v]))

    def order_domain_values(self, var, assignment):
        """Devuelve los valores del dominio en orden. (podría implementarse LCV)."""
        return list(self.domains[var])

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            if self.consistent(var, val, assignment):
                self.assign(var, val, assignment)
                removed = {}
                if self.forward_check(var, val, assignment, removed):
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                # Restaurar dominios
                for v, vals in removed.items():
                    self.domains[v].extend(vals)
                self.unassign(var, assignment)
        return None

    def solve(self):
        return self.backtrack({})

# Ejemplo: coloreado de mapa de Australia
if __name__ == "__main__":
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    domains = {v: ['red', 'green', 'blue'] for v in variables}
    neighbors = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'],
        'V': ['SA', 'NSW'],
        'T': []
    }
    def constraint(a, va, b, vb):
        return va != vb

    csp = CSP(variables, domains, neighbors, constraint)
    solution = csp.solve()
    if solution:
        print("Solución encontrada:")
        for region in variables:
            print(f"  {region}: {solution[region]}")
    else:
        print("No existe solución.")
