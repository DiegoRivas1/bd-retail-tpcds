-- q9_ranking_mensual_ventas.hql
-- Ranking mensual de tiendas por ingresos usando window function.
USE retail;

SELECT
    d.d_year                        AS anio,
    d.d_moy                         AS mes,
    s.s_store_name,
    SUM(ss.ss_net_paid)             AS ingresos_totales,
    RANK() OVER (
        PARTITION BY d.d_year, d.d_moy
        ORDER BY SUM(ss.ss_net_paid) DESC
    )                               AS ranking
FROM store_sales ss
JOIN date_dim d ON ss.ss_sold_date_sk = d.d_date_sk
JOIN store    s ON ss.ss_store_sk     = s.s_store_sk
GROUP BY
    d.d_year,
    d.d_moy,
    s.s_store_name
ORDER BY
    d.d_year,
    d.d_moy,
    ranking;
