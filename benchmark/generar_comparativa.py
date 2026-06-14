# generar_comparativa.py
# Combina los resultados de Hive y Spark en una tabla comparativa
# y genera un grafico de barras.
# Uso: python benchmark/generar_comparativa.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

DIRECTORIO = "benchmark/resultados"
ARCHIVO_HIVE  = os.path.join(DIRECTORIO, "hive_tiempos.csv")
ARCHIVO_SPARK = os.path.join(DIRECTORIO, "spark_tiempos.csv")
ARCHIVO_COMP  = os.path.join(DIRECTORIO, "comparativa.csv")
ARCHIVO_GRAF  = os.path.join(DIRECTORIO, "comparativa_hive_vs_spark.png")

hive  = pd.read_csv(ARCHIVO_HIVE).rename(columns={"tiempo_segundos": "hive_seg", "estado": "estado_hive"})
spark = pd.read_csv(ARCHIVO_SPARK).rename(columns={"tiempo_segundos": "spark_seg", "estado": "estado_spark"})

comparativa = hive.merge(spark, on="consulta")
comparativa["diferencia_seg"] = comparativa["hive_seg"] - comparativa["spark_seg"]
comparativa["speedup"] = (comparativa["hive_seg"] / comparativa["spark_seg"]).round(2)

comparativa.to_csv(ARCHIVO_COMP, index=False)
print("Tabla comparativa guardada en:", ARCHIVO_COMP)
print()
print(comparativa[["consulta", "hive_seg", "spark_seg", "diferencia_seg", "speedup"]].to_string(index=False))

fig, ax = plt.subplots(figsize=(12, 6))

x = range(len(comparativa))
ancho = 0.35

barras_hive  = ax.bar([i - ancho/2 for i in x], comparativa["hive_seg"],  ancho, label="Hive",  color="#E07B39")
barras_spark = ax.bar([i + ancho/2 for i in x], comparativa["spark_seg"], ancho, label="Spark", color="#3A86C8")

ax.set_xlabel("Consulta", fontsize=11)
ax.set_ylabel("Tiempo de ejecucion (segundos)", fontsize=11)
ax.set_title("Benchmark Hive vs Spark — Tiempo de ejecucion por consulta", fontsize=13, fontweight="bold")
ax.set_xticks(list(x))
ax.set_xticklabels(comparativa["consulta"], rotation=30, ha="right", fontsize=9)
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f s"))
ax.legend(fontsize=11)
ax.grid(axis="y", linestyle="--", alpha=0.5)

fig.tight_layout()
fig.savefig(ARCHIVO_GRAF, dpi=150)
print()
print("Grafico guardado en:", ARCHIVO_GRAF)
