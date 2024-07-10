# Proyecto de Big Data con Spark MLlib y Databricks.

En el siguiente proyecto se usará un algortimo de Machine Learning para predecir el incumplimiento crediticio, basandose en un dataset de American Express especialmente preparado para este fin ( https://www.kaggle.com/competitions/amex-default-prediction/data ). El objetivo es predecir la probabilidad de que un cliente no pague el saldo de su tarjeta de crédito en el futuro en función de su perfil de cliente mensual. La variable binaria objetivo se calcula observando el desempeño de 18 meses después del último estado de cuenta de la tarjeta de crédito y, si el cliente no paga el monto adeudado en los 120 días posteriores a la fecha del último estado de cuenta, se considera un evento de incumplimiento.

La métrica de evaluación, 𝑀, para esta competencia es la media de dos medidas de ordenamiento por rango: Coeficiente de Gini Normalizado, 𝐺, y la tasa de incumplimiento se situó en el 4%,𝐷.

𝑀= 0,5 ⋅ ( 𝐺 + 𝐷 )

La tasa predeterminada capturada en 4% es el porcentaje de etiquetas positivas (predeterminadas) capturadas dentro del 4% de las predicciones con mayor clasificación y representa una estadística de Sensibilidad/Recuperación. Para ambas submétricas 𝐺 y 𝐷, a las etiquetas negativas se les asigna un peso de 20 para ajustar el muestreo descendente. Esta métrica tiene un valor máximo de 1.0.

Para cada id de cliente del del conjunto de prueba (campo 'customer_ID'), se va a predecir una probabilidad para la variable objetivo, en el formato (customer_ID, prediction).

El conjunto de datos contiene características de perfil agregadas para cada cliente en cada fecha de estado de cuenta. Las características están anonimizadas y normalizadas y se dividen en las siguientes categorías generales:

D_* = Variables de morosidad
S_* = Variables de gasto
P_* = Variables de pago
B_* = Variables de equilibrio
R_* = Variables de riesgo
con las siguientes características siendo categóricas:

['B_30', 'B_38', 'D_114', 'D_116', 'D_117', 'D_120', 'D_126', 'D_63', 'D_64', 'D_66', 'D_68']

El objetivo es predecir, para cada customer_ID, la probabilidad de un futuro impago ( target = 1).

Los datos de entrenamiento y de prueba se obtendrán desde la API de Kaggle, mientras que las etiquetas de los id de clientes han sido catalogadas a parte, y han sido almcadenadas por el equipo en Amazon S3, por lo cual se deberán obtener con Databricks las etiquetas desde un bucket de AWS.

