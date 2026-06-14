#!/bin/bash

# ejecutar_spark.sh
# Ejecuta las 9 consultas Spark en secuencia y registra tiempos de ejecucion.
# Uso: bash benchmark/ejecutar_spark.sh
# Resultados: benchmark/resultados/spark_tiempos.csv

set -e

# Directorio raiz del repo (donde esta este script, un nivel arriba)
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"

DIRECTORIO_CONSULTAS="$RAIZ/spark/consultas"
DIRECTORIO_RESULTADOS="$RAIZ/benchmark/resultados"
ARCHIVO_SALIDA="$DIRECTORIO_RESULTADOS/spark_tiempos.csv"

mkdir -p "$DIRECTORIO_RESULTADOS"

echo "consulta,tiempo_segundos,estado" > "$ARCHIVO_SALIDA"

consultas=(
    "q1_top_clientes_compras"
    "q2_ventas_por_tienda"
    "q3_ventas_por_mes"
    "q4_ventas_por_dia"
    "q5_top_productos_por_tienda"
    "q6_ticket_promedio_cliente"
    "q7_productos_mayor_ingreso"
    "q8_top_clientes_gasto"
    "q9_ranking_mensual_ventas"
)

echo "Iniciando benchmark Spark..."
echo "Resultados en: $ARCHIVO_SALIDA"
echo ""

for consulta in "${consultas[@]}"; do
    archivo="$DIRECTORIO_CONSULTAS/${consulta}.py"

    if [ ! -f "$archivo" ]; then
        echo "AVISO: No se encontro $archivo, omitiendo."
        echo "$consulta,0,no_encontrado" >> "$ARCHIVO_SALIDA"
        continue
    fi

    echo "Ejecutando $consulta..."
    inicio=$(date +%s%N)

    if spark-submit \
        --master yarn \
        --deploy-mode client \
        "$archivo" > /dev/null 2>&1; then
        fin=$(date +%s%N)
        tiempo=$(( (fin - inicio) / 1000000 ))
        tiempo_seg=$(echo "scale=3; $tiempo / 1000" | bc)
        estado="ok"
        echo "  OK - ${tiempo_seg}s"
    else
        fin=$(date +%s%N)
        tiempo=$(( (fin - inicio) / 1000000 ))
        tiempo_seg=$(echo "scale=3; $tiempo / 1000" | bc)
        estado="error"
        echo "  ERROR - ${tiempo_seg}s"
    fi

    echo "$consulta,$tiempo_seg,$estado" >> "$ARCHIVO_SALIDA"
done

echo ""
echo "Benchmark Spark completado."
echo "Resultados guardados en: $ARCHIVO_SALIDA"