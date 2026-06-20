#!/bin/bash

# setup.sh
# Instala dependencias Python necesarias en el master EMR,
# configura el PATH y carga la API key de Gemini desde .env.
# Ejecutar una sola vez despues de clonar el repositorio.
# Uso: bash setup.sh

set -e

# 1. PATH
echo "Configurando PATH..."

LOCAL_BIN="$HOME/.local/bin"

if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    export PATH="$LOCAL_BIN:$PATH"
    echo "export PATH=\"$LOCAL_BIN:\$PATH\"" >> ~/.bashrc
    echo "  PATH actualizado: $LOCAL_BIN agregado."
else
    echo "  PATH ya contiene $LOCAL_BIN."
fi

# 2. Dependencias Python
echo ""
echo "Instalando dependencias Python..."

pip install \
    fastapi \
    uvicorn \
#    pyspark \
    google-generativeai \
    pandas \
    matplotlib \
    jinja2 \
    python-dotenv \
    httpx

# 3. Cargar .env
echo ""
echo "Verificando archivo .env..."

if [ ! -f ".env" ]; then
    echo ""
    echo "AVISO: No se encontro el archivo .env."
    echo "Crearlo con:"
    echo ""
    echo "    cp .env.example .env"
    echo "    nano .env  # reemplazar tu_api_key_aqui con la clave real"
    echo ""
    echo "Obtener la key en: https://aistudio.google.com/api-keys"
else
    # Leer el .env linea por linea para evitar problemas con xargs
    while IFS='=' read -r clave valor; do
        # ignorar lineas vacias y comentarios
        [[ -z "$clave" || "$clave" == \#* ]] && continue
        # quitar espacios y comillas del valor
        valor=$(echo "$valor" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | tr -d '"' | tr -d "'")
        export "$clave"="$valor"
        # agregar al .bashrc solo si no existe ya
        if ! grep -q "export $clave=" ~/.bashrc 2>/dev/null; then
            echo "export $clave=\"$valor\"" >> ~/.bashrc
        fi
    done < .env
    echo "  Archivo .env cargado y variables exportadas a ~/.bashrc."
fi

#  4. Verificar GEMINI_API_KEY
echo ""
if [ -z "$GEMINI_API_KEY" ]; then
    echo "AVISO: GEMINI_API_KEY no esta configurada. La capa agéntica no funcionara sin ella."
else
    echo "GEMINI_API_KEY configurada correctamente."
fi

#  5. Resumen
echo ""
echo "Setup completado."
echo "Ejecutar 'source ~/.bashrc' o abrir una nueva terminal para aplicar los cambios de PATH."
echo "Siguiente paso: cargar datos TPC-DS a HDFS y ejecutar hive/crear_tablas.hql"