# bd-retail-tpcds

Data Engineering para Retail utilizando Hive, Spark y LLM sobre Amazon EMR.
Trabajo Unidad II, BigData 2026A

---

## Descripción

Plataforma de análisis distribuido sobre un Data Warehouse Retail basado en el benchmark TPC-DS.
Implementa consultas analíticas en Apache Hive y Apache Spark, un benchmark comparativo de rendimiento
y una capa de análisis agéntico que interpreta preguntas en lenguaje natural y genera SQL automáticamente
usando la API de Gemini.

Stack:
- Amazon EMR 7.13.0 (Hadoop 3.4.2, Hive 3.1.3, Spark 3.5.6, Tez 0.10.2)
- Python 3 + FastAPI (web app y agente)
- Gemini API: gemini-2.5-flash (generación de SQL)
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
    │   ├── caratula.tex
    │   ├── marco_conceptual.tex
    │   ├── implementacion_hive.tex
    │   ├── implementacion_spark.tex
    │   ├── benchmark.tex
    │   ├── analitico_agéntico.tex
    │   ├── conclusiones.tex
    │   └── repositorio.tex
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

---

## Configuración del clúster EMR

Al crear el clúster en la consola AWS, usar la siguiente configuración:

| Parámetro | Valor |
|---|---|
| Versión EMR | emr-7.13.0 |
| Aplicaciones | Custom: Hadoop + Hive + Spark + Tez + HCatalog |
| Nodo master | m5.xlarge |
| Nodos core | 2 x m5.xlarge |
| EBS master | **50 GB** (ajustar en configuración avanzada al crear) |
| AWS Glue | Desactivado |

> El volumen EBS debe configurarse en 50 GB al momento de crear el clúster
> no después. Esto evita tener que ejecutar `growpart` manualmente.

---

## Flujo de trabajo recomendado

```
PC local (editor)
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
        generar datos TPC-DS y cargar a HDFS (ver data/README.md)
        ejecutar consultas y benchmarks
        guardar resultados en benchmark/resultados/
        git push resultados
        APAGAR el clúster  ← importante para no gastar créditos
```

> Desarrollar todo el código en local. Encender el clúster solo para ejecución real.
> Siempre hacer commit antes de terminar la sesión.

---

## Configuración del entorno en el master

### 1. Instalar git y clonar el repositorio

```bash
sudo yum install -y git
git clone https://github.com/DiegoRivas1/bd-retail-tpcds.git
cd bd-retail-tpcds
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
nano .env
# Reemplazar tu_api_key_aqui con la clave real de Gemini
# Guardar con Ctrl+O, salir con Ctrl+X
```

Obtener la key de Gemini en: https://aistudio.google.com/api-keys

El `.env` está en `.gitignore` la clave nunca llega a GitHub.

### 3. Instalar dependencias Python

```bash
bash setup.sh
source ~/.bashrc
```

`setup.sh` configura el PATH, instala las dependencias y carga el `.env` automáticamente.

### 4. Configurar PYTHONPATH para PySpark del sistema

```bash
export PYTHONPATH=/usr/lib/spark/python:/usr/lib/spark/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH
echo 'export PYTHONPATH=/usr/lib/spark/python:/usr/lib/spark/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc
```

> Esto es necesario para que la webapp pueda importar PySpark usando el Spark
> del cluster EMR en lugar del instalado por pip, evitando conflictos de versión de Java.

---

## Generación de datos TPC-DS

Ver instrucciones detalladas en `data/README.md`.

Tablas obligatorias que deben estar en HDFS:

| Tabla | Descripción |
|---|---|
| `customer` | Datos de clientes |
| `item` | Catálogo de productos |
| `store` | Tiendas físicas |
| `date_dim` | Dimensión de fechas |
| `store_sales` | Transacciones de ventas (~28.8M filas con 10 GB) |

### Cargar tablas en Hive

```bash
cd ~/bd-retail-tpcds
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
/usr/bin/spark-submit spark/consultas/q1_top_clientes_compras.py

# Ejecutar todas y registrar tiempos
bash benchmark/ejecutar_spark.sh
```

> Usar siempre `/usr/bin/spark-submit` y no `spark-submit` directamente.
> El PATH puede apuntar al spark-submit de pip que genera conflictos de versión Java.

### Benchmark comparativo

```bash
bash benchmark/ejecutar_hive.sh
bash benchmark/ejecutar_spark.sh
python benchmark/generar_comparativa.py
```

Resultados en `benchmark/resultados/`:

| Archivo | Contenido |
|---|---|
| `hive_tiempos.csv` | Tiempos por consulta en Hive |
| `spark_tiempos.csv` | Tiempos por consulta en Spark |
| `comparativa.csv` | Tabla unificada con speedup Spark vs Hive |
| `comparativa_hive_vs_spark.png` | Gráfico de barras para el informe |

### Web app (dashboard + agente)

```bash
cd ~/bd-retail-tpcds/webapp
uvicorn app:app --host 0.0.0.0 --port 8000
```

Acceder desde el navegador via túnel SSH:

```powershell
# En PowerShell local (Windows)
ssh -L 8000:localhost:8000 aws-emr-lab
```

Luego abrir: http://localhost:8000

> La primera consulta agéntica tarda ~40-60s porque inicializa la SparkSession en YARN.
> Las siguientes son más rápidas al reutilizar la sesión.

---

## Resultados del benchmark

Tiempos obtenidos sobre dataset TPC-DS 10 GB en EMR 7.13.0 (m5.xlarge, 3 nodos):

| Consulta | Hive (s) | Spark (s) | Speedup |
|---|---|---|---|
| Q1 Top clientes por compras | 45.09 | 37.33 | 1.21x |
| Q2 Ventas por tienda | 37.38 | 38.72 | 0.97x |
| Q3 Ventas por mes | 37.72 | 33.15 | 1.14x |
| Q4 Ventas por día | 37.90 | 34.41 | 1.10x |
| Q5 Top productos por tienda | 63.47 | 41.23 | 1.54x |
| Q6 Ticket promedio cliente | 58.67 | 37.66 | 1.56x |
| Q7 Productos mayor ingreso | 48.27 | 36.73 | 1.31x |
| Q8 Top clientes por gasto | 56.48 | 39.01 | 1.45x |
| Q9 Ranking mensual ventas | 39.47 | 34.18 | 1.15x |
| **Total** | **424.45** | **332.42** | **1.28x** |

---

## Informe

El informe en LaTeX está en `informe/`. Compilar con pdfLaTeX:

```bash
cd informe
pdflatex main.tex
```

Las capturas van en `informe/figuras/`.

---

## Referencias

- [TPC-DS Benchmark](https://www.tpc.org/tpcds/)
- [tpcds-kit](https://github.com/gregrahn/tpcds-kit)
- [Gemini API](https://ai.google.dev/gemini-api/docs)
- [Apache Hive](https://hive.apache.org/)
- [Apache Spark](https://spark.apache.org/)
- [dev-environment-setup](https://github.com/DiegoRivas1/dev-environment-setup)