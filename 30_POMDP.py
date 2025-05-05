# Definir las acciones disponibles para el sistema de navegación
actions = ['Go_Straight', 'Turn_Left', 'Turn_Right']

# Definir los estados (ubicaciones en la ciudad) y las observaciones posibles (niveles de tráfico)
states = ['Location_A', 'Location_B', 'Location_C']
observations = ['Low_Traffic', 'High_Traffic']

# Definir las probabilidades de transición del estado
transition_probabilities = {
    'Location_A': {'Go_Straight': {'Location_A': 0.8, 'Location_B': 0.2}, 'Turn_Left': {'Location_B': 0.8, 'Location_A': 0.2}},
    'Location_B': {'Go_Straight': {'Location_B': 0.5, 'Location_C': 0.5}, 'Turn_Left': {'Location_C': 0.8, 'Location_B': 0.2}},
    'Location_C': {'Go_Straight': {'Location_C': 0.8, 'Location_B': 0.2}, 'Turn_Right': {'Location_B': 0.8, 'Location_C': 0.2}}
}

# Definir las probabilidades de observación
observation_probabilities = {
    'Location_A': {'Low_Traffic': {'Location_A': 0.8, 'Location_B': 0.2}, 'High_Traffic': {'Location_A': 0.2, 'Location_B': 0.8}},
    'Location_B': {'Low_Traffic': {'Location_B': 0.8, 'Location_C': 0.2}, 'High_Traffic': {'Location_B': 0.2, 'Location_C': 0.8}},
    'Location_C': {'Low_Traffic': {'Location_C': 0.8, 'Location_B': 0.2}, 'High_Traffic': {'Location_C': 0.2, 'Location_B': 0.8}}
}

# Definir las recompensas por estado
rewards = {'Location_C': 100, 'Location_A': -10, 'Location_B': -10}

# Definir la función de utilidad
def utility(state):
    return rewards.get(state, 0)

# Definir la función de utilidad observada
def observed_utility(state, observation):
    return rewards.get(state, 0) if observation == 'Low_Traffic' else 0

# Definir la función de transición
def transition(state, action):
    return np.random.choice(list(transition_probabilities[state][action].keys()), 
                             p=list(transition_probabilities[state][action].values()))

# Definir la función de observación
def observe(state, action):
    return np.random.choice(list(observation_probabilities[state][action].keys()), 
                             p=list(observation_probabilities[state][action].values()))

# Implementar el algoritmo de búsqueda en profundidad (DFS) para encontrar la ruta óptima
def dfs(state, path):
    if state == 'Location_C':
        return path
    for action in actions:
        next_state = transition(state, action)
        path.append(action)
        observed = observe(next_state, action)
        if observed == 'Low_Traffic':
            return dfs(next_state, path)
        path.pop()
    return path

# Ejecutar el algoritmo de búsqueda en profundidad (DFS) desde la ubicación inicial
initial_state = 'Location_A'
optimal_path = dfs(initial_state, [initial_state])
print("La ruta optima planificada por el sistema de navegacion es:", optimal_path)