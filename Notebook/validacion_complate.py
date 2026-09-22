import pandas as pd

def validate_campaign_data(df: pd.DataFrame) -> dict[str, bool]:
    """Ejecuta 5 validaciones de calidad sobre los datos de campaña.

    Returns:
        dict con nombre_validacion: True/False
    """
    results = {}

    # 1. El DataFrame no está vacío
    results["no_vacio"] = len(df) > 0

    # 2. Campos obligatorios no tienen NULLs
    campos_obligatorios = ["venta_id", "producto_id", "fecha_compra", "precio"]
    results["sin_nulls_obligatorios"] = all(
        df[campo].notna().all() for campo in campos_obligatorios
    )

    # 3. Todos los precios son > 0
    results["precios_positivos"] = bool((df["precio"] > 0).all())

    # 4. Fechas dentro del rango de campaña verano (2024-06-15 a 2024-09-15)
    results["fechas_en_rango"] = bool(
        ((df["fecha_compra"] >= "2024-06-15") & (df["fecha_compra"] <= "2024-09-15")).all()
    )

    # 5. No hay filas 100% duplicadas
    results["sin_duplicados"] = bool(df.duplicated().sum() == 0)

    return results


# Test con datos de ejemplo
datos_test = pd.DataFrame({
    "venta_id": [1, 2, 3],
    "cliente_id": [100, None, 200],
    "producto_id": [2001, 2002, 2003],
    "fecha_compra": pd.to_datetime(["2024-07-01", "2024-08-15", "2024-09-01"]),
    "cantidad": [1, 2, 3],
    "precio": [2.45, 8.99, 1.20],
})

resultados = validate_campaign_data(datos_test)
for nombre, paso in resultados.items():
    print(f"{'✓' if paso else '✗'} {nombre}")