# q7_productos_mayor_ingreso.py
# Productos con mayor ingreso total generado.
# Uso: spark-submit spark/consultas/q7_productos_mayor_ingreso.py

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("q7_productos_mayor_ingreso") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("USE retail")

resultado = spark.sql("""
    SELECT
        i.i_item_sk,
        i.i_product_name,
        i.i_category,
        i.i_brand,
        SUM(ss.ss_quantity)  AS unidades_vendidas,
        SUM(ss.ss_net_paid)  AS ingresos_totales
    FROM store_sales ss
    JOIN item i ON ss.ss_item_sk = i.i_item_sk
    GROUP BY
        i.i_item_sk,
        i.i_product_name,
        i.i_category,
        i.i_brand
    ORDER BY ingresos_totales DESC
    LIMIT 20
""")

resultado.show(truncate=False)

spark.stop()
