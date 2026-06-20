#!/bin/bash

# setup.sh
# Instala dependencias Python necesarias en el master EMR.
# Ejecutar una sola vez despues de clonar el repositorio.
# Uso: bash setup.sh

set -e

echo "Instalando dependencias Python..."

pip install \
    fastapi \
    uvicorn \
    pyspark \
    google-generativeai \
    pandas \
    matplotlib \
    jinja2 \
    python-dotenv \
    httpx

echo "Verificando archivo .env..."

if [ -f ".env" ]; then
    # shellcheck disable=SC2046
    export $(grep -v '^#' ..env | xargs)
    echo "Archivo .env cargado."
else
    echo ""
    echo "AVISO: No se encontro el archivo .env."
    echo "Crear el archivo .env en la raiz del proyecto basandose en .env.example:"
    echo ""
    echo "    cp .env.example .env"
    echo "    # editar .env y reemplazar tu_api_key_aqui con la clave real"
    echo ""
    echo "Obtener la key en: https://aistudio.google.com/api-keys"
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "AVISO: GEMINI_API_KEY sigue sin configurarse. La capa agéntica no funcionara sin ella."
else
    echo "GEMINI_API_KEY configurada correctamente."
fi

echo ""
echo "Setup completado."
echo "Siguiente paso: cargar datos TPC-DS a HDFS y ejecutar hive/crear_tablas.hql"