# q3_ventas_por_mes.py
# Ventas totales agrupadas por año y mes.
# Uso: spark-submit spark/consultas/q3_ventas_por_mes.py

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("q3_ventas_por_mes") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("USE retail")

resultado = spark.sql("""
    SELECT
        d.d_year                    AS anio,
        d.d_moy                     AS mes,
        COUNT(ss.ss_ticket_number)  AS total_transacciones,
        SUM(ss.ss_net_paid)         AS ingresos_totales
    FROM store_sales ss
    JOIN date_dim d ON ss.ss_sold_date_sk = d.d_date_sk
    GROUP BY
        d.d_year,
        d.d_moy
    ORDER BY
        d.d_year,
        d.d_moy
""")

resultado.show(50, truncate=False)

spark.stop()
