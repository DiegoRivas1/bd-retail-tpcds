-- q4_ventas_por_dia.hql
-- Ventas totales agrupadas por dia de la semana.
-- d_dow: 0=domingo, 1=lunes, ..., 6=sabado
USE retail;

SELECT
    d.d_day_name                AS dia_semana,
    d.d_dow                     AS numero_dia,
    COUNT(ss.ss_ticket_number)  AS total_transacciones,
    SUM(ss.ss_net_paid)         AS ingresos_totales
FROM store_sales ss
JOIN date_dim d ON ss.ss_sold_date_sk = d.d_date_sk
GROUP BY
    d.d_day_name,
    d.d_dow
ORDER BY d.d_dow;
