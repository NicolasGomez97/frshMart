# Comparar esquemas: verano vs primavera
import pandas as pd
from log_utils import setup_logging

setup_logging()

verano = pd.read_csv('../Datos/campana_verano_ventas.csv', nrows=3)
primavera = pd.read_csv('../Datos/campana_primavera_ventas.csv', nrows=3)

print("Columnas VERANO:", list(verano.columns))
# ['venta_id', 'cliente_id', 'producto_id', 'fecha_compra',
#  'cantidad', 'precio', 'descuento_pct', 'tienda_id', 'campana']

print("Columnas PRIMAVERA:", list(primavera.columns))
# ['id_transaccion', 'id_cliente', 'id_producto', 'fecha_venta',
#  'unidades', 'importe', 'descuento', 'almacen', 'promocion']

print("\n→ Mismo concepto, nombres diferentes. Necesitamos un MAPPING.")