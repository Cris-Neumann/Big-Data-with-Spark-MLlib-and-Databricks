<h1 align="center"> Big Data con Spark MLlib y Databricks </h1>

## Índice

- [Resumen del proyecto](#Resumen-del-proyecto)
- [¿Qué es Databricks?](#qué-es-databricks)
- [¿Qué es Kaggle?](#qué-es-kaggle)
- [Arquitectura empleada](#Arquitectura-empleada)
- [Sobre el conjunto de datos](#Sobre-el-conjunto-de-datos)
- [Sobre la métrica de evaluación](#Sobre-la-métrica-de-evaluación)
- [Proceso de creación del modelo de ML](#Proceso-de-Creación-del-Modelo-de-ML)

## Resumen del proyecto
El siguiente proyecto tiene como objetivo predecir la probabilidad de que un cliente no pague el saldo de su tarjeta de crédito en el futuro, en función de su perfil de cliente mensual. Para ello, se procesarán archivos con millones de registros de transacciones bancarias anonimizadas de American Express, obtenidos desde Kaggle (ver: https://acortar.link/LOfyfq).

La capacidad de cómputo necesaria para ejecutar varias operaciones sobre estas cantidades de datos (y sobre todo para cantidades mayores) suele sobrepasar la capacidad de una sola máquina. Por esta razón, se utilizará la plataforma Databricks, que facilita el uso de Apache Spark para estos fines y tiene la capacidad para realizar cómputos de forma distribuida, es decir, utilizar varias máquinas en paralelo para aumentar la capacidad de procesamiento. Dado que se utilizará la versión Community Edition, que es gratuita, sólo podremos acceder a un solo nodo de cómputo, por lo que para utilizar computación distribuida, se debe acceder a versiones pagadas.

Para cumplir el objetivo de predicción, se usará un algoritmo de Machine Learning llamado Gradient Boosting Trees (GBTClassifier) con el fin de predecir el incumplimiento crediticio. En el proceso de obtención de datos, se utilizará la API de Kaggle y un bucket de Amazon S3. Los resultados (inferencia, datasets depurados y modelo de ML utilizado) serán almacenados en un bucket de S3. Todos los códigos serán almacenados en archivos con extensión .ipynb (Jupyter Notebook), pues Databricks permite exportar y cargar sus notebooks en este formato y en .dbc, pero dado que no todos los usuarios podrán leer los archivos .dbc, el formato .ipynb es una mejor opción para que cualquier persona pueda leer los notebooks en sus IDE (entorno de desarrollo integrado) favoritos, como Visual Studio Code por ejemplo.

## ¿Qué es Databricks?
Databricks es una plataforma en la nube que optimiza el uso de Apache Spark para la ingeniería de datos. Facilita la colaboración entre ingenieros de datos y científicos de datos al proporcionar un entorno integrado para el procesamiento y análisis de grandes volúmenes de datos. Permite diseñar, implementar y gestionar flujos de trabajo de datos de manera eficiente, aprovechando las capacidades de Apache Spark para realizar tareas de ETL, procesamiento en tiempo real y Machine Learning.. Documentación oficial: https://www.databricks.com/databricks-documentation.

* Es importante notar que, para aplicaciones creadas con Apache Spark, en Databricks no es necesario inicializar el "SparkContext" ni crear "SparkSessions", ya que el entorno lo hace automáticamente.
  
* Como paso previo, se debe crear un clúster. En la versión Community Edition, el clúster tiene 15 GB de memoria y 2 núcleos. Adjunto una imagen donde se muestra cómo crear el clúster en la sección "Compute":

<p align="center">
  <img width="555" alt="create_test_cluster" src="https://github.com/user-attachments/assets/58557b47-3c53-47cb-b46f-788999920702">
</p>

* Por un lado, cuando se accede al sistema de archivos local en Databricks (por ejemplo, 'file:/tmp/wiki_data/') desde el nodo en el que se está ejecutando el código, es similar a cómo se manejan archivos en un entorno de escritorio o servidor normal. Los archivos almacenados en el sistema de archivos local son temporales y pueden no estar disponibles después de que finaliza la sesión o se reinicia el clúster.

* Por otro lado, Databricks cuenta con un sistema de archivos distribuido llamado 'DBFS' (Databricks File System) (por ejemplo, 'dbfs:/tmp/wiki_data/'), el cual está disponible en todos los nodos del clúster de Databricks. Esto significa que los archivos en DBFS pueden ser accedidos desde cualquier nodo, lo cual es crucial para la ejecución de trabajos distribuidos. Los archivos almacenados en DBFS son persistentes y permanecen disponibles incluso después de que finaliza la sesión o se reinicia el clúster. Esto hace que DBFS sea ideal para almacenar datos que necesitas reutilizar o compartir entre sesiones. Además, DBFS está optimizado para trabajar con Apache Spark, lo que facilita la lectura y escritura de grandes conjuntos de datos distribuidos.

## ¿Qué es Kaggle?
Kaggle es una plataforma en línea para competencias en ciencia de datos, donde los usuarios pueden compartir datos, códigos y modelos, así como participar en competencias para resolver problemas reales. Para este proyecto, es necesario crear una cuenta gratuita en Kaggle ( https://www.kaggle.com/ ) y utilizar su API pública. Para ello, debes solicitar la creación de tu API Token en su página web (ver totorial al respecto: https://christianjmills.com/posts/kaggle-obtain-api-key-tutorial/ ). Esto te proporcionará un archivo JSON que contiene tu usuario y la clave de la API de Kaggle.

## Arquitectura empleada
El esquema general del modo en que se relacionan las partes del sistema es el siguiente:
<br/><br/>

![Databricks](https://github.com/user-attachments/assets/0e14303f-4b51-4895-a25e-99814618568d)


## Sobre el conjunto de datos
El conjunto de datos contiene características de perfil agregadas para cada cliente (campo "customer_ID") en cada fecha de estado de cuenta. El número total de registros supera los 11 millones de operaciones crediticias en el conjunto a predecir, 5.5 millones en el conjunto de entrenamiento, y alrededor de 450.000 clientes etiquetados. Las características están anonimizadas, normalizadas y se dividen en las siguientes categorías generales:

- D_* = Variables de morosidad
- S_* = Variables de gasto
- P_* = Variables de pago
- B_* = Variables de equilibrio
- R_* = Variables de riesgo

Con las siguientes características siendo categóricas: ['B_30', 'B_38', 'D_114', 'D_116', 'D_117', 'D_120', 'D_126', 'D_63', 'D_64', 'D_66', 'D_68'] El objetivo es predecir, para cada "customer_ID", la probabilidad de un futuro impago (campo "target" = 1).

## Sobre la métrica de evaluación
La métrica de evaluación, 𝑀, para este proyecto es la media de dos medidas de ordenamiento por rango: Coeficiente de Gini Normalizado, 𝐺, y la tasa de incumplimiento, 𝐷.

𝑀 = 0,5 ⋅ ( 𝐺 + 𝐷 )

La tasa predeterminada capturada en 4% es el porcentaje de etiquetas positivas (predeterminadas) capturadas dentro del 4% de las predicciones con mayor clasificación y representa una estadística de Sensibilidad/Recuperación. Para ambas submétricas 𝐺 y 𝐷, a las etiquetas negativas se les asigna un peso de 20 para ajustar el muestreo descendente. Esta métrica tiene un valor máximo de 1.0. Para cada id de cliente del conjunto de prueba (campo 'customer_ID'), se va a predecir la probabilidad para la variable objetivo, en el formato (customer_ID, prediction).

## Proceso de creación del modelo de ML
- Ingesta de datos: Los datos de entrenamiento y de los clientes a evaluar se obtendrán desde la API de Kaggle, ambos en formato parquet. Mientras que las etiquetas (campo donde se clasifican como clientes con default o no, para realizar aprendizaje supervisado) de los id de clientes han sido almacenadas en Amazon S3, en formato CSV, desde donde Databricks deberá obtener dichos registros. En archivos "extract_data" y "extract_labels" se muestra como obtener los datos y las etiquetas, respectivamente. Una vez extraídos, serán almacenados de forma transitoria en DBFS.

- Análisis Exploratorio de datos (EDA) e Ingeniería de Características: Se realiza la exploración de los datos, con el fin de conocer su distribución, valores faltantes, estructura, volumen y forma de registros y características, entre otros. Luego, con la información acumulada, se realiza la ingeniería de características, donde se realizan operaciones entre columnas y se seleccionan las que serán parte del dataset final. Una vez determinadas las característics finales, serán almacenadas de forma transitoria en DBFS. En archivo "feature_engineering" se pueden apreciar las operaciones en este paso del proceso. Se adjuntan algunas imagenes de operaciones realizadas para conocer cómo evolucionaron los datos en el tiempo, y cómo se distribuyen las etiquetas en achivo "train_labels.csv"

![eventos](https://github.com/user-attachments/assets/54bf3dd7-3c8c-426f-b516-64fd2f61ef12)

<p align="center">
  <img width="555" alt="create_test_cluster" src="https://github.com/user-attachments/assets/7a6e608e-49e4-40e9-b75d-244e140f1177" alt="distribuciones">
</p>

- Entrenamiento del modelo de ML e Inferencia: Se vectorizan las caracteristicas a utilizar, se selecciona el clasificador Gradient Boosting Trees (GBTClassifier) y se realiza la búsqueda de hiperparámetros con la técnica de Validación Cruzada "K-Fold Cross Validation". Posteriormente se evalúa su rendimiento con varias métricas usuales como el Recall, F1 Score y Precision, asi como tambien con la métrica particular definida por quien solicita la predicción, llamada "M score". Finalmente se realiza la inferencia (predicción) para los clientes solicitados, sobre si caerán en dafault o no, guardando esta predicción como archivo CSV en DBFS y el modelo de ML es almacenado tambén en DBFS. Estas operaciones están en archivo "model_selection".
  
- Pequeña disgresión: Gradient Boosting Trees (GBT) es un algoritmo de aprendizaje supervisado utilizado principalmente para tareas de clasificación y regresión. El concepto central detrás de GBT es construir un modelo robusto mediante la combinación de varios árboles de decisión simples (o débiles) de manera secuencial, donde cada árbol nuevo intenta corregir los errores cometidos por los árboles anteriores. Aunque es computacionalmente intensivo, sus capacidades para manejar datos complejos, su implementación nativa en Spark MLlib y su capacidad para producir resultados precisos lo hacen muy popular en el campo del Machine Learning.
  
- Persistencia de datos y modelo: Finalmente, el modelo generado, las predicciones realizadas, y los datasets depurados en el proceso de ingeniería de características, son almacenados para que persistan en un bucket de Amazon S3, lo cual se puede apreciar en archivo "save_data". De esta manera, se libera el espacio y memoria de Databricks, y estos resultados pueden ser usados en el futuro por otros usuarios con acceso al bucket.


