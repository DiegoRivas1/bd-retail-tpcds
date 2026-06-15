# agente.py
# Orquestador del pipeline de analisis agéntico.
# Coordina los 4 skills en secuencia para responder
# preguntas en lenguaje natural sobre el Data Warehouse retail.

from agentic.skills.clasificador_intencion import clasificar
from agentic.skills.generador_sql import generar_sql
from agentic.skills.ejecutor_consulta import ejecutar
from agentic.skills.formateador_resultado import formatear


def responder(pregunta: str) -> dict:
    """
    Pipeline completo:
      1. Clasificar la intencion de la pregunta.
      2. Generar SQL con Gemini.
      3. Ejecutar el SQL en Spark.
      4. Formatear y retornar el resultado.
    """
    # 1. Clasificar intencion
    intencion = clasificar(pregunta)

    # 2. Generar SQL con Gemini
    try:
        sql = generar_sql(pregunta)
    except ValueError as error:
        return {
            "exito": False,
            "pregunta": pregunta,
            "intencion": intencion,
            "sql": "",
            "mensaje": str(error),
            "columnas": [],
            "filas": [],
            "total": 0,
        }

    # 3. Ejecutar en Spark
    resultado = ejecutar(sql)

    # 4. Formatear respuesta
    respuesta = formatear(pregunta, sql, resultado)
    respuesta["intencion"] = intencion

    return respuesta
