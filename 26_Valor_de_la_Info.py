# Función para calcular la utilidad de comprar un producto
def utility_purchase(price, quality):
    # Supongamos una función de utilidad que valora la calidad y penaliza el precio
    utility = quality - 0.8 * price
    return utility

# Valor esperado de la compra sin información adicional
expected_utility_no_info = utility_purchase(50, 8)

# Valor esperado de la compra con información adicional sobre la calidad percibida del producto
expected_utility_with_info = utility_purchase(50, 9)

# Calcular el valor de la información
value_of_information = expected_utility_with_info - expected_utility_no_info
print("El valor de la informacion es:", value_of_information)