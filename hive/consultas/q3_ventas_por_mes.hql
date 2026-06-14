-- q3_ventas_por_mes.hql
-- Ventas totales agrupadas por año y mes.
USE retail;

SELECT
    d.d_year                    AS anio,
    d.d_moy                     AS mes,
    COUNT(ss.ss_ticket_number)  AS total_transacciones,
    SUM(ss.ss_net_paid)         AS ingresos_totales
FROM store_sales ss
JOIN date_dim d ON ss.ss_sold_date_sk = d.d_date_sk
GROUP BY
    d.d_year,
    d.d_moy
ORDER BY
    d.d_year,
    d.d_moy;
