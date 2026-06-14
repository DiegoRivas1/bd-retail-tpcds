# q1_top_clientes_compras.py
# Top 20 clientes con mayor numero de compras.
# Uso: spark-submit spark/consultas/q1_top_clientes_compras.py

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("q1_top_clientes_compras") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("USE retail")

resultado = spark.sql("""
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
    LIMIT 20
""")

resultado.show(truncate=False)

spark.stop()
