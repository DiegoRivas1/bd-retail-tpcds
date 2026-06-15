# formateador_resultado.py
# Skill 4: convierte el resultado del ejecutor en una estructura
# lista para devolver como respuesta JSON desde la webapp.


def formatear(pregunta: str, sql: str, resultado: dict) -> dict:
    """
    Recibe la pregunta original, el SQL generado y el resultado del ejecutor.
    Retorna una respuesta estructurada lista para el frontend.
    """
    if not resultado["exito"]:
        return {
            "exito": False,
            "pregunta": pregunta,
            "sql": sql,
            "mensaje": f"Error al ejecutar la consulta: {resultado['error']}",
            "columnas": [],
            "filas": [],
            "total": 0,
        }

    filas_serializables = []
    for fila in resultado["filas"]:
        fila_limpia = {}
        for clave, valor in fila.items():
            if valor is None:
                fila_limpia[clave] = None
            elif isinstance(valor, float):
                fila_limpia[clave] = round(valor, 2)
            else:
                fila_limpia[clave] = valor
        filas_serializables.append(fila_limpia)

    return {
        "exito": True,
        "pregunta": pregunta,
        "sql": sql,
        "columnas": resultado["columnas"],
        "filas": filas_serializables,
        "total": resultado["total"],
    }
