import random

def hill_climbing(objective, neighbors, initial_state, max_iterations=1000):
    """
    Algoritmo de búsqueda por colinas (Hill Climbing):
    - objective: función que toma un estado y devuelve su valor (a maximizar).
    - neighbors: función que toma un estado y devuelve una lista de estados vecinos.
    - initial_state: estado inicial para comenzar la búsqueda.
    - max_iterations: número máximo de iteraciones.
    Retorna el mejor estado encontrado y su valor.
    """
    current = initial_state
    current_value = objective(current)

    for i in range(max_iterations):
        # Generar vecinos del estado actual
        nbrs = neighbors(current)
        # Evaluar valores de vecinos
        best_neighbor = None
        best_value = current_value
        for n in nbrs:
            val = objective(n)
            if val > best_value:
                best_value = val
                best_neighbor = n

        # Si no hay mejora, terminamos
        if best_neighbor is None:
            break

        # Moverse a la mejor vecindad
        current = best_neighbor
        current_value = best_value

    return current, current_value

if __name__ == "__main__":
    # Ejemplo: maximizar f(x) = -(x-3)^2 + 10
    def f(x):
        return -(x - 3)**2 + 10

    def gen_neighbors(x):
        # Vecinos: x-1, x+1
        return [x - 1, x + 1]

    # Estado inicial aleatorio entre -10 y 10
    init = random.randint(-10, 10)
    best_state, best_val = hill_climbing(f, gen_neighbors, init, max_iterations=100)

    print(f"Estado inicial: {init}")
    print(f"Mejor estado encontrado: {best_state} con valor {best_val}")
