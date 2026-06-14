-- q1_top_clientes_compras.hql
-- Top 20 clientes con mayor numero de compras.
USE retail;

SELECT
    c.c_customer_sk,
    c.c_first_name,
    c.c_last_name,
    COUNT(ss.ss_ticket_number) AS total_compras
FROM store_sales ss
JOIN customer c ON ss.ss_customer_sk = c.c_customer_sk
GROUP BY
    c.c_customer_sk,
    c.c_first_name,
    c.c_last_name
ORDER BY total_compras DESC
LIMIT 20;
