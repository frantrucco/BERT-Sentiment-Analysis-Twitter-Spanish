# Clasificación De Polaridad De Tweets En Español Usando BERT

## Resumen

El workshop TASS 2019 propone diferentes desafíos de análisis
semántico del Español. Este trabajo presenta un enfoque posible para
la tarea de clasificación de polaridad de tweets utilizando el modelo
de representación de lenguaje BERT. En particular, el modelo pre
entrenado multilingüe ofrecido por los desarrolladores de BERT fue pre
entrenado con un corpus de un millón de tweets en español. Luego el
modelo fue ajustado con el corpus InterTASS 2019 para la tarea de
clasificación de polaridad de tweets.

## Introducción

Desde 2012, el Taller de Análisis de Sentimiento en SEPLN (TASS) se ha
llevado a cabo en el marco de la Conferencia Internacional de la
Sociedad Española de Procesamiento del Lenguaje Natural (SEPLN). El
español es el segundo idioma utilizado en Facebook y Twitter, lo cual
demanda el desarrollo de métodos y recursos para el análisis de
sentimientos en español. En particular uno de los desafíos más
importantes de este taller es la clasificación de polaridad de tweets
basada en tres conjuntos de datos de tweets tomados de tres países
de habla hispánica: España (ES), Costa Rica (CR) y Perú (PE). En este
trabajo presentamos un enfoque posible para la tarea de clasificación
de polaridad de tweets utilizando el modelo de representación de
lenguaje BERT.

El modelo de representación de lenguaje BERT está diseñado para pre
entrenar representaciones bidireccionales profundas utilizando texto
sin etiquetar, condicionando conjuntamente en el contexto izquierdo y
derecho en todas las capas. Luego, el modelo BERT pre-entrenado puede
ajustarse con solo una capa de salida adicional para crear modelos de
vanguardia para una amplia gama de tareas. En la práctica esto
significa que entrenamos un modelo de comprensión del lenguaje de
propósito general en un gran corpus de manera no supervisada y luego
usamos ese modelo para las tareas específicas que nos interesan. La
ventaja de esto es que podemos utilizar un corpus como Wikipedia
para entrenar un buen modelo de lenguaje.

## Técnicas y Recursos
### Conjuntos de datos
Utilizamos dos conjuntos de datos. Contamos con 65000000 de tweets en
español para el entrenamiento no supervisado del modelo y los tweets
del conjunto de datos Inter-TASS 2019 para el ajuste del modelo a la
tarea de clasificación de polaridad de tweets. Aplicamos el mismo
preprocesamiento a ambos conjuntos de datos.

### Preprocesamiento
El preprocesamiento es esencial cuando se trabaja con datos con mucho
ruido. Cualquier trabajo sobre tweets debe realizar un buen
preprocesamiento para funcionar adecuadamente debido al lenguaje
informal de los mismos. Un tweet puede poseer errores de ortografía,
emojis, urls, menciones y onomatopeyas.

Las siguientes transformaciones fueron aplicadas a los tweets:

- Reemplazamos todas las palabras por su versión en minúsculas.
- Reemplazamos menciones por `@USER`.
- Reemplazamos URLs por `URL`.
- Reemplazamos emails por `user@mail.com`
- Eliminamos emojis, números y puntuación
- Remplazamos cuatro o más letras repetidas por tres letras.
- Remplazamos dos o más espacios repetidos por un único espacio.

### Modelo Pre Entrenado
Los autores de BERT ofrecen modelos pre entrenados basados en las
descargas de Wikipedia. En particular, existe un modelo multilingüe
entrenado utilizando las descargas de Wikipedias en varios
lenguajes. En este trabajo utilizamos dicho modelo. El modelo puede
ser encontrado en [bert](https://github.com/google-research/bert) bajo
el nombre: `BERT-Base, Multilingual Cased`. El modelo fue pre
entrenado por los autores de BERT con la descarga de las Wikipedias de
104 languages.

### Pre entrenamiento
Una vez que preprocesamos los tweets del corpus UBA utilizamos estos
tweets en el pre entrenamiento no supervisado del modelo pre entrenado
para obtener un modelo de representación del lenguaje específico para
Twitter en español.

Es importante notar que BERT intenta minimizar el error de dos tareas
no supervisadas distintas. Por un lado intenta minimizar el error de
la tarea Masked LM y por otro intenta minimizar el error de la tarea
de Next Sentence Prediction. Explicamos brevemente ambas tareas a
continuación.

#### Masked LM

Si bien es razonable creer que un model bidireccional es
inmediatamente superior a los modelos unidireccionales, los modelos de
lenguaje condicionales usuales sólo pueden ser entrenados de forma
unidireccional, debido a que un condicionamiento bidireccional podría
permitir a cada palabra poder observarse a sí misma, por lo que el
modelo podría predecir fácilmente la palabra objetivo en el contexto
de una red neuronal con muchas capas. Para resolver este problema,
los autores de BERT primero enmascaran un porcentaje de los tokens
aleatoriamente y luego intentan hacer que la red prediga los tokens
enmascarados utilizando la información del contexto. Esta tarea
utilizada para entrenar el modelo es denominada por los autores como
"Masked LM".

#### Next Sentence Prediction

Los autores de BERT también entrenaron BERT usando la tarea de Next
Sentence Prediction (NSP). Esta tarea consiste en determinar si una
oración es la siguiente oración de otra oración. De esta forma el
modelo puede capturar las relaciones entre oraciones. Si bien esta
tarea es muy útil cuando se quiere utilizar BERT para resolver
problemas como Question Answering, para nuestros fines es
completamente prescindible, puesto que por lo general los tweets
contienen una o pocas oraciones. Por este motivo no pre entrenamos
BERT en esta tarea.

### Creando los datos para el pre entrenamiento

Antes de poder pre entrenar el modelo, fue necesario crear los datos
para el pre entrenamiento utilizando el corpus de
UBA. Afortunadamente, el equipo de Google ofrece un script sencillo
que hace justamente esto. El script toma un archivo con una oración
por cada línea del archivo y devuelve un conjunto de ejemplos en el
formato adecuado serializados en el formato TFRecord. Una vez creado
este archivo podemos ejecutar el pre entrenamiento.

### Hiperparámetros del pre entrenamiento

Para el pre entrenamiento es necesario dar ciertos hiperparámetros al
algoritmo. En la siguiente tabla damos los valores de cada hiper
parámetro utilizado.

| Parámetro                 | Valor |
|---------------------------|-------|
| `train_batch_size`        |    32 |
| `max_seq_length`          |    64 |
| `max_predictions_per_seq` |    20 |
| `num_train_steps`         | 10000 |
| `num_warmup_steps`        |    10 |
| `learning_rate`           |  2e-5 |


### Ajuste fino del modelo
Una vez obtenido el modelo de representación del lenguaje es necesario
ajustar el modelo para la tarea específica de clasificación de
polaridad de tweets en español. Para ello, hicimos un ajuste fino del
modelo utilizando el conjunto de datos Inter TASS 2019 para

### Hiperparámetros del ajuste fino del modelo

Para el ajuste fino del modelo también es necesario dar ciertos
hiperparámetros al algoritmo. En la siguiente tabla damos los valores
de cada hiper parámetro utilizado.

| Parámetro                 | Valor |
|---------------------------|-------|
| `max_seq_length`          |    64 |
| `train_batch_size`        |    32 |
| `learning_rate`           |  2e-5 |
| `num_train_epochs`        |     2 |

## Código fuente e Instrucciones

El preprocesamiento, pre entrenamiento y entrenamiento pueden ser
ejecutados fácilmente utilizando el Makefile.

### Preprocesamiento

El código fuente para el preprocesamiento puede encontrarse en
`scripts/preprocess`. En este directorio se encuentran cuatro modulos
de python. Por un lado tenemos un módulo que implementa la lectura del
formato intertass llamado `tass.py`. Por otra parte tenemos un archivo
`clean.py` que implementa la lógica para el preprocesamiento de datos
descripta en este documento. Y finalmente los módulos
`clean_intertass.py` y `clean_uba.py` se encargan de implementar el
preprocesamiento para los conjuntos de datos intertass y uba.

Para ejecutar el preprocesamiento sobre el conjunto de datos intertass
basta hacer:

```
make intertass
```

Para ejecutar el preprocesamiento sobre el conjunto de datos uba basta
hacer:

```
make uba
```

Para ejecutarlo sobre ambos:

```
make preprocess
```

### Pre pre entrenamiento (o creación de datos para pre entrenamiento)

Como dijimos antes, es necesario crear los datos en el formato
adecuado antes de ejecutar el pre entrenamiento. El código fuente que
implementa es el mismo que el provisto por los desarrolladores de BERT
que puede ser encontrado en el repositorio de BERT. En nuestro
repositorio este código puede encontrarse en el archivo
`scripts/train/create_pretraining_data.py`.

Para ejecutar el pre pre entranamiento:

```
make prepretrain
```

### Pre entrenamiento

El código del pre entrenamiento es el mismo que el provisto por los
desarrolladores de BERT. Lo modificamos para que calculara el error
basandose únicamente en el error de la tarea `Masked LM` y que
ignorara el error de la tarea `NSP`. En nuestro repositorio este
código puede encontrarse en el archivo
`scripts/train/run_pretraining.py`.

Para ejecutar el pre entranamiento:

```
make pretrain
```

### Ajuste fino del modelo

El código del entrenamiento es el mismo que el provisto por los
desarrolladores de BERT. Lo modificamos para que pudiera tomar los
datos de TASS y entrenara de manera apropiada a la tarea de
clasificación de polaridad de tweets. En nuestro repositorio este
código puede encontrarse en el archivo
`scripts/train/run_classifier.py`.

Para ejecutar el entranamiento:

```
make train
```

## Resultados

Lamentablemente no pudimos pre entrenar el modelo con el conjunto de
datos completo de uba debido a limitaciones de tiempo. Sólo pre
entrenamos el algoritmo con un 15% de los datos obteniendo resultados
poco alentadores.

Los resultados de la ejecución pueden encontrarse en el directorio
`log`.

## Conclusiones

En este trabajo pudimos utilizar BERT para la clasificación de
polaridad de tweets en español. Sin embargo, debido a las limitaciones
de tiempo, no pudimos determinar si BERT puede ser utilizado para esta
tarea puesto que no obtuvimos resultados alentadores con la escasa
cantidad de datos que utilizamos para pre entrenar el modelo. Queda
claro que es necesario pre entrenar BERT con un conjunto de datos muy
superior al utilizado en este trabajo. En primer lugar, sería
interesante pre entrenar BERT utilizando el conjunto de datos completo
de uba. Si no se obtienen buenos resultados, es posible que pre
entrenar BERT `base` con la descarga de Wikipedia en español para
luego continuar este pre entrenamiento con el conjunto de datos uba
obtenga mejores resultados.

El principal aporte de este trabajo es haber codificado la estructura
necesaria para el uso de BERT para la clasificación de polaridad de
tweets en español. Usuarios interesados en entrenar BERT utilizando el
conjunto de datos completos de uba simplemente tienen que usar la
interfaz implementada mediante el Makefile.
