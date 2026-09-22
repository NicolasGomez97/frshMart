"""Configuración centralizada del pipeline de campañas."""
from enum import Enum
from pathlib import Path


class Campaign(Enum):
    """Campañas conocidas. Usar este Enum evita typos silenciosos."""
    VERANO = "verano"
    PRIMAVERA = "primavera"


# Columnas obligatorias después del mapping
REQUIRED_COLUMNS = [
    "venta_id", "cliente_id", "producto_id", "fecha_compra",
    "cantidad", "precio", "descuento_pct", "tienda_id", "campana",
]

# Mapping de columnas por campaña (origen → destino estándar)
COLUMN_MAPPINGS: dict[Campaign, dict[str, str]] = {
    Campaign.VERANO: {},  # Ya viene con nombres correctos
    Campaign.PRIMAVERA: {
        "id_transaccion": "venta_id",
        "id_cliente": "cliente_id",
        "id_producto": "producto_id",
        "fecha_venta": "fecha_compra",
        "unidades": "cantidad",
        "importe": "precio",
        "descuento": "descuento_pct",
        "almacen": "tienda_id",
        "promocion": "campana",
    },
}

# Configuración específica de limpieza por campaña
CAMPAIGN_CONFIG: dict[Campaign, dict] = {
    Campaign.VERANO: {
        "precio_es_string": True,
        "fechas_mixtas": True,
        "anonimo_valor": None,  # NULL = anónimo
    },
    Campaign.PRIMAVERA: {
        "precio_es_string": False,
        "fechas_mixtas": False,
        "anonimo_valor": -1,  # -1 = anónimo
    },
}

# Rutas
RAW_DIR = Path("data/raw")
SILVER_DIR = Path("data/silver")

# Rango válido de fechas por campaña
DATE_RANGES: dict[Campaign, tuple[str, str]] = {
    Campaign.VERANO: ("2024-06-15", "2024-09-15"),
    Campaign.PRIMAVERA: ("2024-03-01", "2024-05-31"),
}
