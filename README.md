<h1 align="center"> Big Data con Spark MLlib y Databricks </h1>

## Índice

- [Resumen del proyecto](#Resumen-del-proyecto)
- [¿Qué es Databricks?](#qué-es-databricks)
- [¿Qué es Kaggle?](#qué-es-kaggle)
- [Arquitectura empleada](#Arquitectura-empleada)
- [Sobre el conjunto de datos](#Sobre-el-conjunto-de-datos)
- [Sobre la métrica de evaluación](#Sobre-la-métrica-de-evaluación)
- [Sobre el algoritmo Gradient Boosting Trees](#Sobre-el-algoritmo-Gradient-Boosting-Trees)

## Resumen del proyecto
El siguiente proyecto tiene como objetivo predecir la probabilidad de que un cliente no pague el saldo de su tarjeta de crédito en el futuro, en función de su perfil de cliente mensual, para lo cual se deberán procesar archivos con millones de registros de transacciones bancarias anonimizadas de American Express, obtenidos desde Kaggle, y especialmente preparados para este fin (https://acortar.link/LOfyfq). La capacidad de cómputo para ejeuctar operaciones sobre estas cantidades de datos (y para cantidades mucho mayores), muchas veces sobrepasa la capacidad de una sóla máquina, por lo cual se utilizará la plataforma Databricks, que facilita el uso de Apache Spark para estos fines, y tiene la capacidad para realizar cómputos de forma distribuida, es decir, utilizar varias máquinas en paralelo para aumentar la capacidad de procesamiento. Para cumplir el objetivo, se usará un algortimo de Machine Learning llamado Gradient Boosting Trees (GBTClassifier) con el fin de predecir el incumplimiento crediticio. En el proceso de obtención de datos, se utilizará la API de Kaggle y un bucket de Amazon S3.

## ¿Qué es Databricks?
Databricks es una plataforma en la nube que optimiza el uso de Apache Spark para la ingeniería de datos. Facilita la colaboración entre ingenieros de datos y científicos de datos al proporcionar un entorno integrado para el procesamiento y análisis de grandes volúmenes de datos, permiendo diseñar, implementar y gestionar flujos de trabajo de datos de manera eficiente, aprovechando las capacidades de Apache Spark para realizar tareas de ETL, procesamiento en tiempo real y machine learning. Documentación oficial: https://www.databricks.com/databricks-documentation.

* Es importante notar que, para efectos de aplicaciones creadas con Apache Spark, en Databricks no es necesario inicializar el "SparkContext" ni crear "SparkSessions", pues el propio entorno ya lo hace.
  
* Como paso previo, se debe crear un cluster, el cual para la versión Community Edition, que es gratuita, posee 15 GB de memoria y 2 cores. Adjunto una imagen donde se muestra en qué lugar debe crear el custer, en sección "compute":
<br/><br/>

<img width="555" alt="create_test_cluster" src="https://github.com/user-attachments/assets/58557b47-3c53-47cb-b46f-788999920702">

* Por un lado, cuando se accede al sistema de archivos local en Databricks (por ejemplo: 'file:/tmp/wiki_data/') del nodo en el que se está ejecutando el código, es similar a cómo se manjean archivos en un entorno de escritorio o servidor normal. Los archivos almacenados en el sistema de archivos local son temporales y pueden no estar disponibles después de que finaliza la sesión o el clúster se reinicia.

* Por otro lado, Databricks cuenta con un sistema de archivos distribuido llamado 'DBFS' (Databricks File System) (por ejemplo: 'dbfs:/tmp/wiki_data/'), el cual está disponible en todos los nodos del clúster de Databricks. Esto significa que los archivos en DBFS pueden ser accedidos desde cualquier nodo, lo cual es crucial para la ejecución de trabajos distribuidos. Los archivos almacenados en DBFS son persistentes y están disponibles incluso después de que finaliza la sesión o se reinicia el clúster. Esto hace que DBFS sea ideal para almacenar datos que necesitas reutilizar o compartir entre sesiones. DBFS está optimizado para trabajar con Apache Spark, lo que facilita la lectura y escritura de grandes conjuntos de datos distribuidos.

## ¿Qué es Kaggle?
Kaggle es una plataforma en línea para la competencia en ciencia de datos, donde los usuarios pueden compartir datos, códigos, y modelos, así como participar en competencias para resolver problemas reales. Para este proyecto, es necesario que se cree una cuenta gratuita en Kaggle ( https://www.kaggle.com/ ) y que utilice su API púbica, para lo cual debe solicitar en su página que se cree su API Token ( https://christianjmills.com/posts/kaggle-obtain-api-key-tutorial/ ), con lo cual obtendrá un archivo json con su usuario y contraseña de la API de Kaggle.

## Arquitectura empleada
El esquema general del modo en que se relacionan las partes del sistema es el siguiente:
<br/><br/>

![Databricks](https://github.com/user-attachments/assets/8a912e9f-6cdf-43a3-8edb-fe8525dc23a7)

## Sobre el conjunto de datos
El conjunto de datos contiene características de perfil agregadas para cada cliente (campo "customer_ID") en cada fecha de estado de cuenta. La cantidad de registros supera los 11 millones de operaciones crediticias procesadas en el conjunto de prueba, sobre los 5,5 millones en el conjunto de entrenamiento, y sobre los 450.000 clientes etiquetados. Las características están anonimizadas y normalizadas y se dividen en las siguientes categorías generales:

- D_* = Variables de morosidad
- S_* = Variables de gasto
- P_* = Variables de pago
- B_* = Variables de equilibrio
- R_* = Variables de riesgo

Con las siguientes características siendo categóricas: ['B_30', 'B_38', 'D_114', 'D_116', 'D_117', 'D_120', 'D_126', 'D_63', 'D_64', 'D_66', 'D_68'] El objetivo es predecir, para cada "customer_ID", la probabilidad de un futuro impago (campo "target" = 1).

Los datos de entrenamiento y de prueba se obtendrán desde la API de Kaggle, desde los archivos "train.parquet" y "test.parquet", respectivamente, mientras que las etiquetas (campo donde se clasifican como clientes con default o no, para realizar aprendizaje supervisado) de los id de clientes han sido catalogadas a parte, y han sido almacenadas por el equipo de encargado del etiquetado en Amazon S3, en archivo "train_labels.csv", por lo cual se deberán obtener con Databricks las etiquetas desde un bucket de AWS.

## Sobre la métrica de evaluación
La métrica de evaluación, 𝑀, para este proyecto es la media de dos medidas de ordenamiento por rango: Coeficiente de Gini Normalizado, 𝐺, y la tasa de incumplimiento se situó en el 4%,𝐷.

𝑀= 0,5 ⋅ ( 𝐺 + 𝐷 )

La tasa predeterminada capturada en 4% es el porcentaje de etiquetas positivas (predeterminadas) capturadas dentro del 4% de las predicciones con mayor clasificación y representa una estadística de Sensibilidad/Recuperación. Para ambas submétricas 𝐺 y 𝐷, a las etiquetas negativas se les asigna un peso de 20 para ajustar el muestreo descendente. Esta métrica tiene un valor máximo de 1.0. Para cada id de cliente del del conjunto de prueba (campo 'customer_ID'), se va a predecir una probabilidad para la variable objetivo, en el formato (customer_ID, prediction).

## Sobre el algoritmo Gradient Boosting Trees
Gradient Tree Boosting (GBT) es un algoritmo de aprendizaje supervisado utilizado principalmente para tareas de clasificación y regresión. El concepto central detrás de GTB es construir un modelo robusto mediante la combinación de varios árboles de decisión simples (o débiles), de manera secuencial, donde cada árbol nuevo intenta corregir los errores cometidos por los árboles anteriores. Aunque es computacionalmente intensivo, sus capacidades para manejar datos complejos y producir resultados precisos lo hacen muy popular en el campo del machine learning.


