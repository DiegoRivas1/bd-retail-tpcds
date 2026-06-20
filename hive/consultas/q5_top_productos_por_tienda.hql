-- q5_top_productos_por_tienda.hql
-- Top 5 productos mas vendidos por tienda (por unidades vendidas).
USE retail;

SELECT
    s_store_name,
    i_product_name,
    unidades_vendidas,
    ingresos_totales
FROM (
    SELECT
        s.s_store_name,
        i.i_product_name,
        SUM(ss.ss_quantity)    AS unidades_vendidas,
        SUM(ss.ss_net_paid)    AS ingresos_totales,
        ROW_NUMBER() OVER (
            PARTITION BY s.s_store_name
            ORDER BY SUM(ss.ss_quantity) DESC
        ) AS rn
    FROM store_sales ss
    JOIN store s ON ss.ss_store_sk = s.s_store_sk
    JOIN item  i ON ss.ss_item_sk  = i.i_item_sk
    GROUP BY s.s_store_name, i.i_product_name
) t
WHERE rn <= 5
ORDER BY s_store_name, unidades_vendidas DESC;