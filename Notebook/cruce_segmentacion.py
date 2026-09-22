# cruce_segmentacion.py — Lo que Jorge necesita
import pandas as pd
from datetime import datetime, timedelta
from log_utils import setup_logging

setup_logging()

# Cargar datos
clientes_campana = pd.read_csv('../Datos/campana_verano_clientes.csv')
clientes_maestra = pd.read_csv('../Datos/clientes.csv')  # nombre, fecha_registro, email...
pedidos = pd.read_csv('../Datos/pedidos.csv')

# Convertir fechas (pedidos puede tener formatos mixtos)
pedidos['fecha_pedido'] = pd.to_datetime(
    pedidos['fecha_pedido'], format='mixed', dayfirst=True
)

# Paso 1: Filtrar pedidos últimos 3 meses (desde 2024-06-16)
fecha_corte = pd.Timestamp('2024-06-16')
pedidos_recientes = pedidos[
    (pedidos['fecha_pedido'] >= fecha_corte) &
    (pedidos['estado'] != 'cancelado')
]

# Paso 2: Contar pedidos por cliente
conteo = (
    pedidos_recientes
    .groupby('cliente_id')
    .size()
    .reset_index(name='pedidos_3m')
)

# Paso 3: LEFT JOIN con clientes de la campaña
resultado = clientes_campana.merge(
    conteo, on='cliente_id', how='left'
)
resultado['pedidos_3m'] = resultado['pedidos_3m'].fillna(0).astype(int)

# Paso 4: Clasificar en segmentos
def clasificar(pedidos):
    if pedidos > 6:
        return 'premium'
    elif pedidos >= 2:
        return 'regular'
    else:
        return 'nuevo'

resultado['segmento_calculado'] = resultado['pedidos_3m'].apply(clasificar)

# Paso 5: Enriquecer con datos de la tabla maestra (nombre, fecha_registro)
# OJO: campana_verano_clientes.csv NO trae nombre ni fecha_registro,
# solo el cliente_id. Hay que cruzarlo con clientes.csv.
resultado = resultado.merge(
    clientes_maestra[['cliente_id', 'nombre', 'fecha_registro']],
    on='cliente_id', how='left'
)

# Resumen
print("Distribución de segmentos:")
print(resultado['segmento_calculado'].value_counts())
print(f"\nClientes sin pedidos: {(resultado['pedidos_3m'] == 0).sum()}")

# Exportar para Jorge (con fecha_registro incluida)
cols_jorge = ['cliente_id', 'nombre', 'fecha_registro',
              'segmento_calculado', 'pedidos_3m']
resultado[cols_jorge].to_csv('../Datos/output/segmentacion_jorge.csv', index=False)
print("\n✅ Archivo exportado: output/segmentacion_jorge.csv")