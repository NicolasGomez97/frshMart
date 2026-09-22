"""Funciones de limpieza para datos de campañas de Marketing."""
import logging

import pandas as pd

from .config import Campaign, COLUMN_MAPPINGS, CAMPAIGN_CONFIG, REQUIRED_COLUMNS

logger = logging.getLogger(__name__)


def apply_column_mapping(df: pd.DataFrame, campaign: Campaign) -> pd.DataFrame:
    """Renombra columnas según el mapping de la campaña."""
    mapping = COLUMN_MAPPINGS[campaign]
    if mapping:
        df = df.rename(columns=mapping)
        logger.info(f"  Mapping aplicado: {len(mapping)} columnas renombradas")

    # Verificar que todas las columnas obligatorias existen
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(
            f"Columnas obligatorias ausentes después del mapping: {missing}"
        )
    return df


def clean_dates(df: pd.DataFrame, campaign: Campaign) -> pd.DataFrame:
    """Normaliza la columna fecha_compra a datetime."""
    config = CAMPAIGN_CONFIG[campaign]
    try:
        if config["fechas_mixtas"]:
            df["fecha_compra"] = pd.to_datetime(
                df["fecha_compra"], format="mixed", dayfirst=True
            )
        else:
            df["fecha_compra"] = pd.to_datetime(
                df["fecha_compra"], dayfirst=True
            )
    except Exception as e:
        # No dejar que una fecha rota tumbe el pipeline entero
        logger.warning(f"  Fechas no parseables encontradas: {e}")
        df["fecha_compra"] = pd.to_datetime(
            df["fecha_compra"], format="mixed", dayfirst=True, errors="coerce"
        )
        nulas = df["fecha_compra"].isna().sum()
        logger.warning(f"  {nulas} fechas convertidas a NaT")

    return df


def clean_prices(df: pd.DataFrame, campaign: Campaign) -> pd.DataFrame:
    """Normaliza la columna precio a float."""
    config = CAMPAIGN_CONFIG[campaign]
    if config["precio_es_string"]:
        df["precio"] = (
            df["precio"]
            .astype(str)
            .str.replace("€", "", regex=False)
            .str.replace(",", ".")
            .astype(float)
        )
        logger.info("  Precios limpiados: eliminado €, coma → punto")
    else:
        df["precio"] = df["precio"].astype(float)
    return df


def mark_anonymous(df: pd.DataFrame, campaign: Campaign) -> pd.DataFrame:
    """Marca ventas anónimas con una columna booleana."""
    config = CAMPAIGN_CONFIG[campaign]
    anonimo_valor = config["anonimo_valor"]

    if anonimo_valor is None:
        df["es_anonimo"] = df["cliente_id"].isna()
    else:
        df.loc[df["cliente_id"] == anonimo_valor, "cliente_id"] = None
        df["es_anonimo"] = df["cliente_id"].isna()

    n_anonimos = df["es_anonimo"].sum()
    logger.info(f"  Ventas anónimas: {n_anonimos:,}")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas 100% duplicadas."""
    antes = len(df)
    df = df.drop_duplicates()
    eliminados = antes - len(df)
    if eliminados > 0:
        logger.info(f"  Duplicados eliminados: {eliminados:,}")
    return df


def filter_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra filas con cantidad <= 0 (errores de la app)."""
    antes = len(df)
    df = df[df["cantidad"] > 0]
    eliminados = antes - len(df)
    if eliminados > 0:
        logger.info(f"  Filas con cantidad <= 0 eliminadas: {eliminados}")
    return df


def run_cleaning(df: pd.DataFrame, campaign: Campaign) -> pd.DataFrame:
    """Ejecuta el pipeline de limpieza completo."""
    logger.info(f"Limpiando campaña: {campaign.value} ({len(df):,} filas)")

    df = apply_column_mapping(df, campaign)
    df = remove_duplicates(df)
    df = clean_dates(df, campaign)
    df = clean_prices(df, campaign)
    df = mark_anonymous(df, campaign)
    df = filter_invalid_rows(df)

    logger.info(f"  Resultado: {len(df):,} filas limpias")
    return df
