# ejecutor_consulta.py
# Skill 3: ejecuta una consulta SQL en Spark y retorna los resultados
# como lista de diccionarios lista para serializar a JSON.

from pyspark.sql import SparkSession

def obtener_sesion_spark() -> SparkSession:
    global _spark

    if _spark is None:
        _spark = (
            SparkSession.builder
            .appName("agente_retail")
            .master("local[*]")
            .getOrCreate()
        )

    return _spark
#def obtener_sesion_spark() -> SparkSession:
#   return SparkSession.builder \
#      .appName("agente_retail") \
#     .enableHiveSupport() \
#    .getOrCreate()


def ejecutar(sql: str) -> dict:
    """
    Ejecuta una consulta SQL en Spark SQL.
    Retorna un diccionario con columnas, filas y total de registros.
    En caso de error retorna el mensaje de excepcion.
    """
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
