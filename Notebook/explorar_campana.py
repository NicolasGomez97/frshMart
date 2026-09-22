#explorar_campana.py — Tu primer script en FreshMart
import pandas as pd

# Cargar los 3 archivos de María
clientes = pd.read_csv('datos/campana_verano_clientes.csv')
ventas = pd.read_csv('datos/campana_verano_ventas.csv')
productos = pd.read_csv('datos/productos_promo_verano.csv')

print("=" * 60)
print("CLIENTES DE LA CAMPAÑA")
print("=" * 60)
print(f"Filas: {len(clientes):,}")
print(f"Columnas: {list(clientes.columns)}")
print()
print(clientes.info())
print()
print(clientes.head())
print()
print("Nulos por columna:")
print(clientes.isnull().sum())
print()
print(f"IDs únicos: {clientes['cliente_id'].nunique():,}")
print(f"IDs totales: {len(clientes):,}")
print(f"→ Posibles duplicados: {len(clientes) - clientes['cliente_id'].nunique():,}")