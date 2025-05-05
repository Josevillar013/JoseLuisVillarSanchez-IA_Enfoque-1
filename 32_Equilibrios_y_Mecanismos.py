# Definir una lista de ofertas de los jugadores
bids = [10, 20, 15, 25, 30]

# Ordenar las ofertas de mayor a menor
sorted_bids = sorted(bids, reverse=True)

# El ganador de la subasta es el jugador con la segunda oferta más alta
winner_price = sorted_bids[1] if len(sorted_bids) > 1 else sorted_bids[0]

print("El precio pagado por el ganador es:", winner_price)