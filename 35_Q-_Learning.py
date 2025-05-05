import numpy as np

# Definir el entorno del laberinto (matriz de recompensas)
R = np.array([[-1, -1, -1, -1, 0, -1],
              [-1, -1, -1, 0, -1, 100],
              [-1, -1, -1, 0, -1, -1],
              [-1, 0, 0, -1, 0, -1],
              [0, -1, -1, 0, -1, 100],
              [-1, 0, -1, -1, 0, 100]])

# Inicializar la tabla Q con ceros
Q = np.zeros_like(R)

# Definir hiperparámetros
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento

# Ejecutar el algoritmo Q-Learning
num_episodes = 1000
for _ in range(num_episodes):
    state = np.random.randint(0, 6)  # Seleccionar un estado inicial aleatorio
    while state != 5:  # Hasta que llegue al estado objetivo
        # Elegir una acción aleatoria
        action = np.random.choice(np.where(R[state] >= 0)[0])
        
        # Obtener el próximo estado y la recompensa
        next_state = action
        reward = R[state, action]
        
        # Actualizar la tabla Q utilizando la ecuación de Q-Learning
        Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        
        # Actualizar el estado actual al próximo estado
        state = next_state

# Imprimir la tabla Q después del entrenamiento
print("Tabla Q después del entrenamiento:")
print(Q)