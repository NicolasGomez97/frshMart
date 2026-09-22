# normalizar.py — Aplicar el mapping de columnas
import pandas as pd
from config_campama import COLUMN_MAPPINGS, COLUMNAS_OBLIGATORIAS, CAMPANA_CONFIG


def aplicar_mapping(df: pd.DataFrame, campana: str) -> pd.DataFrame:
    """
    Renombra columnas según el mapping de la campaña.
    Valida que todas las columnas obligatorias existen después.
    """
    mapping = COLUMN_MAPPINGS.get(campana, {})

    if mapping:
        df = df.rename(columns=mapping)

    # Validar que tenemos todas las columnas obligatorias
    faltantes = set(COLUMNAS_OBLIGATORIAS) - set(df.columns)
    if faltantes:
        raise ValueError(
            f"Campaña '{campana}': faltan columnas después del mapping: {faltantes}"
        )

    return df


def normalizar_anonimos(df: pd.DataFrame, campana: str) -> pd.DataFrame:
    """
    Unifica la representación de clientes anónimos.
    Verano: NULL = anónimo. Primavera: -1 = anónimo.
    Resultado: siempre NULL + columna 'es_anonimo'.
    """
    config = CAMPANA_CONFIG[campana]

    if not config['anonimo_es_null']:
        # Primavera usa -1 para anónimos → convertir a NULL
        df.loc[df['cliente_id'] == -1, 'cliente_id'] = None

    df['es_anonimo'] = df['cliente_id'].isna()
    return df
def limpiar_precio_flexible(df: pd.DataFrame, campana: str) -> pd.DataFrame:
    """
    Limpia la columna precio según la configuración de la campaña.
    - Verano: string '2,45€' → float 2.45
    - Primavera: ya es float, no hacer nada
    """
    config = CAMPANA_CONFIG[campana]

    if config['precio_es_string']:
        df['precio'] = (
            df['precio']
            .astype(str)
            .str.replace('€', '', regex=False)
            .str.replace(',', '.')
            .astype(float)
        )
    else:
        df['precio'] = df['precio'].astype(float)

    return df

def normalizar_fechas_flexible(df: pd.DataFrame, campana: str) -> pd.DataFrame:
    """
    Normaliza fechas según la campaña.
    - Verano: 3 formatos mezclados → format='mixed'
    - Primavera: solo DD/MM/YYYY → dayfirst=True
    """
    config = CAMPANA_CONFIG[campana]

    if config['fechas_mixtas']:
        df['fecha_compra'] = pd.to_datetime(
            df['fecha_compra'], format='mixed', dayfirst=True
        )
    else:
        df['fecha_compra'] = pd.to_datetime(
            df['fecha_compra'], dayfirst=True
        )

    return df
# Uso:
# df = pd.read_csv('../Datos/campana_primavera_ventas.csv')
# df = aplicar_mapping(df, 'primavera')
# df = normalizar_anonimos(df, 'primavera')
# → Ahora tiene el mismo esquema que verano