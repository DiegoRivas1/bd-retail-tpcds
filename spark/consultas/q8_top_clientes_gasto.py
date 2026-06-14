# q8_top_clientes_gasto.py
# Top 20 clientes por gasto total acumulado.
# Uso: spark-submit spark/consultas/q8_top_clientes_gasto.py

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("q8_top_clientes_gasto") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("USE retail")

resultado = spark.sql("""
    SELECT
        c.c_customer_sk,
        c.c_first_name,
        c.c_last_name,
        c.c_email_address,
        SUM(ss.ss_net_paid)                 AS gasto_total,
        COUNT(DISTINCT ss.ss_ticket_number) AS total_tickets
    FROM store_sales ss
    JOIN customer c ON ss.ss_customer_sk = c.c_customer_sk
    GROUP BY
        c.c_customer_sk,
        c.c_first_name,
        c.c_last_name,
        c.c_email_address
    ORDER BY gasto_total DESC
    LIMIT 20
""")

resultado.show(truncate=False)

spark.stop()
