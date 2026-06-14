# q5_top_productos_por_tienda.py
# Top 5 productos mas vendidos por tienda (por unidades vendidas).
# Uso: spark-submit spark/consultas/q5_top_productos_por_tienda.py

from pyspark.sql import SparkSession
from pyspark.sql import Window
from pyspark.sql.functions import sum as _sum, rank

spark = SparkSession.builder \
    .appName("q5_top_productos_por_tienda") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("USE retail")

ventas = spark.sql("""
    SELECT
        s.s_store_name,
        i.i_product_name,
        SUM(ss.ss_quantity)  AS unidades_vendidas,
        SUM(ss.ss_net_paid)  AS ingresos_totales
    FROM store_sales ss
    JOIN store s ON ss.ss_store_sk = s.s_store_sk
    JOIN item  i ON ss.ss_item_sk  = i.i_item_sk
    GROUP BY
        s.s_store_name,
        i.i_product_name
""")

ventana = Window.partitionBy("s_store_name").orderBy(ventas["unidades_vendidas"].desc())

resultado = ventas \
    .withColumn("ranking", rank().over(ventana)) \
    .filter("ranking <= 5") \
    .orderBy("s_store_name", "ranking")

resultado.show(truncate=False)

spark.stop()
