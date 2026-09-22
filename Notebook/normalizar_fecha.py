import pandas as pd
from log_utils import setup_logging

setup_logging()

ventas = pd.read_csv('../Datos/campana_verano_ventas.csv')

print("Tipo original:", ventas['fecha_compra'].dtype)
print("Ejemplo formatos:")
print("  ISO:", ventas.loc[0, 'fecha_compra'])  # YYYY-MM-DD
# Buscar ejemplo de cada formato para verificar


def normalizar_fechas(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte fecha_compra de 3 formatos a datetime."""
    df = df.copy()

    # pd.to_datetime con format='mixed' maneja múltiples formatos
    df['fecha_compra'] = pd.to_datetime(
        df['fecha_compra'],
        format='mixed',       # TODO: este parámetro maneja múltiples formatos
        dayfirst=True        # TODO: cámbialo a True para que DD/MM se interprete bien
    )

    # Verificar que no quedaron NaT
    nat_count = df['fecha_compra'].isna().sum()
    if nat_count > 0:
        print(f"⚠️ {nat_count} fechas no se pudieron parsear")
    else:
        print("✓ Todas las fechas parseadas correctamente")

    return df


ventas = normalizar_fechas(ventas)
print(f"\nTipo después: {ventas['fecha_compra'].dtype}")
print(f"Rango: {ventas['fecha_compra'].min()} a {ventas['fecha_compra'].max()}")