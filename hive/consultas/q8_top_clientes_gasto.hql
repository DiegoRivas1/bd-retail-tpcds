-- q8_top_clientes_gasto.hql
-- Top 20 clientes por gasto total acumulado.
USE retail;

SELECT
    c.c_customer_sk,
    c.c_first_name,
    c.c_last_name,
    c.c_email_address,
    SUM(ss.ss_net_paid)             AS gasto_total,
    COUNT(DISTINCT ss.ss_ticket_number) AS total_tickets
FROM store_sales ss
JOIN customer c ON ss.ss_customer_sk = c.c_customer_sk
GROUP BY
    c.c_customer_sk,
    c.c_first_name,
    c.c_last_name,
    c.c_email_address
ORDER BY gasto_total DESC
LIMIT 20;
