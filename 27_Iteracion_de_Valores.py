# Definir las acciones y sus recompensas y probabilidades de éxito
actions = {
    'Action_A': {'reward': 10, 'success_prob': 0.8},
    'Action_B': {'reward': 20, 'success_prob': 0.5}
}

# Número máximo de iteraciones
max_iterations = 100
# Tasa de descuento
gamma = 0.9

# Inicializar los valores de las acciones
values = {'Action_A': 0, 'Action_B': 0}

# Realizar la iteración de valores
for _ in range(max_iterations):
    for action, details in actions.items():
        expected_value = details['reward'] + gamma * (details['success_prob'] * values['Action_A'] + \
                                                      (1 - details['success_prob']) * values['Action_B'])
        values[action] = expected_value

# Determinar la mejor acción basada en los valores finales
best_action = max(values, key=values.get)
print("La mejor accion es:", best_action)