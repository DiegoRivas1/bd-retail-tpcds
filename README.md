# bd-retail-tpcds

Data Engineering para Retail utilizando Hive, Spark y LLM sobre Amazon EMR.
Trabajo Unidad II — BigData 2026.

---

## Descripción

Plataforma de análisis distribuido sobre un Data Warehouse Retail basado en el benchmark TPC-DS.
Implementa consultas analíticas en Apache Hive y Apache Spark, un benchmark comparativo de rendimiento
y una capa de análisis agéntico que interpreta preguntas en lenguaje natural y genera SQL automáticamente
usando la API de Gemini.

Stack:
- Amazon EMR (Hadoop, Hive, Spark)
- Python 3 + FastAPI (web app y agente)
- Gemini API (generación de SQL)
- HTML/CSS/JS (dashboard de visualización)
- LaTeX (informe)

---

## Estructura del repositorio

```
bd-retail-tpcds/
│
├── README.md
├── .gitignore
├── setup.sh                        # instala dependencias Python en el master EMR
├── .env.example                    # plantilla de variables de entorno
├── .env                            # clave real (no se sube al repo, ver .gitignore)
│
├── data/
│   └── README.md                   # instrucciones para generar datos TPC-DS (10 GB)
│
├── hive/
│   ├── crear_tablas.hql            # DDL de las 5 tablas obligatorias
│   └── consultas/
│       ├── q1_top_clientes_compras.hql
│       ├── q2_ventas_por_tienda.hql
│       ├── q3_ventas_por_mes.hql
│       ├── q4_ventas_por_dia.hql
│       ├── q5_top_productos_por_tienda.hql
│       ├── q6_ticket_promedio_cliente.hql
│       ├── q7_productos_mayor_ingreso.hql
│       ├── q8_top_clientes_gasto.hql
│       └── q9_ranking_mensual_ventas.hql
│
├── spark/
│   └── consultas/
│       ├── q1_top_clientes_compras.py
│       ├── q2_ventas_por_tienda.py
│       ├── q3_ventas_por_mes.py
│       ├── q4_ventas_por_dia.py
│       ├── q5_top_productos_por_tienda.py
│       ├── q6_ticket_promedio_cliente.py
│       ├── q7_productos_mayor_ingreso.py
│       ├── q8_top_clientes_gasto.py
│       └── q9_ranking_mensual_ventas.py
│
├── benchmark/
│   ├── ejecutar_hive.sh
│   ├── ejecutar_spark.sh
│   ├── generar_comparativa.py
│   └── resultados/
│       ├── hive_tiempos.csv
│       ├── spark_tiempos.csv
│       ├── comparativa.csv
│       └── comparativa_hive_vs_spark.png
│
├── agentic/
│   ├── agente.py                   # orquestador de skills
│   └── skills/
│       ├── clasificador_intencion.py
│       ├── generador_sql.py        # llama a Gemini API
│       ├── ejecutor_consulta.py    # ejecuta en Spark
│       └── formateador_resultado.py
│
├── webapp/
│   ├── app.py                      # FastAPI: endpoints REST y agente
│   ├── requirements.txt
│   ├── static/
│   │   ├── css/
│   │   │   └── estilos.css
│   │   └── js/
│   │       └── dashboard.js
│   └── templates/
│       └── index.html
│
└── informe/
    ├── main.tex
    ├── secciones/
    │   ├── marco_conceptual.tex
    │   ├── implementacion_hive.tex
    │   ├── implementacion_spark.tex
    │   ├── benchmark.tex
    │   ├── analisis_agenticoc.tex
    │   └── conclusiones.tex
    └── figuras/                    # capturas de pantalla para el informe
```

---

## Requisitos previos

### Configuración SSH y Wave Terminal

La conexión al master EMR y la configuración de Wave Terminal están documentadas en:

**[dev-environment-setup](https://github.com/DiegoRivas1/dev-environment-setup)**

El alias SSH utilizado en este proyecto es `aws-emr-lab`. Antes de continuar, asegurarse
de tener el archivo `~/.ssh/config` configurado con el DNS actual del master y el `.pem` correcto.

> Cada vez que se levanta un nuevo clúster EMR en Vocareum, el DNS del master cambia.
> Actualizar `HostName` en el config SSH antes de conectarse.

### JetBrains Gateway (desarrollo remoto)

Para editar y ejecutar desde el IDE directamente en el master:

1. Instalar [JetBrains Gateway](https://www.jetbrains.com/remote-development/gateway/)
2. Nueva conexión SSH → usar el alias `aws-emr-lab` o el DNS directo del master
3. Abrir la carpeta `~/bd-retail-tpcds/` en el master como proyecto remoto

El master EMR tiene Python 3, Spark y Hive disponibles. Todo se ejecuta ahí.

---

## Flujo de trabajo recomendado

```
PC local (JetBrains / editor)
    │
    ├── desarrollar código (webapp, agente, consultas)
    ├── git push → GitHub
    │
    └── cuando toca ejecutar contra datos reales:
            │
            ▼
        Levantar clúster EMR en Vocareum
        ssh aws-emr-lab
        git clone / git pull ~/bd-retail-tpcds
        cargar datos TPC-DS a HDFS
        ejecutar consultas y benchmarks
        guardar resultados en benchmark/resultados/
        git push resultados
        APAGAR el clúster  ← importante para no gastar créditos
```

> Desarrollar todo el código en local. Encender el clúster solo para ejecución real.
> Siempre hacer commit antes de terminar la sesión.

---

## Configuración del entorno en el master

### 1. Clonar el repositorio

```bash
git clone https://github.com/DiegoRivas1/bd-retail-tpcds.git
cd bd-retail-tpcds
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env y reemplazar tu_api_key_aqui con la clave real
```

Obtener la key de Gemini en: https://aistudio.google.com/api-keys

El `.env` está en `.gitignore`, la clave nunca llega a GitHub.

### 3. Instalar dependencias Python

```bash
bash setup.sh
```

`setup.sh` instala:

```bash
pip install fastapi uvicorn pyspark google-generativeai pandas matplotlib
```

### 4. Configurar la API key de Gemini

```bash
export GEMINI_API_KEY="tu_api_key_aqui"
```

Obtener la key en: https://aistudio.google.com/api-keys

---

## Generación de datos TPC-DS

Ver instrucciones detalladas en `data/README.md`.

Opciones:
- Generar 10 GB localmente con [tpcds-kit](https://github.com/gregrahn/tpcds-kit) y subir a HDFS
- Usar un dataset TPC-DS ya generado (> 10 GB) disponible en S3 público

Tablas obligatorias que deben estar en HDFS antes de ejecutar las consultas:

| Tabla | Descripción |
|---|---|
| `customer` | Datos de clientes |
| `item` | Catálogo de productos |
| `store` | Tiendas físicas |
| `date_dim` | Dimensión de fechas |
| `store_sales` | Transacciones de ventas |

### Cargar tablas en Hive

```bash
hive -f hive/crear_tablas.hql
```

---

## Ejecución

### Consultas Hive

```bash
# Ejecutar una consulta individual
hive -f hive/consultas/q1_top_clientes_compras.hql

# Ejecutar todas y registrar tiempos
bash benchmark/ejecutar_hive.sh
```

### Consultas Spark

```bash
# Ejecutar una consulta individual
spark-submit spark/consultas/q1_top_clientes_compras.py

# Ejecutar todas y registrar tiempos
bash benchmark/ejecutar_spark.sh
```

### Benchmark comparativo

```bash
# Ejecutar benchmark Hive (genera benchmark/resultados/hive_tiempos.csv)
bash benchmark/ejecutar_hive.sh

# Ejecutar benchmark Spark (genera benchmark/resultados/spark_tiempos.csv)
bash benchmark/ejecutar_spark.sh

# Generar tabla comparativa y gráfico PNG
python benchmark/generar_comparativa.py
```

### Web app (dashboard + agente)

```bash
cd webapp
uvicorn app:app --host 0.0.0.0 --port 8000
```

Acceder desde el navegador via túnel SSH:

```powershell
# En PowerShell local (Windows)
ssh -L 8000:localhost:8000 aws-emr-lab
```

Luego abrir: http://localhost:8000

---

## Módulos

### Hive y Spark

Las 9 consultas analíticas están implementadas en ambos frameworks con la misma lógica:

- Top 20 clientes con mayor número de compras
- Ventas por tienda
- Ventas por mes
- Ventas por día de la semana
- Top productos por tienda
- Ticket promedio por cliente
- Productos con mayor ingreso generado
- Top clientes por gasto total
- Ranking mensual de ventas

### Benchmark

`benchmark/ejecutar_hive.sh` y `benchmark/ejecutar_spark.sh` ejecutan las consultas
en secuencia, registran tiempo de ejecución, uso de CPU y memoria, y guardan los
resultados en `benchmark/resultados/` como CSV para análisis comparativo.

### Capa agéntica

El agente recibe una pregunta en lenguaje natural y ejecuta el siguiente pipeline de skills:

```
pregunta en lenguaje natural
        │
        ▼
clasificador_intencion.py   → identifica la consulta analítica solicitada
        │
        ▼
generador_sql.py            → llama a Gemini API y genera SQL compatible con Spark SQL
        │
        ▼
ejecutor_consulta.py        → ejecuta el SQL generado en Spark
        │
        ▼
formateador_resultado.py    → devuelve tabla o gráfico al dashboard
```

Consultas agénticas implementadas:

- ¿Cuáles fueron los cinco productos más vendidos?
- ¿Qué tienda tuvo mayores ventas?
- ¿Cuál fue el mes con mayores ingresos?
- ¿Cuáles son los diez mejores clientes?
- ¿Qué producto generó mayores ingresos?
- (+ 5 consultas adicionales en lenguaje natural)

### Web app

FastAPI sirve el dashboard y expone los endpoints del agente. El frontend muestra
gráficos comparativos Hive vs Spark y permite ingresar consultas en lenguaje natural.

---

## Informe

El informe en LaTeX está en `informe/`. Compilar con pdfLaTeX:

```bash
cd informe
pdflatex main.tex
```

Las capturas de pantalla van en `informe/figuras/` y se referencian desde los `.tex`.

---

## Capturas recomendadas para el informe

| # | Qué capturar | Cuándo |
|---|---|---|
| 1 | Cluster EMR activo en consola AWS | Al levantar el clúster |
| 2 | Tablas cargadas en Hive (`show tables`) | Después de `crear_tablas.hql` |
| 3 | Resultado de una consulta Hive en terminal | Durante ejecución |
| 4 | Resultado de la misma consulta en Spark | Durante ejecución |
| 5 | Tabla comparativa de tiempos Hive vs Spark | Del CSV de benchmark |
| 6 | Dashboard web con gráficos de ventas | Con la webapp corriendo |
| 7 | Consulta agéntica en lenguaje natural y su resultado | Con la webapp corriendo |
| 8 | Gráfico de barras comparativo Hive vs Spark | Del dashboard |

---

## Referencias

- [TPC-DS Benchmark](https://www.tpc.org/tpcds/)
- [tpcds-kit (generador de datos)](https://github.com/gregrahn/tpcds-kit)
- [Gemini API](https://ai.google.dev/gemini-api/docs)
- [Apache Hive](https://hive.apache.org/)
- [Apache Spark](https://spark.apache.org/)
- [dev-environment-setup](https://github.com/DiegoRivas1/dev-environment-setup)