-- detectar_gaps_pipeline.sql
-- Encuentra dias sin datos en la tabla gold de ventas diarias
-- Se asume que TODOS los dias deberian tener al menos 1 registro

-- 1. Generar serie de fechas esperadas (ventana de 30 dias)
-- Usamos una fecha de referencia FIJA porque el dataset es historico de 2024.
WITH fechas_esperadas AS (
    SELECT gs::date AS fecha
    FROM generate_series(
        DATE '2024-04-20' - INTERVAL '30 days',
        DATE '2024-04-20' - INTERVAL '1 day',
        INTERVAL '1 day'
    ) AS t(gs)
),

-- 2. Obtener las fechas que SI tienen datos
fechas_con_datos AS (
    SELECT DISTINCT fecha_venta AS fecha
    FROM gold_ventas_diarias
    WHERE fecha_venta >= DATE '2024-04-20' - INTERVAL '30 days'
),

-- 3. Encontrar los gaps (fechas sin datos)
gaps AS (
    SELECT
        fe.fecha,
        CASE
            WHEN fd.fecha IS NULL THEN 'SIN DATOS'
            ELSE 'OK'
        END AS estado
    FROM fechas_esperadas fe
    LEFT JOIN fechas_con_datos fd ON fe.fecha = fd.fecha
    WHERE fd.fecha IS NULL
)

SELECT
    fecha,
    estado,
    fecha - LAG(fecha) OVER (ORDER BY fecha) AS dias_desde_ultimo_gap
FROM gaps
ORDER BY fecha DESC;

-- Si esta query devuelve filas, hay dias sin datos
-- En un sistema de alertas, esto dispararia una notificacion