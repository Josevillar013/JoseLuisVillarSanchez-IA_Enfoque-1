import random  # Importa el módulo random para generar el estado inicial aleatorio

def hill_climbing(objective, neighbors, initial_state, max_iterations=1000):
    """
    Algoritmo de Hill Climbing (ascenso por colinas):
    - objective: función objetivo que se quiere maximizar.
    - neighbors: función que genera los vecinos de un estado dado.
    - initial_state: el estado desde el que se inicia la búsqueda.
    - max_iterations: tope de iteraciones para evitar bucles infinitos.
    Retorna el mejor estado encontrado junto con su valor.
    """
    current = initial_state                      # Estado actual comienza desde el inicial
    current_value = objective(current)           # Evalúa el valor del estado actual

    for i in range(max_iterations):              # Bucle de iteraciones controlado por el máximo
        nbrs = neighbors(current)                # Genera la lista de vecinos del estado actual

        best_neighbor = None                     # Inicializa el mejor vecino
        best_value = current_value               # El mejor valor empieza siendo el actual

        # Itera sobre los vecinos para encontrar el de mayor valor
        for n in nbrs:
            val = objective(n)                   # Evalúa el valor del vecino
            if val > best_value:                 # Si mejora el valor actual, actualiza mejor vecino
                best_value = val
                best_neighbor = n

        if best_neighbor is None:                # Si no hay mejora, se alcanzó un máximo local
            break

        current = best_neighbor                  # Se mueve al mejor vecino
        current_value = best_value               # Actualiza el valor actual

    return current, current_value                # Retorna el mejor estado encontrado

# BLOQUE PRINCIPAL
if __name__ == "__main__":
    # Función objetivo: f(x) = -(x-3)^2 + 10 → tiene un máximo en x=3
    def f(x):
        return -(x - 3)**2 + 10

    # Función de vecinos: genera dos vecinos (x-1 y x+1)
    def gen_neighbors(x):
        return [x - 1, x + 1]

    # Estado inicial aleatorio entre -10 y 10
    init = random.randint(-10, 10)

    # Ejecuta la búsqueda por colinas con hasta 100 iteraciones
    best_state, best_val = hill_climbing(f, gen_neighbors, init, max_iterations=100)

    # Muestra los resultados
    print(f"Estado inicial: {init}")
    print(f"Mejor estado encontrado: {best_state} con valor {best_val}")
