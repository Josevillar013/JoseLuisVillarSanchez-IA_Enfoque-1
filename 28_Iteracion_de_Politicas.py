# Definir las acciones y sus recompensas y probabilidades de éxito
actions = {
    'Action_A': {'reward': 10, 'success_prob': 0.8},
    'Action_B': {'reward': 20, 'success_prob': 0.5}
}

# Inicializar la política
policy = {'Action_A': 0.5, 'Action_B': 0.5}
# Número máximo de iteraciones
max_iterations = 100
# Tasa de descuento
gamma = 0.9

# Realizar la iteración de políticas
for _ in range(max_iterations):
    new_policy = {}
    for action, details in actions.items():
        # Calcular el valor esperado de cada acción
        expected_value = details['reward'] + gamma * details['success_prob'] * policy['Action_A'] + \
                        gamma * (1 - details['success_prob']) * policy['Action_B']
        new_policy[action] = expected_value
    
    # Normalizar la nueva política
    total = sum(new_policy.values())
    for action in new_policy:
        new_policy[action] /= total
    
    policy = new_policy

# Determinar la mejor acción basada en la política final
best_action = max(policy, key=policy.get)
print("La mejor accion es:", best_action)