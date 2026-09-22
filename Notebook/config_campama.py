# config.py — Configuración centralizada del pipeline de campañas

# Esquema estándar que espera nuestro pipeline de limpieza
COLUMNAS_OBLIGATORIAS = [
    'venta_id', 'cliente_id', 'producto_id', 'fecha_compra',
    'cantidad', 'precio', 'descuento_pct', 'tienda_id', 'campana'
]

# Mappings: cómo se llaman las columnas en cada archivo de origen
COLUMN_MAPPINGS = {
    'verano': {
        # Verano ya viene con los nombres correctos, no necesita mapping
    },
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

# Particularidades por campaña
CAMPANA_CONFIG = {
    'verano': {
        'precio_es_string': True,   # "2,45€" → necesita limpiar
        'fechas_mixtas': True,      # 3 formatos diferentes
        'anonimo_es_null': True,    # cliente_id NULL = anónimo
    },
    'primavera': {
        'precio_es_string': False,  # ya es float
        'fechas_mixtas': False,     # solo DD/MM/YYYY
        'anonimo_es_null': False,   # usa -1 para anónimos
    },
}