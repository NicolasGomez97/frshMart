import pandas as pd

# Funciones a testear (simplificadas)
# bool() convierte el numpy.bool_ de pandas en un bool de Python
def validate_positive_prices(df):
    return bool((df["precio"] > 0).all())

def validate_no_duplicates(df):
    return bool(df.duplicated().sum() == 0)

def df_valido():
    """Datos que cumplen las dos validaciones."""
    return pd.DataFrame({
        "precio": [2.45, 8.99, 1.20, 15.00],
        "producto": ["A", "B", "C", "D"],
    })

# TESTS — completa cada uno. Cada test devuelve True si acierta.
def test_pasa_con_precios_validos():
    df = df_valido()
    return validate_positive_prices(df)

def test_falla_con_precio_negativo():
    df = df_valido()
    df.loc[1, "precio"] = -5.0
    return not validate_positive_prices(df)

def test_pasa_sin_duplicados():
    df = df_valido()
    return validate_no_duplicates(df)

def test_falla_con_duplicados():
    df = df_valido()
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    return not validate_no_duplicates(df)

# Lanzar los cuatro
tests = [
    test_pasa_con_precios_validos,
    test_falla_con_precio_negativo,
    test_pasa_sin_duplicados,
    test_falla_con_duplicados,
]
ok = 0
for t in tests:
    paso = t()
    print(f"{'✓' if paso else 'X'} {t.__name__}")
    ok += 1 if paso else 0
print(f"{ok}/{len(tests)} tests OK")