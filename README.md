# Proyecto de Big Data con Spark MLlib y Databricks.

En el siguiente proyecto se usará un algortimo de Machine Learning para predecir el incumplimiento crediticio, basandose en un dataset de American Express especialmente preparado para este fin ( https://www.kaggle.com/competitions/amex-default-prediction/data ).

El objetivo es predecir la probabilidad de que un cliente no pague el saldo de su tarjeta de crédito en el futuro en función de su perfil de cliente mensual. La variable binaria objetivo se calcula observando el desempeño de 18 meses después del último estado de cuenta de la tarjeta de crédito y, si el cliente no paga el monto adeudado en los 120 días posteriores a la fecha del último estado de cuenta, se considera un evento de incumplimiento.

## Sobre el conjunto de datos a utilizar
El conjunto de datos contiene características de perfil agregadas para cada cliente (campo "customer_ID") en cada fecha de estado de cuenta. La cntidad de registros supera las 5,5 millones de operaciones crediticias procesadas en el conjunto de entrenamiento, x en el conjunto de prueba y sobre los 450.000 los clientes etiquetados. Las características están anonimizadas y normalizadas y se dividen en las siguientes categorías generales:

- D_* = Variables de morosidad
- S_* = Variables de gasto
- P_* = Variables de pago
- B_* = Variables de equilibrio
- R_* = Variables de riesgo

Con las siguientes características siendo categóricas: ['B_30', 'B_38', 'D_114', 'D_116', 'D_117', 'D_120', 'D_126', 'D_63', 'D_64', 'D_66', 'D_68'] El objetivo es predecir, para cada "customer_ID", la probabilidad de un futuro impago (campo "target" = 1).

Los datos de entrenamiento y de prueba se obtendrán desde la API de Kaggle, mientras que las etiquetas de los id de clientes han sido catalogadas a parte, y han sido almcadenadas por el equipo de encarado del etiquetado en Amazon S3, por lo cual se deberán obtener con Databricks las etiquetas desde un bucket de AWS.

La métrica de evaluación, 𝑀, para esta competencia es la media de dos medidas de ordenamiento por rango: Coeficiente de Gini Normalizado, 𝐺, y la tasa de incumplimiento se situó en el 4%,𝐷.

𝑀= 0,5 ⋅ ( 𝐺 + 𝐷 )

La tasa predeterminada capturada en 4% es el porcentaje de etiquetas positivas (predeterminadas) capturadas dentro del 4% de las predicciones con mayor clasificación y representa una estadística de Sensibilidad/Recuperación. Para ambas submétricas 𝐺 y 𝐷, a las etiquetas negativas se les asigna un peso de 20 para ajustar el muestreo descendente. Esta métrica tiene un valor máximo de 1.0.

Para cada id de cliente del del conjunto de prueba (campo 'customer_ID'), se va a predecir una probabilidad para la variable objetivo, en el formato (customer_ID, prediction).

## ¿Qué es Databricks?
Databricks es una plataforma en la nube que optimiza el uso de Apache Spark para la ingeniería de datos. Facilita la colaboración entre ingenieros de datos y científicos de datos al proporcionar un entorno integrado para el procesamiento y análisis de grandes volúmenes de datos, permiendo diseñar, implementar y gestionar flujos de trabajo de datos de manera eficiente, aprovechando las capacidades de Apache Spark para realizar tareas de ETL, procesamiento en tiempo real y machine learning. Documentación oficial: https://www.databricks.com/databricks-documentation

## ¿Qué es Kaggle?
Kaggle es una plataforma en línea para la competencia en ciencia de datos y machine learning, donde los usuarios pueden compartir datos, códigos, y modelos, así como participar en competencias para resolver problemas reales. Para este proyecto, es necesario que se cree una cuenta gratuita en Kaggle ( https://www.kaggle.com/ ) y que utilice su API púbica, para lo cual debe solicitar en su página que se cree su API Token ( https://christianjmills.com/posts/kaggle-obtain-api-key-tutorial/ ), con lo cual obtendrá un archivo json con su usuario y contraseña de la API de Kaggle.


