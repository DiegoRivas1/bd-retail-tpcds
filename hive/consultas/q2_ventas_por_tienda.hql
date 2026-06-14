-- q2_ventas_por_tienda.hql
-- Ventas totales agrupadas por tienda.
USE retail;

SELECT
    s.s_store_sk,
    s.s_store_name,
    COUNT(ss.ss_ticket_number)  AS total_transacciones,
    SUM(ss.ss_net_paid)         AS ingresos_totales,
    AVG(ss.ss_net_paid)         AS ingreso_promedio
FROM store_sales ss
JOIN store s ON ss.ss_store_sk = s.s_store_sk
GROUP BY
    s.s_store_sk,
    s.s_store_name
ORDER BY ingresos_totales DESC;
