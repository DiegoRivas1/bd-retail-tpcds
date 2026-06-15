# clasificador_intencion.py
# Skill 1: identifica la intencion analitica de una pregunta en lenguaje natural.

INTENCIONES = {
    "top_productos": [
        "productos mas vendidos",
        "productos vendidos",
        "articulos mas vendidos",
        "items mas vendidos",
        "productos populares",
    ],
    "ventas_tienda": [
        "tienda con mayores ventas",
        "tienda mas ventas",
        "mejor tienda",
        "tiendas ventas",
        "ventas por tienda",
    ],
    "ventas_mes": [
        "mes con mayores ingresos",
        "mes con mas ventas",
        "mejor mes",
        "ventas por mes",
        "ingresos por mes",
        "mes mas rentable",
    ],
    "top_clientes": [
        "mejores clientes",
        "clientes con mas compras",
        "top clientes",
        "clientes mas fieles",
        "clientes mayor gasto",
    ],
    "productos_ingresos": [
        "producto genero mayores ingresos",
        "producto mas rentable",
        "productos mayor ingreso",
        "productos mas rentables",
        "mayor ingreso producto",
    ],
    "ventas_dia": [
        "ventas por dia",
        "dia con mas ventas",
        "mejor dia de la semana",
        "dia mas rentable",
    ],
    "ticket_promedio": [
        "ticket promedio",
        "gasto promedio por cliente",
        "promedio de compra",
        "compra promedio",
    ],
    "ranking_mensual": [
        "ranking mensual",
        "ranking de tiendas por mes",
        "tiendas por mes",
        "ranking ventas mensual",
    ],
}


def clasificar(pregunta: str) -> str:
    """
    Recibe una pregunta en lenguaje natural y retorna la intencion identificada.
    Si no se encuentra coincidencia retorna 'desconocida'.
    """
    pregunta_lower = pregunta.lower()

    for intencion, palabras_clave in INTENCIONES.items():
        for frase in palabras_clave:
            if frase in pregunta_lower:
                return intencion

    return "desconocida"
