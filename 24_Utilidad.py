# Función de utilidad para evaluar una decisión de compra
def utility_purchase(price, quality):
    # Supongamos una función de utilidad que valora la calidad y penaliza el precio
    utility = quality - 0.8 * price
    return utility

# Ejemplo de uso de la función de utilidad para evaluar una decisión de compra
product_price = 50     # Precio del producto en dólares
product_quality = 8    # Calidad percibida del producto en una escala de 1 a 10
decision_utility = utility_purchase(product_price, product_quality)
print("Utilidad de la decision de compra:", decision_utility)