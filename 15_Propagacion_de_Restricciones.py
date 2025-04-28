from collections import deque

class CSP:
    """
    Problema de Satisfacción de Restricciones con propagación AC-3 (Arc-Consistency).
    """
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        # Dominios es dict var -> lista de valores posibles
        self.domains = {v: list(domains[v]) for v in variables}
        # Vecindad: dict var -> lista de variables con las que tiene restricción
        self.neighbors = neighbors
        # constraints(X, x, Y, y) -> True si (X=x, Y=y) cumple la restricción
        self.constraints = constraints

    def revise(self, Xi, Xj):
        """
        Revisa y elimina valores del dominio de Xi que no tienen soporte en Xj.
        Retorna True si se eliminó algún valor.
        """
        revised = False
        for x in self.domains[Xi][:]:
            # Si no existe ningún y en dominio de Xj que satisfaga la restricción
            if not any(self.constraints(Xi, x, Xj, y) for y in self.domains[Xj]):
                self.domains[Xi].remove(x)
                revised = True
        return revised

    def ac3(self):
        """
        Aplica AC-3 para lograr consistencia de arcos en todos los pares.
        Retorna False si algún dominio queda vacío, True si ac3 completó.
        """
        # Cola de arcos (Xi, Xj)
        queue = deque((Xi, Xj) for Xi in self.variables for Xj in self.neighbors[Xi])

        while queue:
            Xi, Xj = queue.popleft()
            if self.revise(Xi, Xj):
                if not self.domains[Xi]:
                    return False
                # Añadir a la cola todos los arcos (Xk, Xi) excepto Xj
                for Xk in self.neighbors[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True

    def is_solved(self):
        """Verifica si todos los dominios están reducidos a un solo valor."""
        return all(len(self.domains[v]) == 1 for v in self.variables)

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
        # Colores diferentes para regiones adyacentes
        return va != vb

    csp = CSP(variables, domains, neighbors, constraint)
    result = csp.ac3()

    if result:
        print("Dominios tras AC-3:")
        for v in variables:
            print(f"  {v}: {csp.domains[v]}")
        if csp.is_solved():
            print("Solución encontrada! Cada variable tiene un único color.")
        else:
            print("AC-3 completado, pero algunos dominios tienen múltiples valores.")
    else:
        print("Dominio vacío detectado - no hay solución.")
