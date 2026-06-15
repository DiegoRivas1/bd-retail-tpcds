# Datos TPC-DS

Instrucciones para generar o descargar el dataset TPC-DS de 10 GB
y cargarlo en HDFS para su uso con Hive y Spark.

---

## Opcion A: Generar los datos con tpcds-kit (recomendado)

### 1. Clonar y compilar tpcds-kit en el master EMR

```bash
sudo yum install -y gcc make git
git clone https://github.com/gregrahn/tpcds-kit.git
cd tpcds-kit/tools
make OS=LINUX
```

### 2. Generar los datos (10 GB)

```bash
mkdir -p ~/tpcds-data
cd tpcds-kit/tools

./dsdgen \
    -SCALE 10 \
    -DIR ~/tpcds-data \
    -TERMINATE N \
    -PARALLEL 4
```

`-SCALE 10` genera aproximadamente 10 GB distribuidos en los archivos `.dat`.
`-PARALLEL 4` divide la generacion en 4 procesos para aprovechar los nucleos del master.

Los archivos generados siguen el patron `<tabla>_<parte>.dat` cuando se usa paralelismo,
por ejemplo `store_sales_1_4.dat`, `store_sales_2_4.dat`, etc.

El tiempo de generacion en un master EMR m5.xlarge es aproximadamente 20-30 minutos.

### 3. Verificar los archivos generados

```bash
ls -lh ~/tpcds-data/*.dat
```

Las 5 tablas obligatorias deben estar presentes:

```
customer.dat
item.dat
store.dat
date_dim.dat
store_sales_*.dat
```

---

## Opcion B: Usar un dataset ya generado desde S3

Si ya existe un dataset TPC-DS disponible en S3 del lab de Vocareum,
copiarlo directamente a HDFS:

```bash
aws s3 cp s3://<bucket>/tpcds/ /tmp/tpcds-data/ --recursive
```

Consultar con el docente si hay un bucket S3 compartido para el curso.

---

## Cargar los datos en HDFS

### 1. Crear directorios en HDFS

```bash
hadoop fs -mkdir -p /user/hadoop/tpcds/customer
hadoop fs -mkdir -p /user/hadoop/tpcds/item
hadoop fs -mkdir -p /user/hadoop/tpcds/store
hadoop fs -mkdir -p /user/hadoop/tpcds/date_dim
hadoop fs -mkdir -p /user/hadoop/tpcds/store_sales
```

### 2. Subir los archivos

```bash
hadoop fs -put ~/tpcds-data/customer.dat      /user/hadoop/tpcds/customer/
hadoop fs -put ~/tpcds-data/item.dat          /user/hadoop/tpcds/item/
hadoop fs -put ~/tpcds-data/store.dat         /user/hadoop/tpcds/store/
hadoop fs -put ~/tpcds-data/date_dim.dat      /user/hadoop/tpcds/date_dim/
hadoop fs -put ~/tpcds-data/store_sales*.dat  /user/hadoop/tpcds/store_sales/
```

> Si se genero con `-PARALLEL`, los archivos de `store_sales` seran multiples.
> El wildcard `store_sales*.dat` los sube todos de una vez.

### 3. Verificar en HDFS

```bash
hadoop fs -ls /user/hadoop/tpcds/
hadoop fs -du -h /user/hadoop/tpcds/
```

La salida esperada debe mostrar los 5 directorios con datos.

---

## Crear las tablas en Hive

Una vez los datos esten en HDFS, ejecutar el DDL:

```bash
cd ~/bd-retail-tpcds
hive -f hive/crear_tablas.hql
```

Verificar que las tablas quedaron creadas:

```bash
hive -e "USE retail; SHOW TABLES;"
```

Salida esperada:

```
customer
date_dim
item
store
store_sales
```

---

## Verificar con una consulta rapida

```bash
hive -e "USE retail; SELECT COUNT(*) FROM store_sales;"
```

Con 10 GB de datos, `store_sales` debe tener aproximadamente 28-30 millones de filas.

---

## Notas

- Los archivos `.dat` no se suben al repositorio por su tamaño.
- El directorio `~/tpcds-data/` en el master es temporal, se pierde al apagar el cluster.
- Los datos en HDFS persisten mientras el cluster este activo.
- Si se reinicia el cluster, repetir los pasos de carga desde la Opcion A o B.
- Documentacion oficial TPC-DS: https://www.tpc.org/tpcds/
- Repositorio tpcds-kit: https://github.com/gregrahn/tpcds-kit
