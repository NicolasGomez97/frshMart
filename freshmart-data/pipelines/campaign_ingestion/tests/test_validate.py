"""Tests unitarios para las funciones de validación."""
import pandas as pd
import pytest

from campaign_ingestion.config import Campaign
from campaign_ingestion.validate import (
    validate_not_empty,
    validate_no_null_required_fields,
    validate_positive_prices,
    validate_dates_in_range,
    validate_no_duplicates,
)


@pytest.fixture
def df_valido():
    """DataFrame que pasa TODAS las validaciones."""
    return pd.DataFrame({
        "venta_id": [1, 2, 3],
        "cliente_id": [100, None, 200],  # None es anónimo, OK
        "producto_id": [2001, 2002, 2003],
        "fecha_compra": pd.to_datetime(["2024-07-01", "2024-07-15", "2024-08-01"]),
        "cantidad": [1, 2, 3],
        "precio": [2.45, 8.99, 1.20],
        "descuento_pct": [0.0, 10.0, 5.0],
        "tienda_id": [1, 2, 1],
        "campana": ["verano", "verano", "verano"],
        "es_anonimo": [False, True, False],
    })


@pytest.fixture
def df_vacio():
    """DataFrame sin filas."""
    return pd.DataFrame(columns=["venta_id", "producto_id", "fecha_compra", "precio", "cantidad"])


class TestValidateNotEmpty:
    def test_pasa_con_datos(self, df_valido):
        result = validate_not_empty(df_valido)
        assert result.passed is True

    def test_falla_sin_datos(self, df_vacio):
        result = validate_not_empty(df_vacio)
        assert result.passed is False


class TestValidatePositivePrices:
    def test_pasa_con_precios_positivos(self, df_valido):
        result = validate_positive_prices(df_valido)
        assert result.passed is True

    def test_falla_con_precio_negativo(self, df_valido):
        df_valido.loc[0, "precio"] = -5.0
        result = validate_positive_prices(df_valido)
        assert result.passed is False
        assert "-5" in result.details or "1" in result.details


class TestValidateDatesInRange:
    def test_pasa_con_fechas_en_rango_verano(self, df_valido):
        result = validate_dates_in_range(df_valido, Campaign.VERANO)
        assert result.passed is True

    def test_falla_con_fecha_fuera_de_rango(self, df_valido):
        df_valido.loc[0, "fecha_compra"] = pd.Timestamp("2024-01-01")
        result = validate_dates_in_range(df_valido, Campaign.VERANO)
        assert result.passed is False


class TestValidateNoDuplicates:
    def test_pasa_sin_duplicados(self, df_valido):
        result = validate_no_duplicates(df_valido)
        assert result.passed is True

    def test_falla_con_duplicados(self, df_valido):
        df_con_dupes = pd.concat([df_valido, df_valido.iloc[[0]]])
        result = validate_no_duplicates(df_con_dupes)
        assert result.passed is False
