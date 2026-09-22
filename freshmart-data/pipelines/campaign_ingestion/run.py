# pipelines/campaign_ingestion/run.py
"""Orquestación del pipeline: raw → limpieza → validación → silver."""
import argparse
import logging
import sys

import pandas as pd

from .config import Campaign, RAW_DIR, SILVER_DIR
from .clean import run_cleaning
from .validate import run_validations

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    stream=sys.stdout,
    force=True,
)
logger = logging.getLogger(__name__)


def run_pipeline(campaign: Campaign) -> pd.DataFrame:
    """Procesa una campaña de principio a fin."""
    origen = RAW_DIR / f"campana_{campaign.value}_ventas.csv"
    logger.info(f"=== Campaña {campaign.value}: leyendo {origen} ===")
    df = pd.read_csv(origen)

    df = run_cleaning(df, campaign)
    resultados = run_validations(df, campaign)

    # La decisión de diseño: si algo no valida, no se escribe.
    fallidas = [r for r in resultados if not r.passed]
    if fallidas:
        logger.error(
            f"{len(fallidas)} validación(es) fallida(s): no se escribe en silver. "
            "Revisa el detalle de arriba y consulta antes de tocar los datos."
        )
        raise SystemExit(1)

    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    destino = SILVER_DIR / f"ventas_{campaign.value}.parquet"
    df.to_parquet(destino, index=False)
    logger.info(f"=== {len(df):,} filas escritas en {destino} ===")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de ingesta de campañas")
    parser.add_argument(
        "--campaign",
        required=True,
        choices=[c.value for c in Campaign],
        help="Campaña a procesar",
    )
    args = parser.parse_args()
    run_pipeline(Campaign(args.campaign))