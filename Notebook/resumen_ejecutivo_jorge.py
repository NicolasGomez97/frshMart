import pandas as pd
from log_utils import setup_logging

setup_logging()

# Supón que ya tienes el DataFrame 'resultado' con la columna 'segmento_calculado'
# Simular cargándolo del CSV que exportaste
resultado = pd.read_csv('../Datos/segmentacion_jorge.csv')

# Generar tabla resumen: segmento, cantidad, porcentaje
resumen = (
    resultado['segmento_calculado']
    .value_counts()
    .reset_index()
)
resumen.columns = ['segmento', 'cantidad']

# Calcular porcentaje
resumen['porcentaje'] = round(100*resumen['cantidad']/resumen['cantidad'].sum(),1)

# Ordenar de mayor a menor
resumen = resumen.sort_values('cantidad', ascending=False)

print("SEGMENTACIÓN DE CLIENTES — CAMPAÑA VERANO 2024")
print("=" * 50)
print(resumen.to_string(index=False))