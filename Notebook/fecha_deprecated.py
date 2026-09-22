import pandas as pd
import logging
import sys

# stream=sys.stdout y force=True para que los avisos salgan en orden
# y sean los mismos en la segunda ejecución de la página
logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
    stream=sys.stdout,
    force=True,
)
logger = logging.getLogger(__name__)


def clean_dates(df: pd.DataFrame, has_mixed_formats: bool) -> pd.DataFrame:
    """Normaliza fecha_compra a datetime.

    - Si has_mixed_formats=True, usa format='mixed'
    - Si alguna fecha no se puede parsear, usa errors='coerce'
    - Loggea cuántas fechas quedaron como NaT
    """
    df = df.copy()
    formato = "mixed" if has_mixed_formats else None

    try:
        df["fecha_compra"] = pd.to_datetime(
            df["fecha_compra"], format=formato, dayfirst=True
        )
    except (ValueError, TypeError):
        logger.warning("Fechas no parseables (DateParseError). Reintento con errors='coerce'.")
        df["fecha_compra"] = pd.to_datetime(
            df["fecha_compra"], format=formato, dayfirst=True, errors="coerce"
        )
        n_nat = df["fecha_compra"].isna().sum()
        logger.warning(f"{n_nat} fechas convertidas a NaT")

    return df


# Test
datos = pd.DataFrame({
    "fecha_compra": [
        "2024-07-15",        # ISO
        "15/07/2024",        # EU
        "Jul 15, 2024",      # US
        "esto-no-es-fecha",  # Inválida
    ]
})

resultado = clean_dates(datos, has_mixed_formats=True)
print(resultado["fecha_compra"])
print(f"NaT count: {resultado['fecha_compra'].isna().sum()}")