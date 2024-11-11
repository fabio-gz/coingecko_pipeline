Descripcion
========
Este proyecto tiene como objetivo extraer datos de la API de CoinGecko y almacenarlos en un un bucket en area de staging y luego en bigquery para análisis.
Se utilizo Airflow como orquestador de las tareas y dbt como herramienta de transformación de datos.

Se utilizo Google Cloud Platform como solucion para el almacenamiento de los datos y Bigquery como datawarehouse.
En el primer paso se extrae los datos de la API de CoinGecko y se almacenan en un bucket de Google Cloud Storage en formato parquet.
Luego se transforman los datos utilizando dbt y se almacenan en Bigquery usando dbt.

En el caso de que los datos aumentaran al tener un area de staging donde se almacenan los datos crudos no tendra problema si estos aumentan.
Se esta usando Dataset de Airflow para ejecutar el dag de transformación cuando los datos estan listos, sin embargo es posible especificar ventanas de tiempo.
Al usar bigquery como datawarehouse no hay problema en tener 100 usuario finales accediendo a las tablas, debido a sus caracteristicas de escalabilidad y performance.

Si se requiriera hacer analitica en tiempo real se podria usar un servicio de mensajes como pub/sub para leer eventos que el servicio este escuchando constantemente.

Contenido
================


- dags: Carpeta que contiene los Dags para ingesta de datos y la transformación de los mismos.
- include: Carpeta que contiene archivos de ayuda y utilidades.
- requirements.txt: liberias necesarias.


Uso
===========================

Para este proyecto se utilizo Astronomer localmente, para levantar el ambiente se debe ejecutar el siguiente comando:

```bash
astro dev start
```


Para eliminar el ambiente se debe ejecutar el siguiente comando:

```bash
astro dev stop
```


