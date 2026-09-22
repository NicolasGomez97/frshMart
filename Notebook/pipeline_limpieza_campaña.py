import pandas as pd
import logging
from log_utils import setup_logging

setup_logging()

logging.basicConfig(level=logging.INFO, format='%(message)s')

COLUMNAS_OBLIGATORIAS = [
    'venta_id', 'cliente_id', 'producto_id', 'fecha_compra',
    'cantidad', 'precio', 'descuento_pct', 'tienda_id', 'campana'
]
COLUMN_MAPPINGS = {
    'verano': {},
    'primavera': {
        'id_transaccion': 'venta_id', 'id_cliente': 'cliente_id',
        'id_producto': 'producto_id', 'fecha_venta': 'fecha_compra',
        'unidades': 'cantidad', 'importe': 'precio',
        'descuento': 'descuento_pct', 'almacen': 'tienda_id',
        'promocion': 'campana',
    },
}
CAMPANA_CONFIG = {
    'verano': {'precio_es_string': True, 'fechas_mixtas': True, 'anonimo_es_null': True},
    'primavera': {'precio_es_string': False, 'fechas_mixtas': False, 'anonimo_es_null': False},
}

def aplicar_mapping(df, campana):
    mapping = COLUMN_MAPPINGS.get(campana, {})
    if mapping:
        df = df.rename(columns=mapping)
    faltantes = set(COLUMNAS_OBLIGATORIAS) - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan: {faltantes}")
    return df

ARCHIVOS = {
    'verano': '../Datos/campana_verano_ventas.csv',
    'primavera': '../Datos/campana_primavera_ventas.csv',
}
resultados = []

for campana, ruta in ARCHIVOS.items():
    logging.info(f"\n{'='*40}")
    logging.info(f"Procesando: {campana}")
    df = pd.read_csv(ruta)
    logging.info(f"  Cargadas: {len(df):,} filas")
    df = aplicar_mapping(df, campana)
    antes = len(df)
    df = df.drop_duplicates()
    logging.info(f"  Duplicados eliminados: {antes - len(df)}")
    config = CAMPANA_CONFIG[campana]
    if config['fechas_mixtas']:
        df['fecha_compra'] = pd.to_datetime(df['fecha_compra'], format='mixed', dayfirst=True)
    else:
        df['fecha_compra'] = pd.to_datetime(df['fecha_compra'], dayfirst=True)
    if config['precio_es_string']:
        df['precio'] = df['precio'].astype(str).str.replace('€','',regex=False).str.replace(',','.').astype(float)
    else:
        df['precio'] = df['precio'].astype(float)
    if not config['anonimo_es_null']:
        df.loc[df['cliente_id'] == -1, 'cliente_id'] = None
    df['es_anonimo'] = df['cliente_id'].isna()
    df = df[df['cantidad'] > 0]
    resultados.append(df)
    logging.info(f"  Resultado: {len(df):,} filas limpias")

unificado = pd.concat(resultados, ignore_index=True)
print(f"\n{'='*40}")
print(f"RESUMEN FINAL")
print(f"{'='*40}")
print(f"Total filas: {len(unificado):,}")
print(f"Por campaña: {unificado['campana'].value_counts().to_dict()}")
print(f"Anónimos: {unificado['es_anonimo'].sum():,}")
print(f"Rango fechas: {unificado['fecha_compra'].min()} a {unificado['fecha_compra'].max()}")