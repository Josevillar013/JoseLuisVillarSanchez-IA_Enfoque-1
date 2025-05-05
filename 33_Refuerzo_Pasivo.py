import numpy as np

# Definir el conjunto de datos de acciones aleatorias (estado, acción, recompensa)
data = [
    ((0, 0), 'Up', -1),
    ((0, 1), 'Left', -1),
    ((1, 1), 'Down', 1),
    # Más ejemplos de acciones aleatorias...
]

# Inicializar la tabla de valores de estado
V = np.zeros((2, 2))

# Actualizar la tabla de valores de estado con los ejemplos de acciones aleatorias
for state, action, reward in data:
    row, col = state
    V[row, col] += reward

# Mostrar la tabla de valores de estado actualizada
print("Tabla de valores de estado actualizada:")
print(V)