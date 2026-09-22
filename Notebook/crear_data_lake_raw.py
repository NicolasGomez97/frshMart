import shutil
from pathlib import Path

LAKE_ROOT = Path("freshmart-lake")
FUENTE = "marketing"
ANIO, MES, DIA = "2024", "09", "16"

archivos = [
    "campana_verano_clientes.csv",
    "campana_verano_ventas.csv",
    "productos_promo_verano.csv",
]

for archivo in archivos:
    # Extraer nombre de la tabla del nombre del archivo (quita la extensión .csv)
    tabla = archivo.replace(".csv", "")

    # Construir la ruta de destino: raw/{fuente}/{tabla}/{año}/{mes}/{dia}/
    destino = LAKE_ROOT / "raw" / FUENTE / tabla / ANIO / MES / DIA

    # Crear directorios si no existen
    destino.mkdir(parents=True, exist_ok=True)

    # Copiar archivo original sin tocar
    shutil.copy(f"datos/{archivo}", destino / archivo)

    print(f"✓ {archivo} → {destino}")