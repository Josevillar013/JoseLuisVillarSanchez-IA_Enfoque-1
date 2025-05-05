# Función para calcular la utilidad de comprar un producto
def utility_purchase(price, quality):
    # Supongamos una función de utilidad que valora la calidad y penaliza el precio
    utility = quality - 0.8 * price
    return utility

# Definir las opciones de compra y sus características
products = {
    'Product_A': {'price': 50, 'quality': 8},
    'Product_B': {'price': 30, 'quality': 6}
}

# Calcular la utilidad esperada para cada producto
expected_utilities = {}
for product, attributes in products.items():
    expected_utilities[product] = utility_purchase(attributes['price'], attributes['quality'])

# Seleccionar el producto con la mayor utilidad esperada
best_product = max(expected_utilities, key=expected_utilities.get)
print("El mejor producto para comprar es:", best_product)