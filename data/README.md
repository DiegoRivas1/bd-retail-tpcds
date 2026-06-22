# Datos TPC-DS

Instrucciones para generar el dataset TPC-DS de 10 GB y cargarlo en HDFS
para su uso con Hive y Spark.

---

## Opcion A: Generar los datos con tpcds-kit (recomendado)

### 0. Configurar el volumen EBS del master

El volumen raíz del master EMR tiene 15 GB por defecto, insuficiente para generar
10 GB de datos TPC-DS. Al crear el clúster, configurar el EBS del master en **50 GB**
desde la consola AWS en la sección de configuración avanzada de instancias.

Si el clúster ya fue creado con 15 GB, ampliar desde EC2:

1. EC2 → Instances → seleccionar la instancia Primary
2. Storage → click en el Volume ID
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

El flag `-fcommon` es necesario para compilar con gcc 10+ que por defecto usa
`-fno-common` y genera errores de definiciones múltiples en el código fuente de tpcds-kit.

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

> Usar siempre la ruta absoluta `/home/hadoop/tpcds-data` en `-DIR`, no `~/tpcds-data`.
> Las tablas globales como `customer`, `store` y `date_dim` no se particionan y 
> generarlas en paralelo causa colisiones de escritura y el error `Failed to open output file`.
> Solo `store_sales` admite generación paralela con `-CHILD`.
> `-PARALLEL 4` define cuántas partes hay en total. `-CHILD N` especifica qué parte
> genera cada proceso y deben lanzarse como procesos separados con `&`.

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

---

## Opcion B: Usar un dataset ya generado desde S3

Si existe un dataset TPC-DS disponible en S3 del lab de Vocareum:

```bash
aws s3 cp s3://<bucket>/tpcds/ /home/hadoop/tpcds-data/ --recursive
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
hadoop fs -put /home/hadoop/tpcds-data/customer.dat      /user/hadoop/tpcds/customer/
hadoop fs -put /home/hadoop/tpcds-data/item.dat          /user/hadoop/tpcds/item/
hadoop fs -put /home/hadoop/tpcds-data/store.dat         /user/hadoop/tpcds/store/
hadoop fs -put /home/hadoop/tpcds-data/date_dim.dat      /user/hadoop/tpcds/date_dim/
hadoop fs -put /home/hadoop/tpcds-data/store_sales_*.dat /user/hadoop/tpcds/store_sales/
```

### 3. Verificar en HDFS

```bash
hadoop fs -ls /user/hadoop/tpcds/
hadoop fs -du -h /user/hadoop/tpcds/
```

Salida esperada:

```
63.3 M   /user/hadoop/tpcds/customer
9.8 M    /user/hadoop/tpcds/date_dim
27.4 M   /user/hadoop/tpcds/item
26.4 K   /user/hadoop/tpcds/store
3.7 G    /user/hadoop/tpcds/store_sales
```

---

## Crear las tablas en Hive

```bash
cd ~/bd-retail-tpcds
hive -f hive/crear_tablas.hql
```

Verificar:

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
El valor obtenido en este proyecto fue **28,800,991** filas.

---

## Notas

- Los archivos `.dat` no se suben al repositorio por su tamaño.
- El directorio `/home/hadoop/tpcds-data/` en el master es temporal, se pierde al apagar el cluster.
- Los datos en HDFS persisten mientras el cluster esté activo.
- Si se reinicia el cluster, repetir los pasos de carga desde la Opcion A o B.
- Documentacion oficial TPC-DS: https://www.tpc.org/tpcds/
- Repositorio tpcds-kit: https://github.com/gregrahn/tpcds-kit