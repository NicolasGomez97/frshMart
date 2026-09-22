|import pandas as pd

def auditoria_rapida(df: pd.DataFrame, nombre: str) -> dict:
    """Genera un resumen de calidad básico de un DataFrame."""
    total_filas = len(df)
    total_columnas = len(df.columns)
    filas_duplicadas = df.duplicated().sum()
    nulos_totales = df.isnull().sum().sum()
    
    # Calcular el porcentaje respecto al total de celdas
    total_celdas = total_filas * total_columnas
    porcentaje_nulos = round((nulos_totales / total_celdas) * 100, 2) if total_celdas > 0 else 0

    return {
        'archivo': nombre,
        'total_filas': total_filas,
        'total_columnas': total_columnas,
        'filas_duplicadas': filas_duplicadas,
        'nulos_totales': nulos_totales,
        'porcentaje_nulos': f"{porcentaje_nulos}%",
    }

# Cargar los 3 archivos
archivos = {
    'clientes': 'datos/campana_verano_clientes.csv',
    'ventas': 'datos/campana_verano_ventas.csv',
    'productos': 'datos/productos_promo_verano.csv',
}

for nombre, ruta in archivos.items():
    df = pd.read_csv(ruta)
    resumen = auditoria_rapida(df, nombre)
    print(f"\n{'='*40}")
    print(f"  {resumen['archivo'].upper()}")
    print(f"{'='*40}")
    for k, v in resumen.items():
        if k != 'archivo':
            print(f"  {k}: {v}")