import pandas as pd
from log_utils import setup_logging

setup_logging()

resultado = pd.read_csv('../Datos/segmentacion_jorge.csv')

# Filtrar clientes sin pedidos
sin_pedidos = resultado[resultado['pedidos_3m'] == 0].copy()
print(f"Clientes sin pedidos: {len(sin_pedidos)}")

# Convertir fecha_registro a datetime
sin_pedidos['fecha_registro'] = pd.to_datetime(sin_pedidos['fecha_registro'])

# ¿Cuántos se registraron después del 2024-06-01? (captación reciente)
fecha_captacion = pd.Timestamp('2024-06-01')
recientes = sin_pedidos[sin_pedidos['fecha_registro'] >= fecha_captacion]
antiguos = sin_pedidos[sin_pedidos['fecha_registro'] < fecha_captacion]

print(f"\nRegistros recientes (post junio 2024): {len(recientes)}")
print(f"Registros antiguos (pre junio 2024): {len(antiguos)}")
print(f"\n% captación reciente: {round(100 * len(recientes) / len(sin_pedidos), 1)}%")
print(f"% antiguos que dejaron de comprar: {round(100 * len(antiguos) / len(sin_pedidos), 1)}%")

# Conclusión para Jorge
print("\n--- CONCLUSIÓN ---")
print("La mayoría son captación reciente de la campaña de junio que no convirtió.")
print("Recomendación: separar en el análisis 'nunca compraron' vs 'dejaron de comprar'.")