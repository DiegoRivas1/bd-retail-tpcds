# q9_ranking_mensual_ventas.py
# Ranking mensual de tiendas por ingresos usando window function.
# Uso: spark-submit spark/consultas/q9_ranking_mensual_ventas.py

from pyspark.sql import SparkSession
from pyspark.sql import Window
from pyspark.sql.functions import rank

spark = SparkSession.builder \
    .appName("q9_ranking_mensual_ventas") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("USE retail")

ventas = spark.sql("""
    SELECT
        d.d_year            AS anio,
        d.d_moy             AS mes,
        s.s_store_name,
        SUM(ss.ss_net_paid) AS ingresos_totales
    FROM store_sales ss
    JOIN date_dim d ON ss.ss_sold_date_sk = d.d_date_sk
    JOIN store    s ON ss.ss_store_sk     = s.s_store_sk
    GROUP BY
        d.d_year,
        d.d_moy,
        s.s_store_name
""")

ventana = Window.partitionBy("anio", "mes").orderBy(ventas["ingresos_totales"].desc())

resultado = ventas \
    .withColumn("ranking", rank().over(ventana)) \
    .orderBy("anio", "mes", "ranking")

resultado.show(100, truncate=False)

spark.stop()
