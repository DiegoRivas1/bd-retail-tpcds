-- q6_ticket_promedio_cliente.hql
-- Ticket promedio de compra por cliente.
USE retail;

SELECT
    c.c_customer_sk,
    c.c_first_name,
    c.c_last_name,
    COUNT(DISTINCT ss.ss_ticket_number)                             AS total_tickets,
    SUM(ss.ss_net_paid)                                            AS gasto_total,
    SUM(ss.ss_net_paid) / COUNT(DISTINCT ss.ss_ticket_number)      AS ticket_promedio
FROM store_sales ss
JOIN customer c ON ss.ss_customer_sk = c.c_customer_sk
GROUP BY
    c.c_customer_sk,
    c.c_first_name,
    c.c_last_name
ORDER BY ticket_promedio DESC
LIMIT 50;
