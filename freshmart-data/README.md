# freshmart-data

Pipelines de datos de FreshMart.

## Estructura

```
freshmart-data/
├── pipelines/
│   └── campaign_ingestion/
│       ├── config.py      # Mappings, constantes, enums
│       ├── clean.py       # Funciones de limpieza
│       ├── validate.py    # Validaciones de calidad
│       ├── run.py         # Orquestación del pipeline
│       └── tests/
├── data/
│   ├── raw/                # CSVs originales (no se tocan)
│   └── silver/              # Parquet limpios (output)
└── README.md
```

## Uso

```bash
python -m pipelines.campaign_ingestion.run
```

## Tests

```bash
pytest pipelines/campaign_ingestion/tests/
```
