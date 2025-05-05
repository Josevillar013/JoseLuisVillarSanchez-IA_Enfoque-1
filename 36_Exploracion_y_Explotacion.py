import numpy as np

# Definir una función para el decaimiento de ε
def decay_epsilon(initial_epsilon, episode, decay_rate):
    return initial_epsilon * (1 / (1 + decay_rate * episode))

# Ejemplo de uso:
initial_epsilon = 0.5  # Probabilidad inicial de exploración
decay_rate = 0.1  # Tasa de decaimiento
episode = 10  # Número de episodio actual
epsilon = decay_epsilon(initial_epsilon, episode, decay_rate)
print("Probabilidad de exploracion para el episodio", episode, ":", epsilon)