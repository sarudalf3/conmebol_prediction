## Predicción de los resultados de fútbol para las clasificatorias sudamericanas para el mundial de Qatar 2022 

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

    No es necesaria una limpieza de datos, aunque es necesario extraer los 11 partidos que aún no se realizan.

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
    Antes del modelo vamos a analizar detalladamente los goles convertidos en los partidos que se encuentran en el período de análisis.

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

    Se puede concluir que en promedio el equipo de local convierte más goles que el equipo visitante. El máximo de goles convertidos es 6. Para mayor detalle se utiliza un gráfico de frecuencias para los goles tanto de visita como de local.

    <div class="image_center mb-4 mt-2">
        <img src="/img/goals_descriptive.png" alt="system device" style="max-width: 100%; max-height: 100%; height: 280px;" />
    </div>

    Se observa que menor a 2 goles, la mayor frecuencia esta en los equipos visitantes, mientras que para una cantidad mayor a de 1 gol hay una frecuencia más favorable del equipo local.

    Al ser un valor discreto con mayor frecuencia en los primeros valores y decayendo fuertemente a medida que la cantidad de goles convertidos aumenta, es plausible asumir que estos conllevan una distribución Poisson y mediante estimación de máxima verosimilitud, se estima el parámetro <img src="https://render.githubusercontent.com/render/math?math=\Large \lambda"> con el promedio de goles convertidos.



    <div class="image_center mb-4 mt-2">
        <img src="/img/goals_predictive.png" alt="system device" style="max-width: 100%; max-height: 100%; width: 650px;" />
    </div>

    En el caso de los goles de local es estimó un <img src="https://render.githubusercontent.com/render/math?math= \large \lambda = 1.68"> y para los goles de visita es de <img src="https://render.githubusercontent.com/render/math?math=\LARGE \lambda=0.94">.

4. Construcción del modelo

    Para la construcción del modelo 

    ```python
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    ```

    ```python
    goals = pd.concat([df[['Team_home','Team_away','Goals_home']].assign(Home=1).
    rename(columns={'Team_home':'Team', 'Team_away':'Opponent','Goals_home':'goals'}), 
    df[['Team_home','Team_away','Goals_away']].assign(Home=0).
    rename(columns={'Team_away':'Team', 'Team_home':'Opponent','Goals_away':'goals'})])

    poisson_model = smf.glm(formula="goals ~ Home + Team + Opponent", 
        data=goals, family=sm.families.Poisson()).fit()
    poisson_model.summary()

    >>>
               Generalized Linear Model Regression Results
            Dep. Variable: goals	    No. Observations: 1166
            Model: GLM	                Df Residuals: 1146
            Model Family: Poisson	    Df Model: 19
            Link Function: Log	        Scale: 1.0000
            Method: IRLS	            Log-Likelihood: -1640.3
            Date: Mon, 21 Mar 2022	    Deviance: 1319.4
            Time: 18:21:44	            Pearson chi2: 1.17e+03
            No. Iterations:	5           Pseudo R-squ. (CS): 0.2221
            Covariance Type:    nonrobust		

                            coef  std err	     z	P>|z|	[0.025	0.975]
    Intercept            -0.2571	0.130	-1.983	0.047	-0.511	-0.003
    Home                  0.5751	0.053	10.787	0.000	 0.471	 0.680
    Team[T.Bolivia]	     -0.2707	0.112	-2.407	0.016	-0.491	-0.050
    Team[T.Brazil]	      0.1975	0.105	 1.880	0.060	-0.008	 0.404
    Team[T.Chile]	     -0.0950	0.106	-0.899	0.369	-0.302	 0.112
    Team[T.Colombia]     -0.2866	0.110	-2.597	0.009	-0.503	-0.070
    Team[T.Ecuador]	     -0.1685	0.107	-1.572	0.116	-0.379	 0.042
    Team[T.Paraguay]     -0.2856	0.111	-2.571	0.010	-0.503	-0.068
    Team[T.Peru]	     -0.3964	0.115	-3.435	0.001	-0.623	-0.170
    Team[T.Uruguay]	     -0.1424	0.107	-1.334	0.182	-0.352	 0.067
    Team[T.Venezuela]    -0.4407	0.118	-3.733	0.000	-0.672	-0.209
    Opponent[T.Bolivia]   0.7567	0.119	 6.338	0.000	 0.523	 0.991
    Opponent[T.Brazil]   -0.2042	0.162	-1.260	0.208	-0.522	 0.113
    Opponent[T.Chile]     0.4241	0.127	 3.339	0.001	 0.175	 0.673
    Opponent[T.Colombia]  0.0572	0.136	 0.420	0.675	-0.210	 0.324
    Opponent[T.Ecuador]   0.3121	0.129	 2.413	0.016	 0.059	 0.566
    Opponent[T.Paraguay]  0.3568	0.128	 2.790	0.005	 0.106	 0.607
    Opponent[T.Peru]      0.4972	0.124	 4.001	0.000	 0.254	 0.741
    Opponent[T.Uruguay]   0.3353	0.129	 2.600	0.009	 0.083	 0.588
    Opponent[T.Venezuela] 0.7269	0.119	 6.085	0.000	 0.493	 0.961

    
    ```

6. Predicción

    ```python
    def match_results(Team, Opponent):
        home_res = np.round(poisson_model.predict(
            pd.DataFrame(data={'Team': Team, 'Opponent': Opponent,'home':1},index=[1])),0)
        away_res = np.round(poisson_model.predict(
            pd.DataFrame(data={'Team': Opponent, 'Opponent': Team,'home':0},index=[1])),0)
        database.loc[(database.Team_home==Team)&(database.Team_away==Opponent)&
            (database.index.isin(index_na)),'Goals_home'] = home_res.values
        database.loc[(database.Team_home==Team)&(database.Team_away==Opponent)&
            (database.index.isin(index_na)),'Goals_away'] = away_res.values  
        return print(f'{Team} {home_res.values[0]:.0f} - {away_res.values[0]:.0f} {Opponent}')

    match_results('Brazil', 'Argentina')
    match_results('Uruguay', 'Peru')
    match_results('Colombia', 'Bolivia')
    match_results('Brazil', 'Chile')
    match_results('Paraguay', 'Ecuador')
    match_results('Argentina', 'Venezuela')
    match_results('Peru', 'Paraguay')
    match_results('Venezuela', 'Colombia')
    match_results('Bolivia', 'Brazil')
    match_results('Chile', 'Uruguay')
    match_results('Ecuador', 'Argentina')    
    >>>
    Brazil    2 - 1  Argentina
    Uruguay   2 - 1  Peru
    Colombia  2 - 1  Bolivia
    Brazil    3 - 1  Chile
    Paraguay  1 - 1  Ecuador
    Argentina 3 - 0  Venezuela
    Peru      1 - 1  Paraguay
    Venezuela 1 - 1  Colombia
    Bolivia   1 - 2  Brazil
    Chile     2 - 1  Uruguay
    Ecuador   1 - 1  Argentina
    ```

7. Conclusión

<div align="center">

|Pos|Team|Points|Goals dif|
|:---|:---:|:---:|:---:|
|1|Brazil|48|31|
|2|Argentina|39|18|
|3|Ecuador|27|10|
|4|Uruguay|25|-3|
|5|Chile|22|-2|
|6|Peru|22|-5|
|7|Colombia|21|-2|
|8|Bolivia|15|-14|
|9|Paraguay|15|-14|
|10|Venezuela|11|-19|

</div>

8. Propuestas de mejora 

    Una alternativa de análisis es dar mayor importancia a los registros más actuales, ponderando pesos mayores a los partidos de la actual clasificatoria y menos importancia a los partidos más antiguos. 