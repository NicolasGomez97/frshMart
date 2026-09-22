"""Validaciones de calidad para los datos de campaña."""
import logging
from dataclasses import dataclass

import pandas as pd

from .config import Campaign, DATE_RANGES

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Resultado de una validación individual."""
    name: str
    passed: bool
    details: str


def validate_not_empty(df: pd.DataFrame) -> ValidationResult:
    """El DataFrame debe tener al menos 1 fila."""
    passed = len(df) > 0
    return ValidationResult(
        name="no_vacio",
        passed=passed,
        details=f"{len(df)} filas" if passed else "¡DataFrame vacío!",
    )


def validate_no_null_required_fields(df: pd.DataFrame) -> ValidationResult:
    """Campos obligatorios no pueden ser NULL (excepto cliente_id en anónimos)."""
    required = ["venta_id", "producto_id", "fecha_compra", "precio", "cantidad"]
    nulls = {col: df[col].isna().sum() for col in required}
    problemas = {k: v for k, v in nulls.items() if v > 0}
    passed = len(problemas) == 0
    return ValidationResult(
        name="campos_obligatorios_no_nulos",
        passed=passed,
        details=f"OK" if passed else f"NULLs: {problemas}",
    )


def validate_positive_prices(df: pd.DataFrame) -> ValidationResult:
    """Todos los precios deben ser positivos."""
    negativos = (df["precio"] <= 0).sum()
    passed = negativos == 0
    return ValidationResult(
        name="precios_positivos",
        passed=passed,
        details="OK" if passed else f"{negativos} precios <= 0",
    )


def validate_dates_in_range(
    df: pd.DataFrame, campaign: Campaign
) -> ValidationResult:
    """Las fechas deben estar dentro del rango de la campaña."""
    date_min, date_max = DATE_RANGES[campaign]
    fuera_de_rango = (
        (df["fecha_compra"] < date_min) | (df["fecha_compra"] > date_max)
    ).sum()
    passed = fuera_de_rango == 0
    return ValidationResult(
        name="fechas_en_rango",
        passed=passed,
        details="OK" if passed else f"{fuera_de_rango} fuera de [{date_min}, {date_max}]",
    )


def validate_no_duplicates(df: pd.DataFrame) -> ValidationResult:
    """No debe haber filas 100% duplicadas."""
    dupes = df.duplicated().sum()
    passed = dupes == 0
    return ValidationResult(
        name="sin_duplicados",
        passed=passed,
        details="OK" if passed else f"{dupes} filas duplicadas",
    )


def run_validations(
    df: pd.DataFrame, campaign: Campaign
) -> list[ValidationResult]:
    """Ejecuta todas las validaciones y devuelve resultados."""
    results = [
        validate_not_empty(df),
        validate_no_null_required_fields(df),
        validate_positive_prices(df),
        validate_dates_in_range(df, campaign),
        validate_no_duplicates(df),
    ]

    # Logging
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    logger.info(f"Validaciones: {passed}/{total} pasaron")
    for r in results:
        icon = "✓" if r.passed else "✗"
        logger.info(f"  {icon} {r.name}: {r.details}")

    return results
