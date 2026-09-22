# FreshMart

Proyecto de práctica de ingeniería de datos: limpieza, validación, normalización y análisis de datos de ventas y campañas de marketing de una cadena de retail ficticia (FreshMart).

Simula un flujo de trabajo real de un equipo de datos: ingesta de CSVs "sucios" de distintas fuentes (campañas de verano y primavera, cada una con su propio esquema), un data lake local particionado por fecha, pipelines de limpieza/normalización, validaciones de calidad, y queries SQL de análisis para stakeholders del negocio.

## Estructura

```
FreshMart/
├── Datos/                  # Datasets de origen (CSV): clientes, productos, pedidos, ventas, campañas
│   └── output/              # Resultados de los pipelines de limpieza (capa "silver")
├── Notebook/                # Scripts exploratorios y pipeline de limpieza de campañas
│   ├── explorar_campana.py       # Primer análisis exploratorio de los datos de campaña
│   ├── config_campama.py         # Mapeo de columnas y particularidades por campaña
│   ├── normalizar.py             # Normalización de fechas, precios, columnas
│   ├── limpiar_ventas.py         # Limpieza del CSV de ventas
│   ├── run_pipeline.py           # Pipeline unificado (cualquier campaña) end-to-end
│   ├── pipeline_limpieza_campaña.py
│   ├── auditoria_calidad.py      # Resumen de calidad de un DataFrame
│   ├── validacion_complate.py    # Validaciones de calidad de datos de campaña
│   ├── ValidadorCSV.py           # Validador reutilizable de CSVs
│   ├── comparar_esquemas_ver_pri.py  # Comparación de esquemas entre campañas
│   ├── cruce_segmentacion.py     # Segmentación de clientes (pedido de negocio)
│   ├── cliente_sin_pedidos.py
│   ├── resumen_ejecutivo_jorge.py
│   ├── crear_data_lake_raw.py    # Simula la estructura de un data lake (zona raw)
│   ├── subir_a_raw.py
│   ├── alertas_slack.py          # Ejemplo de alerta a Slack ante gaps de datos
│   ├── dag_conecction.py         # Diagnóstico de fallas de conexión en Airflow (ejercicio)
│   ├── log_utils.py              # Utilidad compartida de logging
│   └── test_unitario.py
├── SQL/                     # Queries de análisis
│   ├── query_sql.sql             # Segmentación de clientes para negocio
│   ├── calcular_tasa.sql         # Tasa de conversión de campaña
│   └── detectar_gaps_pipeline.sql # Detección de días sin datos en la tabla gold
├── freshmart-data/          # Pipeline de ingestión de campañas empaquetado (con tests)
│   └── pipelines/campaign_ingestion/
│       ├── config.py / clean.py / validate.py / run.py
│       └── tests/
└── freshmart-lake/          # Data lake local simulado, particionado por fecha (raw/marketing/...)
```

## Tech stack

- Python 3.11 (pandas)
- SQL (PostgreSQL)
- pytest para tests del pipeline de ingestión

## Uso

Pipeline de campañas empaquetado:

```bash
cd freshmart-data
python -m pipelines.campaign_ingestion.run
pytest pipelines/campaign_ingestion/tests/
```

Scripts exploratorios / pipeline de limpieza:

```bash
cd Notebook
python run_pipeline.py
```
