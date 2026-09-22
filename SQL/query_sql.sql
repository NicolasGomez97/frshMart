-- segmentacion_campana.sql
-- Cruce para Jorge: segmentación de clientes de la campaña de verano

-- Paso 1: Contar pedidos recientes por cliente
WITH pedidos_recientes AS (
    SELECT
        cliente_id,
        COUNT(*) AS pedidos_3m
    FROM pedidos
    WHERE fecha_pedido >= '2024-06-16'  -- últimos 3 meses desde sept 2024
      AND estado NOT IN ('cancelado')
    GROUP BY cliente_id
),

-- Paso 2: Cruzar con los clientes de la campaña y la tabla maestra
-- LEFT JOIN: queremos TODOS los de la campaña, tengan pedidos o no
-- JOIN con clientes (maestra) porque nombre/email/fecha_registro NO están
-- en campana_verano_clientes.csv (ahí solo está el cliente_id de la campaña)
segmentacion AS (
    SELECT
        c.cliente_id,
        m.nombre,
        m.email,
        m.fecha_registro,
        COALESCE(p.pedidos_3m, 0) AS pedidos_ultimos_3m,
        CASE
            WHEN COALESCE(p.pedidos_3m, 0) > 6 THEN 'premium'
            WHEN COALESCE(p.pedidos_3m, 0) >= 2 THEN 'regular'
            ELSE 'nuevo'
        END AS segmento
    FROM campana_verano_clientes c
    LEFT JOIN clientes m ON c.cliente_id = m.cliente_id
    LEFT JOIN pedidos_recientes p ON c.cliente_id = p.cliente_id
)

-- Paso 3: Resultado ordenado por actividad
SELECT * FROM segmentacion
ORDER BY pedidos_ultimos_3m DESC;