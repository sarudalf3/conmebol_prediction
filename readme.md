## Predicción de los resultados de fútbol para las clasificatorias sudamericanas del mundial de Qatar 2022 

En esta oportunidad, desarrollé una simple solución al problema de predicción de resultados de fútbol modelando los 
goles convertidos por las selecciones nacionales pertenecientes a Conmebol. Los registros se seleccionaron usando la técnica de Webscrapping y comprenden los resultados entre las clasificatorias para el mundial de Francia 1998 y Qatar 2022.

*Nota del autor: Este modelo es una simple aplicación de modelos estadísticos, en la que no se realizó la validación de supuestos, y tiene un enfoque más académico. Hay técnicas más precisas que necesitan mayor información (posesión de balón, pases realizados,..)*

1. Introducción
    
    A días de las últimos partidos de fútbol para las clasificatorias Conmebol para la copa del mundo de Qatar 2022, busqué una técnica sencilla para predecir los partidos de las últimas 2 fechas y el partido pendiente entre Brasil y Argentina. Para este análisis se utilizaron los resultados de todos los partidos clasificatorios desde el mundial de Francia 1998, siendo esta la primera clasificatoria en la que empezó el sistema de partidos de todos contra todos. El foco es modelar los goles convertidos mediante un modelo lineal general generalizado (GLM) asumiendo que tienen una distribución Poisson; usando como variables independientes los equipos Oponentes, la situación de localia y los goles convertidos por los equipos oponentes.  

2. Extracción y limpieza de información

    La extracción de información se realizó usando técnicas de Webscrapping. La información se obtuvo de la biblioteca libre *Wikipedia* s para las clasificatorias de los mundiales de [Francia, 1998](https://en.wikipedia.org/wiki/1998_FIFA_World_Cup_qualification_(CONMEBOL)),
[Korea - Japon, 2002](https://en.wikipedia.org/wiki/2002_FIFA_World_Cup_qualification_(CONMEBOL)), [Alemania, 2006](https://en.wikipedia.org/wiki/2006_FIFA_World_Cup_qualification_(CONMEBOL)), [Sudafrica, 2010](https://en.wikipedia.org/wiki/2010_FIFA_World_Cup_qualification_(CONMEBOL)), [Brazil, 2014](https://en.wikipedia.org/wiki/2014_FIFA_World_Cup_qualification_(CONMEBOL)), [Rusia, 2018](https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_qualification_(CONMEBOL)) y [Qatar, 2022](https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_qualification_(CONMEBOL)).

    El script Scrapping_conmebol.py contiene los detalles de la extracción de información y tienen el siguiente formato.

    ```python
        import Scrapping_conmebol as scrap

        database = scrap.database
        database.sample(7)
    ```
    
    |date|World Cup Qualif|Team_home|Team_away|Goals_home|Goals_away|
    |:---:|:---:|:---:|:---:|:---:|:---:|
    |1997-04-02|1998|Bolivia|Argentina|2.0|1.0|
    |2009-04-01|2010|Chile|Uruguay|0.0|0.0|
    |2000-11-15|2002|Paraguay|Peru|5.0|1.0|
    |2022-03-29|2022|Venezuela|Colombia|NaN|NaN|
    |1997-07-20|1998|Bolivia|Uruguay|1.0|0.0|
    |2001-03-28|2002|Ecuador|Brazil|1.0|0.0|
    |2017-10-05|2018|Venezuela|Uruguay|0.0|0.0|

    No es necesaria una limpieza de datos, aunque es necesario determinar los partidos a predecir.

    |date|World Cup Qualif|Team_home|Team_away|Goals_home|Goals_away|
    |:---:|:---:|:---:|:---:|:---:|:---:|
    |2021-09-05|2022|Brazil|Argentina|NaN|NaN|
    |2022-03-24|2022|Uruguay|Peru|NaN|NaN|
    |2022-03-24|2022|Colombia|Bolivia|NaN|NaN|
    |2022-03-24|2022|Brazil|Chile|NaN|NaN|
    |2022-03-24|2022|Paraguay|Ecuador|NaN|NaN|
    |2022-03-25|2022|Argentina|Venezuela|NaN|NaN|
    |2022-03-29|2022|Peru|Paraguay|NaN|NaN|
    |2022-03-29|2022|Venezuela|Colombia|NaN|NaN|
    |2022-03-29|2022|Bolivia|Brazil|NaN|NaN|
    |2022-03-29|2022|Chile|Uruguay|NaN|NaN|
    |2022-03-29|2022|Ecuador|Argentina|NaN|NaN|

    El objetivo es predecir estos partidos usando información de los partidos anteriores.

3. Análisis descriptivo

    En el conjunto de datos existen 6 variables, y son las siguientes:

    ```python
    >>>
    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 583 entries, 0 to 583
    Data columns (total 6 columns):
    #   Column            Non-Null Count  Dtype         
    ---  ------            --------------  -----         
    0   date              583 non-null    datetime64[ns]
    1   World Cup Qualif  583 non-null    int64         
    2   Team_home         583 non-null    object        
    3   Team_away         583 non-null    object        
    4   Goals_home        583 non-null    float64       
    5   Goals_away        583 non-null    float64       
    dtypes: datetime64[ns](1), float64(2), int64(1), object(2)
    memory usage: 31.9+ KB
    ```

    Existen 583 registros (partidos) que van a ser utilizados en la construcción del modelo. 
    Antes del modelo, vamos a observar detalladamente los goles convertidos en los partidos en el período de análisis.

	||Goals_home|Goals_away|
    |:---:|:---:|:---:|
    |count|583.000000|583.000000|
    |mean|1.675815|0.943396|
    |std|1.395703|1.039703|
    |min|0.000000|0.000000|
    |25%|1.000000|0.000000|
    |50%|1.000000|1.000000|
    |75%|2.500000|1.000000|
    |max|6.000000|6.000000|   

    Se puede concluir que en promedio el equipo de local convierte más goles que el equipo visitante. El máximo de goles convertidos es 6. Ahora revisamos la 

    ![Frecuencia de goles](/img/goals_descriptive.png) 

5. Propuestas 

    Una alternativa de análisis es dar mayor importancia a los registros más actuales, ponderando pesos mayores a los partidos de la actual clasificatoria y menos importancia a los partidos más antiguos. 