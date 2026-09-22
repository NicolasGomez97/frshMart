# run_pipeline.py — Pipeline unificado para cualquier campaña
import pandas as pd
import logging
from config_campama import COLUMN_MAPPINGS, COLUMNAS_OBLIGATORIAS, CAMPANA_CONFIG
from normalizar import aplicar_mapping, normalizar_fechas_flexible, limpiar_precio_flexible, normalizar_anonimos
from log_utils import setup_logging

setup_logging()

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)


def pipeline_campana(ruta_csv: str, campana: str) -> pd.DataFrame:
    """
    Pipeline completo de ingesta y limpieza para cualquier campaña.

    Args:
        ruta_csv: Ruta al archivo CSV original
        campana: Nombre de la campaña ('verano', 'primavera', etc.)

    Returns:
        DataFrame limpio con esquema estándar
    """
    logger.info(f"{'='*50}")
    logger.info(f"Pipeline: {campana} | Archivo: {ruta_csv}")
    logger.info(f"{'='*50}")

    # 1. Cargar
    df = pd.read_csv(ruta_csv)
    logger.info(f"[CARGA] {len(df):,} filas cargadas")

    # 2. Aplicar mapping de columnas
    df = aplicar_mapping(df, campana)
    logger.info(f"[MAPPING] Columnas normalizadas al esquema estándar")

    # 3. Eliminar duplicados
    antes = len(df)
    df = df.drop_duplicates()
    logger.info(f"[DUPLICADOS] {antes - len(df)} eliminados")

    # 4. Normalizar fechas
    df = normalizar_fechas_flexible(df, campana)
    logger.info(f"[FECHAS] Normalizadas a datetime")

    # 5. Limpiar precio
    df = limpiar_precio_flexible(df, campana)
    logger.info(f"[PRECIO] Convertido a float")

    # 6. Normalizar anónimos
    df = normalizar_anonimos(df, campana)
    n_anon = df['es_anonimo'].sum()
    logger.info(f"[ANONIMOS] {n_anon} ventas anónimas marcadas")

    # 7. Filtrar cantidad = 0
    antes = len(df)
    df = df[df['cantidad'] > 0]
    logger.info(f"[CANTIDAD] {antes - len(df)} filas con cantidad=0 eliminadas")

    logger.info(f"[RESULTADO] {len(df):,} filas finales")
    return df


# Ejecutar para ambas campañas
if __name__ == '__main__':
    verano = pipeline_campana('../Datos/campana_verano_ventas.csv', 'verano')
    primavera = pipeline_campana('../Datos/campana_primavera_ventas.csv', 'primavera')

    # Unificar
    unificado = pd.concat([verano, primavera], ignore_index=True)
    unificado.to_csv('../Datos/output/silver_ventas_unificado.csv', index=False)
    logger.info(f"\n✅ Total unificado: {len(unificado):,} filas → silver_ventas_unificado.csv")