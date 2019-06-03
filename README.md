# Clasificación De Polaridad De Tweets En Español Usando BERT

## Resumen

El workshop TASS 2019 propone diferentes desafíos de análisis
semántico del Español. Este trabajo presenta un enfoque posible para
la tarea de clasificación de polaridad de tweets utilizando el modelo
de representación de lenguaje BERT [1]. En particular, el modelo pre
entrenado multilingüe ofrecido por los desarrolladores de BERT fue pre
entrenado con un corpus de un millón de tweets en español. Luego el
modelo fue ajustado con el corpus InterTASS 2019 [2] para la tarea de
clasificación de polaridad de tweets.

## Introducción

Desde 2012, el Taller de Análisis de Sentimiento en SEPLN (TASS) se ha
llevado a cabo en el marco de la Conferencia Internacional de la
Sociedad Española de Procesamiento del Lenguaje Natural (SEPLN). El
español es el segundo idioma utilizado en Facebook y Twitter, lo cual
demanda el desarrollo de métodos y recursos para el análisis de
sentimientos en español. En particular uno de los desafíos más
importantes de este taller es la clasificación de polaridad de tweets
[3] basada en tres conjuntos de datos de tweets tomados de tres países
de habla hispánica: España (ES), Costa Rica (CR) y Perú (PE). En este
trabajo presentamos un enfoque posible para la tarea de clasificación
de polaridad de tweets utilizando el modelo de representación de
lenguaje BERT [1].

El modelo de representación de lenguaje BERT está diseñado para pre
entrenar representaciones bidireccionales profundas utilizando texto
sin etiquetar, condicionando conjuntamente en el contexto izquierdo y
derecho en todas las capas. Luego, el modelo BERT pre-entrenado puede
ajustarse con solo una capa de salida adicional para crear modelos de
vanguardia para una amplia gama de tareas [1]. En la práctica esto
significa que entrenamos un modelo de comprensión del lenguaje de
propósito general en un gran corpus de manera no supervisada y luego
usamos ese modelo para las tareas específicas que nos interesan. La
ventaja de esto es que podemos utilizar un corpus como Wikipedia [3]
para entrenar un buen modelo de lenguaje.

## Técnicas y Recursos
### Conjuntos de datos
Utilizamos dos conjuntos de datos. Utilizamos 500000 de tweets en
español tomados del corpus UBA [4] para el entrenamiento no supervisado
del modelo y los tweets del conjunto de datos Inter-TASS 2019 para el
ajuste del modelo a la tarea de clasificación de polaridad de
tweets. Aplicamos el mismo preprocesamiento a ambos conjuntos de
datos.

### Preprocesamiento
El preprocesamiento es esencial cuando se trabaja con datos con mucho
ruido. Cualquier trabajo sobre tweets debe realizar un buen
preprocesamiento para funcionar adecuadamente debido al lenguaje
informal de los mismos. Un tweet puede poseer errores de ortografía,
emojis, urls, menciones y onomatopeyas.

En este trabajo simplemente remplazamos menciones por `@USER`, URLs
por `URL`, emails por `user@mail.com` y eliminamos los emojis
presentes.

### Modelo Pre Entrenado
Los autores de [1] ofrecen modelos pre entrenados basados en las
descargas de Wikipedia. En particular, existe un modelo multilingüe
entrenado utilizando las descargas de Wikipedias en varios
lenguajes. En este trabajo utilizamos dicho modelo. El modelo puede
ser encontrado en [bert](https://github.com/google-research/bert) bajo
el nombre: `BERT-Base, Multilingual Cased`. El modelo fue pre
entrenado por los autores de [1] con la descarga de las Wikipedias de
104 languages.

### Pre entrenamiento
Una vez que preprocesamos los tweets del corpus UBA utilizamos estos
tweets en el pre entrenamiento no supervisado del modelo pre entrenado
para obtener un modelo de representación del lenguaje específico para
Twitter en español.

Para el pre entrenamiento contabamos con


### Ajuste fino del modelo
Una vez obtenido el modelo de representación del lenguaje es necesario
ajustar el modelo para la tarea específica de clasificación de
polaridad de tweets en español. Para ello, hicimos un ajuste fino del
modelo utilizando el conjunto de datos Inter TASS 2019 para

## Resultados


## Conclusiones

## Referencias

[1] BERT
[2] Inter-TASS 2019
[3] Wikipedia
[4] UBA corpus
