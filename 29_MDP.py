# Definir las acciones y sus recompensas y probabilidades de transición
actions = {
    'Turn_Left': {'reward': -1, 'transition_probs': {'Go_Straight': 0.1, 'Turn_Right': 0.9}},
    'Go_Straight': {'reward': -2, 'transition_probs': {'Go_Straight': 0.8, 'Turn_Right': 0.1, 'Turn_Left': 0.1}},
    'Turn_Right': {'reward': -1, 'transition_probs': {'Go_Straight': 0.1, 'Turn_Left': 0.9}}
}

# Definir la función de utilidad
def utility(state):
    if state == 'Destination':
        return 100
    else:
        return 0

# Definir el algoritmo de iteración de políticas
def policy_iteration_MDP():
    # Inicializar la política
    policy = {'Intersection_1': 'Turn_Left', 'Intersection_2': 'Go_Straight', 'Intersection_3': 'Turn_Right'}
    # Número máximo de iteraciones
    max_iterations = 100
    # Tasa de descuento
    gamma = 0.9

    # Iterar hasta que se alcance el número máximo de iteraciones o converja
    for _ in range(max_iterations):
        new_policy = {}
        for state in policy:
            action = policy[state]
            expected_value = actions[action]['reward'] + \
                             gamma * sum(actions[action]['transition_probs'][next_state] * utility(next_state) for next_state in actions[action]['transition_probs'])
            new_policy[state] = max(actions, key=lambda a: sum(actions[a]['transition_probs'][next_state] * utility(next_state) for next_state in actions[a]['transition_probs']))

        # Si la política no cambia, hemos convergido
        if new_policy == policy:
            break
        policy = new_policy

    return policy

# Ejecutar la iteración de políticas para el MDP
optimal_policy = policy_iteration_MDP()
print("La política optima es:", optimal_policy)