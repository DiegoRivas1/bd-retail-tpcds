from pyspark.sql import SparkSession
import os

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-amazon-corretto.x86_64"
os.environ["SPARK_SUBMIT_OPTS"] = "--add-opens=java.base/java.lang=ALL-UNNAMED"

_spark = None  # 👈 IMPORTANTE: variable global

def obtener_sesion_spark() -> SparkSession:
    global _spark

    if _spark is None:
        _spark = (
            SparkSession.builder
            .appName("agente_retail")
            .enableHiveSupport()
            .getOrCreate()
        )

    return _spark


def ejecutar(sql: str) -> dict:
    spark = obtener_sesion_spark()

    try:
        df = spark.sql(sql)
        columnas = df.columns
        filas = [row.asDict() for row in df.collect()]

        return {
            "exito": True,
            "columnas": columnas,
            "filas": filas,
            "total": len(filas),
        }

    except Exception as error:
        return {
            "exito": False,
            "error": str(error),
            "columnas": [],
            "filas": [],
            "total": 0,
        }