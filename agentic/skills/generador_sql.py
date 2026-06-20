# generador_sql.py
# Skill 2: genera una consulta SQL compatible con Spark SQL
# a partir de una pregunta en lenguaje natural usando la API de Gemini.

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

ESQUEMA = """
Base de datos: retail (TPC-DS)

Tablas disponibles:

customer (c_customer_sk, c_first_name, c_last_name, c_email_address,
          c_birth_year, c_birth_country)

item (i_item_sk, i_product_name, i_category, i_brand,
      i_current_price, i_wholesale_cost)

store (s_store_sk, s_store_name, s_city, s_state, s_country)

date_dim (d_date_sk, d_date, d_year, d_moy, d_dow, d_day_name,
          d_quarter_name)

store_sales (ss_sold_date_sk, ss_item_sk, ss_customer_sk, ss_store_sk,
             ss_ticket_number, ss_quantity, ss_net_paid, ss_net_profit,
             ss_sales_price, ss_ext_discount_amt)

Relaciones:
- store_sales.ss_customer_sk -> customer.c_customer_sk
- store_sales.ss_item_sk     -> item.i_item_sk
- store_sales.ss_store_sk    -> store.s_store_sk
- store_sales.ss_sold_date_sk -> date_dim.d_date_sk

Notas:
- Usar siempre USE retail; al inicio.
- d_dow: 0=domingo, 1=lunes, ..., 6=sabado.
- Para ingresos usar ss_net_paid.
- Para unidades usar ss_quantity.
- El SQL debe ser compatible con Spark SQL.
"""

PROMPT_SISTEMA = f"""
Eres un experto en SQL y analisis de datos retail.
Tu unica tarea es generar consultas SQL compatibles con Spark SQL
a partir de preguntas en lenguaje natural.

{ESQUEMA}

Reglas:
- Responde UNICAMENTE con la consulta SQL, sin explicaciones ni comentarios.
- No uses bloques de codigo markdown, solo el SQL puro.
- Usa alias descriptivos en español para las columnas del resultado.
- Incluye USE retail; al inicio de cada consulta.
"""


def generar_sql(pregunta: str) -> str:
    """
    Recibe una pregunta en lenguaje natural y retorna una consulta
    SQL generada por Gemini compatible con Spark SQL.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no configurada. Verificar archivo ..env")

    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        system_instruction=PROMPT_SISTEMA,
    )

    respuesta = modelo.generate_content(pregunta)
    sql = respuesta.text.strip()

    return sql
