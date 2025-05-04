from collections import deque

class CSP:
    """
    Problema de Satisfacción de Restricciones con propagación AC-3 (Arc-Consistency).
    """
    def __init__(self, variables, domains, neighbors, constraints):
        """
        Inicializa el problema CSP con las variables, dominios, vecinos y restricciones.
        """
        self.variables = variables
        # Dominios es un diccionario que mapea cada variable a su lista de valores posibles.
        self.domains = {v: list(domains[v]) for v in variables}
        # Vecindad es un diccionario que mapea cada variable a una lista de sus variables vecinas.
        self.neighbors = neighbors
        # constraints es una función que verifica si una asignación (X=x, Y=y) cumple las restricciones entre dos variables.
        self.constraints = constraints

    def revise(self, Xi, Xj):
        """
        Revisa y elimina valores del dominio de Xi que no tienen soporte en Xj.
        Retorna True si se eliminó algún valor.
        """
        revised = False
        # Recorre todos los valores del dominio de Xi
        for x in self.domains[Xi][:]:  # Usamos [:] para hacer una copia y evitar modificar la lista mientras iteramos
            # Si no existe ningún valor y en el dominio de Xj que satisfaga la restricción entre (Xi, x) y (Xj, y)
            if not any(self.constraints(Xi, x, Xj, y) for y in self.domains[Xj]):
                # Si no se encontró ningún valor válido, eliminamos x del dominio de Xi
                self.domains[Xi].remove(x)
                revised = True
        return revised

    def ac3(self):
        """
        Aplica el algoritmo AC-3 para lograr consistencia de arcos en todos los pares de variables.
        Retorna False si algún dominio queda vacío, True si AC-3 completó exitosamente.
        """
        # Cola de arcos (Xi, Xj), donde Xi es una variable y Xj es su vecino
        queue = deque((Xi, Xj) for Xi in self.variables for Xj in self.neighbors[Xi])

        # Procesamos la cola mientras haya arcos por revisar
        while queue:
            Xi, Xj = queue.popleft()  # Extraemos el siguiente arco (Xi, Xj)
            # Si se han eliminado valores en el dominio de Xi, revisamos los arcos relacionados con Xi
            if self.revise(Xi, Xj):
                # Si el dominio de Xi queda vacío, no se puede continuar con el algoritmo (no hay solución)
                if not self.domains[Xi]:
                    return False
                # Añadimos los arcos relacionados con Xi a la cola, excepto el arco hacia Xj
                for Xk in self.neighbors[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))  # Agregamos el arco (Xk, Xi) para revisar su consistencia
        return True

    def is_solved(self):
        """
        Verifica si todos los dominios están reducidos a un solo valor.
        Esto indica que se ha encontrado una solución válida.
        """
        return all(len(self.domains[v]) == 1 for v in self.variables)  # Comprueba que cada variable tiene un único valor

# Ejemplo: coloreado de mapa de Australia
if __name__ == "__main__":
    # Definimos las variables del problema (las regiones del mapa de Australia)
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    
    # Definimos los dominios posibles para cada variable (los colores que pueden tener las regiones)
    domains = {v: ['red', 'green', 'blue'] for v in variables}
    
    # Definimos los vecinos de cada región (regiones adyacentes que no pueden tener el mismo color)
    neighbors = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'],
        'V': ['SA', 'NSW'],
        'T': []
    }
    
    # Definimos la función de restricción: dos regiones no pueden tener el mismo color
    def constraint(a, va, b, vb):
        return va != vb  # Retorna True si los colores son diferentes

    # Creamos una instancia de CSP con las variables, dominios, vecinos y restricciones
    csp = CSP(variables, domains, neighbors, constraint)
    
    # Aplicamos el algoritmo AC-3 para lograr consistencia de arcos
    result = csp.ac3()

    # Si AC-3 fue exitoso, mostramos los dominios de las variables
    if result:
        print("Dominios tras AC-3:")
        for v in variables:
            print(f"  {v}: {csp.domains[v]}")  # Imprimimos el dominio de cada variable

        # Verificamos si la solución está completa (todos los dominios reducidos a un solo valor)
        if csp.is_solved():
            print("Solución encontrada! Cada variable tiene un único color.")
        else:
            print("AC-3 completado, pero algunos dominios tienen múltiples valores.")
    else:
        # Si algún dominio quedó vacío, no hay solución posible
        print("Dominio vacío detectado - no hay solución.")
