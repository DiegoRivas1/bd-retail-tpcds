# Datos TPC-DS

Instrucciones para generar o descargar el dataset TPC-DS de 10 GB
y cargarlo en HDFS para su uso con Hive y Spark.

---

## Opcion A: Generar los datos con tpcds-kit (recomendado)

### 0. Ampliar el volumen EBS del master

El volumen raíz del master EMR tiene 15 GB por defecto, insuficiente para generar 10 GB de datos. Antes de continuar, ampliar a 50 GB desde la consola AWS:

1. Ir a EC2 → Instances → seleccionar la instancia Primary del cluster
2. Pestaña Storage → click en el Volume ID
3. Actions → Modify Volume → cambiar a 50 GiB → Modify

Luego en el master aplicar el cambio:

```bash
sudo growpart /dev/xvda 1
sudo xfs_growfs /
df -h /
```

La salida debe mostrar ~50 GB disponibles antes de continuar.

### 1. Instalar dependencias y compilar tpcds-kit

Clonar fuera del repositorio del proyecto, directamente en el home:

```bash
sudo yum install -y gcc make git bison byacc flex

git clone https://github.com/gregrahn/tpcds-kit.git ~/tpcds-kit
cd ~/tpcds-kit/tools
make OS=LINUX CFLAGS="-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DYYDEBUG -DLINUX -g -fcommon"
```

Verificar que compiló correctamente:

```bash
ls -la ~/tpcds-kit/tools/dsdgen
```

### 2. Generar los datos (10 GB)

```bash
mkdir -p /home/hadoop/tpcds-data
cd ~/tpcds-kit/tools

# Tablas globales — generadas secuencialmente para evitar colisiones de escritura
./dsdgen -SCALE 10 -DIR /home/hadoop/tpcds-data -TERMINATE N -FORCE Y -TABLE customer
./dsdgen -SCALE 10 -DIR /home/hadoop/tpcds-data -TERMINATE N -FORCE Y -TABLE item
./dsdgen -SCALE 10 -DIR /home/hadoop/tpcds-data -TERMINATE N -FORCE Y -TABLE store
./dsdgen -SCALE 10 -DIR /home/hadoop/tpcds-data -TERMINATE N -FORCE Y -TABLE date_dim

# store_sales — generada en paralelo con 4 procesos separados
./dsdgen -SCALE 10 -DIR /home/hadoop/tpcds-data -TERMINATE N -PARALLEL 4 -CHILD 1 -FORCE Y -TABLE store_sales &
./dsdgen -SCALE 10 -DIR /home/hadoop/tpcds-data -TERMINATE N -PARALLEL 4 -CHILD 2 -FORCE Y -TABLE store_sales &
./dsdgen -SCALE 10 -DIR /home/hadoop/tpcds-data -TERMINATE N -PARALLEL 4 -CHILD 3 -FORCE Y -TABLE store_sales &
./dsdgen -SCALE 10 -DIR /home/hadoop/tpcds-data -TERMINATE N -PARALLEL 4 -CHILD 4 -FORCE Y -TABLE store_sales &
wait

echo "Generacion completada"
```

> Usar siempre la ruta absoluta `/home/hadoop/tpcds-data` en `-DIR`, no `~/tpcds-data`. Las tablas globales como `customer`, `store` y `date_dim` no se particionan — generarlas en paralelo causa colisiones de escritura. Solo `store_sales` admite generación paralela con `-CHILD`.

`-SCALE 10` genera aproximadamente 10 GB. `-PARALLEL 4` define cuántas partes hay en total. `-CHILD N` especifica qué parte genera cada proceso — deben lanzarse como procesos separados con `&`.

Los archivos de `store_sales` siguen el patrón `store_sales_N_4.dat`, por ejemplo `store_sales_1_4.dat`, `store_sales_2_4.dat`, etc.

El tiempo de generación en un master EMR `m5.xlarge` es aproximadamente 10-20 minutos.

### 3. Verificar los archivos generados

```bash
ls -lh /home/hadoop/tpcds-data/ | grep -E "customer|item|store|date_dim|store_sales"
```

Las 5 tablas obligatorias deben estar presentes:

```
customer.dat         ~64 MB
date_dim.dat         ~10 MB
item.dat             ~28 MB
store.dat            ~27 KB
store_sales_1_4.dat  ~942 MB
store_sales_2_4.dat  ~946 MB
store_sales_3_4.dat  ~950 MB
store_sales_4_4.dat  ~950 MB
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
