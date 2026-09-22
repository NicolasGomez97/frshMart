# subir_a_raw.py — Simular la estructura del data lake en local
import shutil
from pathlib import Path
from datetime import date

# Configuración
LAKE_ROOT = Path("freshmart-lake")
FUENTE = "marketing"
FECHA = date.today()  # 2024-09-16

# Archivos de María
archivos = [
    "campana_verano_clientes.csv",
    "campana_verano_ventas.csv",
    "productos_promo_verano.csv",
]

for archivo in archivos:
    # Nombre de la "tabla" = nombre del archivo sin extensión
    tabla = archivo.replace(".csv", "")

    # Estructura: raw/{fuente}/{tabla}/{año}/{mes}/{dia}/
    destino = (
        ".." / LAKE_ROOT / "raw" / FUENTE / tabla
        / str(FECHA.year) / f"{FECHA.month:02d}" / f"{FECHA.day:02d}"
    )
    destino.mkdir(parents=True, exist_ok=True)

    # Copiar el archivo ORIGINAL sin tocar
    shutil.copy(f"../Datos/{archivo}", destino / archivo)
    print(f"✓ {archivo} → {destino}")

print("\n✅ Todos los archivos subidos a raw (sin modificar)")