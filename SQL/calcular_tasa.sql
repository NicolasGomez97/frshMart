-- Tasa de conversión global de la campaña
-- OJO: compro es BOOLEANO (True/False), compáralo como booleano, no como texto
SELECT
    COUNT(*) AS total_alcanzados,
    SUM(CASE WHEN compro THEN 1 ELSE 0 END) AS compraron,
    ROUND(
        100.0 * SUM(CASE WHEN compro THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS tasa_conversion_pct
FROM campana_verano_clientes;

-- Tasa de conversión por canal
-- OJO: canal_contacto viene sucio (email/Email, push/push_notification...).
-- Normalízalo con LOWER() y unifica las variantes con un CASE.
SELECT
    CASE
        WHEN LOWER(canal_contacto) LIKE 'push%' THEN 'push'
        ELSE LOWER(canal_contacto)
    END AS canal,
    COUNT(*) AS alcanzados,
    SUM(CASE WHEN compro THEN 1 ELSE 0 END) AS compraron,
    ROUND(
        100.0 * SUM(CASE WHEN compro THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS tasa_conversion_pct
FROM campana_verano_clientes
GROUP BY canal,
ORDER BY tasa_conversion_pct DESC;