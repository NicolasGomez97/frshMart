# csv_validator.py -- Validador reutilizable para CSVs de Marketing
import pandas as pd
from typing import Dict, List, Optional


class ValidationResult:
    """Resultado de una validacion con errores acumulados."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, msg: str):
        self.errors.append(msg)

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def summary(self) -> str:
        lines = []
        if self.is_valid:
            extra = f" ({len(self.warnings)} warning(s))" if self.warnings else ""
            lines.append(f"VALIDACION OK{extra}")
        else:
            lines.append(f"VALIDACION FALLIDA -- {len(self.errors)} error(es)")
        for e in self.errors:
            lines.append(f"  ERROR: {e}")
        for w in self.warnings:
            lines.append(f"  WARNING: {w}")
        return "\n".join(lines)


_TIPOS_SOPORTADOS = ('numeric', 'datetime', 'string')


def validate_csv(
    df: pd.DataFrame,
    expected_columns: List[str],
    column_types: Optional[Dict[str, str]] = None,
    max_null_pct: float = 0.05,
    critical_columns: Optional[List[str]] = None,
    key_columns: Optional[List[str]] = None,
) -> ValidationResult:
    """
    Valida un DataFrame contra un esquema esperado.

    Args:
        df: DataFrame cargado del CSV
        expected_columns: lista de columnas que DEBEN existir
        column_types: dict {columna: tipo_esperado} donde tipo es
                      'numeric', 'datetime', 'string'
        max_null_pct: porcentaje maximo de nulos aceptable (0.05 = 5%)
        critical_columns: columnas que NO pueden tener ningun nulo
        key_columns: columnas que forman la clave de negocio (ej: ['venta_id']).
                     Si se pasa, se valida que no haya claves repetidas
                     (distinto de duplicados de fila completa).

    Returns:
        ValidationResult con errores y warnings
    """
    result = ValidationResult()

    # 0. Verificar que el DataFrame no esté vacío
    if df.empty:
        result.add_error("El DataFrame está vacío (0 filas)")
        return result

    # 1. Verificar columnas esperadas
    missing = set(expected_columns) - set(df.columns)
    extra = set(df.columns) - set(expected_columns)
    if missing:
        result.add_error(f"Columnas faltantes: {sorted(missing)}")
    if extra:
        result.add_warning(f"Columnas extra (no esperadas): {sorted(extra)}")

    # Detectar configuraciones con columnas que no existen ni se esperan
    # (típicamente un typo en column_types/critical_columns/key_columns)
    referenced = set((column_types or {}).keys()) | set(critical_columns or []) | set(key_columns or [])
    unknown_refs = referenced - set(expected_columns)
    if unknown_refs:
        result.add_warning(
            f"Se piden validaciones sobre columnas no listadas en expected_columns "
            f"(revisar configuración): {sorted(unknown_refs)}"
        )

    # 2. Verificar tipos de datos
    if column_types:
        for col, expected_type in column_types.items():
            if expected_type not in _TIPOS_SOPORTADOS:
                raise ValueError(
                    f"Tipo desconocido '{expected_type}' para columna '{col}'. "
                    f"Tipos soportados: {_TIPOS_SOPORTADOS}"
                )
            if col not in df.columns:
                continue
            if expected_type == 'numeric':
                non_numeric = pd.to_numeric(df[col], errors='coerce').isna()
                original_na = df[col].isna()
                bad_values = non_numeric & ~original_na
                if bad_values.sum() > 0:
                    result.add_error(
                        f"Columna '{col}': {bad_values.sum()} valores no numéricos"
                    )
            elif expected_type == 'datetime':
                # format='mixed': los CSV de campaña traen fechas en varios formatos
                # a la vez (ISO, DD/MM/YYYY, "Aug 15, 2024"...). Sin esto, pandas
                # infiere un único formato del principio de la columna y marca como
                # inválidas las fechas válidas que no calzan con ese formato.
                non_date = pd.to_datetime(
                    df[col], errors='coerce', dayfirst=True, format='mixed'
                ).isna()
                original_na = df[col].isna()
                bad_values = non_date & ~original_na
                if bad_values.sum() > 0:
                    result.add_error(
                        f"Columna '{col}': {bad_values.sum()} valores no son fecha válida"
                    )
            elif expected_type == 'string':
                if pd.api.types.is_numeric_dtype(df[col]):
                    result.add_warning(
                        f"Columna '{col}' esperada como string pero fue leída como numérica "
                        f"(posible pérdida de ceros a la izquierda o formato)"
                    )

    # 3. Verificar nulos
    if critical_columns:
        for col in critical_columns:
            if col not in df.columns:
                continue
            null_count = df[col].isna().sum()
            if null_count > 0:
                result.add_error(
                    f"Columna crítica '{col}' tiene {null_count} nulos"
                )

    # Verificar umbral general de nulos
    for col in df.columns:
        null_pct = df[col].isna().mean()
        if null_pct > max_null_pct:
            result.add_warning(
                f"Columna '{col}': {null_pct:.1%} nulos (umbral: {max_null_pct:.1%})"
            )

    # 4. Verificar duplicados de fila completa
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        result.add_warning(f"Filas duplicadas exactas: {dup_count}")

    # 5. Verificar duplicados de clave de negocio
    if key_columns:
        cols_presentes = [c for c in key_columns if c in df.columns]
        if cols_presentes:
            key_dup_count = df.duplicated(subset=cols_presentes).sum()
            if key_dup_count > 0:
                result.add_error(
                    f"Clave {cols_presentes} repetida en {key_dup_count} fila(s)"
                )

    return result


# Ejemplo de uso con los datos de Maria
if __name__ == "__main__":
    from log_utils import setup_logging

    setup_logging()

    df = pd.read_csv("../Datos/campana_verano_ventas.csv")

    result = validate_csv(
        df=df,
        expected_columns=[
            'venta_id', 'cliente_id', 'producto_id',
            'fecha_compra', 'cantidad', 'precio'
        ],
        column_types={
            'cantidad': 'numeric',
            'fecha_compra': 'datetime',
        },
        critical_columns=['venta_id', 'producto_id', 'fecha_compra'],
        key_columns=['venta_id'],
        max_null_pct=0.03,
    )

    print(result.summary())