import pandas as pd
from log_utils import setup_logging

setup_logging()

COLUMNAS_OBLIGATORIAS = [
    'venta_id', 'cliente_id', 'producto_id', 'fecha_compra',
    'cantidad', 'precio', 'descuento_pct', 'tienda_id', 'campana'
]

COLUMN_MAPPINGS = {
    'verano': {},  # ya tiene los nombres correctos
    'primavera': {
        'id_transaccion': 'venta_id',
        'id_cliente': 'cliente_id',
        'id_producto': 'producto_id',
        'fecha_venta': 'fecha_compra',
        'unidades': 'cantidad',
        'importe': 'precio',
        'descuento': 'descuento_pct',
        'almacen': 'tienda_id',
        'promocion': 'campana',
    },
}


def aplicar_mapping(df: pd.DataFrame, campana: str) -> pd.DataFrame:
    """Renombra columnas según el mapping de la campaña."""
    mapping = COLUMN_MAPPINGS.get(campana, {})

    if mapping:
        df = df.rename(columns=mapping)

    # Validar columnas obligatorias
    faltantes = set(COLUMNAS_OBLIGATORIAS) - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas: {faltantes}")

    return df


# Probar con primavera
primavera = pd.read_csv('datos/campana_primavera_ventas.csv')
print("Antes:", list(primavera.columns))

primavera = aplicar_mapping(primavera, 'primavera')
print("Después:", list(primavera.columns))
print("\n✓ Mapping aplicado correctamente")