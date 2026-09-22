# limpiar_ventas.py — Pipeline de limpieza del CSV de ventas
import pandas as pd
import logging
from log_utils import setup_logging

setup_logging()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


def normalizar_fechas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte fecha_compra de 3 formatos a datetime unificado.
    Formatos encontrados: YYYY-MM-DD, DD/MM/YYYY, Mon DD, YYYY
    """
    logger.info("Normalizando fechas...")
    antes_nulas = df['fecha_compra'].isna().sum()

    df['fecha_compra'] = pd.to_datetime(
        df['fecha_compra'],
        format='mixed',
        dayfirst=True  # para que DD/MM/YYYY se parsee bien
    )

    despues_nulas = df['fecha_compra'].isna().sum()
    nuevas_nulas = despues_nulas - antes_nulas
    if nuevas_nulas > 0:
        logger.warning(f"  {nuevas_nulas} fechas no se pudieron parsear")
    else:
        logger.info("  ✓ Todas las fechas parseadas correctamente")

    return df


def limpiar_precio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte precio de string '2,45€' a float 2.45
    """
    logger.info("Limpiando columna precio...")

    df['precio'] = (
        df['precio']
        .astype(str)
        .str.replace('€', '', regex=False)
        .str.replace(',', '.')
        .astype(float)
    )

    negativos = (df['precio'] < 0).sum()
    if negativos > 0:
        logger.warning(f"  {negativos} precios negativos detectados")

    logger.info(f"  ✓ Precio convertido. Rango: {df['precio'].min():.2f} - {df['precio'].max():.2f}")
    return df

def marcar_anonimos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Marca ventas sin cliente_id como anónimas.
    NO las elimina — son ventas reales de guest checkout.
    """
    logger.info("Marcando ventas anónimas...")
    df['es_anonimo'] = df['cliente_id'].isna()
    n_anonimos = df['es_anonimo'].sum()
    logger.info(f"  ✓ {n_anonimos} ventas anónimas marcadas ({100*n_anonimos/len(df):.1f}%)")
    return df


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas completamente duplicadas (mismo venta_id, mismos datos).
    """
    logger.info("Eliminando duplicados...")
    antes = len(df)
    df = df.drop_duplicates()
    eliminados = antes - len(df)
    logger.info(f"  ✓ {eliminados} duplicados eliminados")
    return df


def filtrar_cantidad_cero(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra ventas con cantidad = 0 (bug de la app, no son ventas reales).
    """
    logger.info("Filtrando filas con cantidad = 0...")
    antes = len(df)
    df = df[df['cantidad'] > 0]
    eliminados = antes - len(df)
    logger.info(f"  ✓ {eliminados} filas con cantidad=0 eliminadas")
    return df

def limpiar_ventas_campana(ruta_csv: str) -> pd.DataFrame:
    """
    Pipeline completo de limpieza para el CSV de ventas de campaña.
    Aplica cada función en orden y loguea el resultado.
    """
    logger.info(f"=== Iniciando limpieza: {ruta_csv} ===")

    # Cargar
    df = pd.read_csv(ruta_csv)
    logger.info(f"Filas cargadas: {len(df):,}")

    # Aplicar limpieza en orden
    df = eliminar_duplicados(df)
    df = normalizar_fechas(df)
    df = limpiar_precio(df)
    df = marcar_anonimos(df)
    df = filtrar_cantidad_cero(df)

    logger.info(f"=== Limpieza completada. Filas finales: {len(df):,} ===")
    return df


# Ejecutar
if __name__ == '__main__':
    ventas_limpias = limpiar_ventas_campana('../Datos/campana_verano_ventas.csv')

    # Guardar en zona silver (como Parquet en un proyecto real)
    ventas_limpias.to_csv('../Datos/output/silver_ventas_verano.csv', index=False)
    print(f"\n✅ Archivo limpio guardado: ../Datos/output/silver_ventas_verano.csv")
    print(f"   Filas originales: 42,891")
    print(f"   Filas finales: {len(ventas_limpias):,}")