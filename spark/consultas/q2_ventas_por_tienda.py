# q2_ventas_por_tienda.py
# Ventas totales agrupadas por tienda.
# Uso: spark-submit spark/consultas/q2_ventas_por_tienda.py

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("q2_ventas_por_tienda") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("USE retail")

resultado = spark.sql("""
    SELECT
        s.s_store_sk,
        s.s_store_name,
        COUNT(ss.ss_ticket_number)  AS total_transacciones,
        SUM(ss.ss_net_paid)         AS ingresos_totales,
        AVG(ss.ss_net_paid)         AS ingreso_promedio
    FROM store_sales ss
    JOIN store s ON ss.ss_store_sk = s.s_store_sk
    GROUP BY
        s.s_store_sk,
        s.s_store_name
    ORDER BY ingresos_totales DESC
""")

resultado.show(truncate=False)

spark.stop()
