# q6_ticket_promedio_cliente.py
# Ticket promedio de compra por cliente.
# Uso: spark-submit spark/consultas/q6_ticket_promedio_cliente.py

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("q6_ticket_promedio_cliente") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("USE retail")

resultado = spark.sql("""
    SELECT
        c.c_customer_sk,
        c.c_first_name,
        c.c_last_name,
        COUNT(DISTINCT ss.ss_ticket_number)                              AS total_tickets,
        SUM(ss.ss_net_paid)                                             AS gasto_total,
        SUM(ss.ss_net_paid) / COUNT(DISTINCT ss.ss_ticket_number)       AS ticket_promedio
    FROM store_sales ss
    JOIN customer c ON ss.ss_customer_sk = c.c_customer_sk
    GROUP BY
        c.c_customer_sk,
        c.c_first_name,
        c.c_last_name
    ORDER BY ticket_promedio DESC
    LIMIT 50
""")

resultado.show(truncate=False)

spark.stop()
