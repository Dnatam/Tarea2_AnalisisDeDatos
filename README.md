# Tarea 2 - Análisis de Datos

**Curso:** Curso Libre de Configuración 2: Análisis de Datos  
**Autora:** Daniela Natareno  
**Fecha de entrega:** 20 de septiembre de 2026  

## Descripción

Este repositorio contiene el desarrollo de la **Tarea 2 del curso de Análisis de Datos**.

El trabajo se divide en dos partes principales:

- **Parte 1 - Generadores pseudoaleatorios:** implementación y análisis de diferentes generadores de números pseudoaleatorios.
- **Parte 2 - Monte Carlo:** aplicación de métodos de Monte Carlo para integración, análisis en alta dimensión, reducción de varianza y estudio del efecto de la calidad del generador pseudoaleatorio.

---

## Estructura del repositorio

```text
Tarea2_AnalisisDeDatos/
│
├── Parte1-Generadores/
│   ├── 1.LCG/
│   │   └── LCG.py
│   │
│   ├── 2.MSM/
│   │   └── MSM.py
│   │
│   ├── 3.MT/
│   │   └── MT19937.py
│   │
│   ├── 4.BBS/
│   │   └── BBS.py
│   │
│   ├── 5.RANDU/
│   │   └── RANDU.py
│   │
│   ├── d.Comparacion_MT.py
│   └── Parte1_PRNG_DanielaNatareno.pdf
│
├── Parte2-MonteCarlo/
│   │
│   ├── 3.1.Fundamento/
│   │   ├── 3.1.1.jpeg
│   │   ├── 3.1.2.jpeg
│   │   └── 3.1.3.jpeg
│   │
│   ├── 3.2.Python/
│   │   ├── IncisoA/
│   │   │   ├── ComparacionGeneradores.py
│   │   │   ├── Estimador1MonteCarlo.py
│   │   │   └── convergencia_integral_a.png
│   │   │
│   │   └── IncisoB/
│   │       ├── ComparacionGeneradores2.py
│   │       ├── Estimador2MonteCarlo.py
│   │       └── convergencia_integral_b.png
│   │
│   ├── 3.3AltaDimension/
│   │   ├── FraccionVolumen.py
│   │   ├── MonteCarloRejilla.py
│   │   ├── VolumenBolaMonteCarlo.py
│   │   └── fraccion_volumen.png
│   │
│   ├── 3.4.ReduccionDeVarianza/
│   │   ├── VariablesAntiteticas.py
│   │   └── VariablesControl.py
│   │
│   └── 3.5.GeneradorArruinaResultado/
│       ├── RANDUMonteCarlo.py
│       ├── puntos_3d_randu.png
│       └── puntos_3d_mt19937.png
│
├── requirements.txt
└── README.md
```

---

# Parte 1 - Generadores pseudoaleatorios

En esta sección se implementan y analizan diferentes algoritmos para la generación de números pseudoaleatorios.

Los generadores estudiados son:

- Linear Congruential Generator (LCG).
- Middle-Square Method (MSM).
- Mersenne Twister MT19937.
- Blum Blum Shub (BBS).
- RANDU.

Además de generar las secuencias, se realizan diferentes pruebas estadísticas y visuales para analizar su comportamiento.

---

## 1. Linear Congruential Generator - LCG

Implementación de un **generador congruencial lineal** 

Archivo principal:

```text
Parte1-Generadores/1.LCG/LCG.py
```

El programa incluye:

- Generación de números pseudoaleatorios.
- Normalización de los valores.
- Prueba de uniformidad Kolmogorov-Smirnov.
- Prueba de independencia serial.
- Verificación de las condiciones de Hull-Dobell.
- Histograma de los valores generados.
- Prueba espectral visual.

---

## 2. Middle-Square Method - MSM

Implementación del **método de cuadrados medios**.

Archivo principal:

```text
Parte1-Generadores/2.MSM/MSM.py
```

El experimento permite observar algunas de las principales limitaciones del método, como la aparición de ciclos cortos y la posibilidad de degenerar hacia valores repetitivos o cero.

---

## 3. Mersenne Twister MT19937

Implementación propia del generador **Mersenne Twister MT19937**.

Archivo principal:

```text
Parte1-Generadores/3.MT/MT19937.py
```

La implementación incluye:

- Vector de estado interno de 624 palabras.
- Inicialización del estado.
- Transformación `twist`.
- `Tempering`.
- Normalización de los valores generados.
- Prueba de uniformidad Kolmogorov-Smirnov.
- Prueba de independencia serial.
- Histograma.
- Prueba espectral visual.

MT19937 posee un período de:

\[
2^{19937}-1
\]

---

## 4. Blum Blum Shub - BBS

Implementación del generador **Blum Blum Shub**.

Archivo principal:

```text
Parte1-Generadores/4.BBS/BBS.py
```

La implementación incluye validaciones sobre los parámetros utilizados y la generación de la secuencia pseudoaleatoria.

---

## 5. RANDU

Implementación del generador **RANDU**

Archivo principal:

```text
Parte1-Generadores/5.RANDU/RANDU.py
```

El programa incluye:

- Generación de la secuencia.
- Normalización.
- Prueba de uniformidad Kolmogorov-Smirnov.
- Prueba de independencia serial.
- Histograma.
- Prueba espectral tridimensional.
- Análisis de ternas consecutivas.
- Verificación de los planos característicos de RANDU.

La prueba espectral permite visualizar una de las principales deficiencias de RANDU: al formar puntos tridimensionales con valores consecutivos, estos se distribuyen sobre un número reducido de planos en lugar de llenar uniformemente el espacio.

---

## Comparación de generadores

También se incluye una comparación entre diferentes alternativas para la generación de números pseudoaleatorios.

Archivo:

```text
Parte1-Generadores/d.Comparacion_MT.py
```

Los resultados permiten comparar características estadísticas y visuales de las secuencias producidas por los generadores estudiados.

---

# Parte 2 - Métodos de Monte Carlo

La segunda parte utiliza números pseudoaleatorios para desarrollar diferentes aplicaciones del método de Monte Carlo.

Se estudian:

- Integración mediante Monte Carlo.
- Intervalos de confianza.
- Convergencia del estimador.
- Alta dimensión.
- Maldición de la dimensionalidad.
- Reducción de varianza.
- Influencia de la calidad del generador pseudoaleatorio.

---

## 3.1 Fundamento del estimador

Se desarrolla matemáticamente el estimador de Monte Carlo utilizado para aproximar una integral.

En esta sección se desarrolla:

- Demostración de que el estimador es insesgado.
- Varianza del estimador.
- Error estándar.
- Tasa de convergencia.
- Intervalo de confianza del 95%.

Los desarrollos correspondientes se encuentran en:

```text
Parte2-MonteCarlo/3.1.Fundamento/
```

---

## 3.2 Integración mediante Monte Carlo

Se utilizan simulaciones de Monte Carlo para aproximar dos integrales conocidas y comparar las estimaciones con sus valores teóricos.

---

### Inciso A - Integral de seno

Archivos:

```text
Parte2-MonteCarlo/3.2.Python/IncisoA/
```

El experimento incluye:

- Estimación mediante Monte Carlo.
- Cálculo del error estándar.
- Intervalo de confianza del 95%.
- Error absoluto.
- Estudio de convergencia.
- Gráfica log-log del error.
- Comparación entre `random` de Python y la implementación propia de MT19937.

---

### Inciso B - Integral de la función normal estándar

Archivos:

```text
Parte2-MonteCarlo/3.2.Python/IncisoB/
```

Se realizan los mismos análisis del inciso anterior:

- Estimación.
- Error estándar.
- Intervalo de confianza del 95%.
- Error absoluto.
- Estudio de convergencia.
- Comparación de generadores.

---

## 3.3 Alta dimensión y maldición de la dimensionalidad

Se estudia el volumen de la bola unitaria en \(d\) dimensiones.

Archivos:

```text
Parte2-MonteCarlo/3.3AltaDimension/
```

Se estudian las dimensiones:

```text
d = 2, 5, 10, 20
```

### Estimación mediante Monte Carlo

Se generan puntos uniformes en el hipercubo correspondiente para estimar el volumen de la bola unitaria.

### Comparación con una rejilla determinística

Se compara Monte Carlo con una rejilla.

Permite observar cómo el número de puntos requerido por una rejilla crece exponencialmente conforme aumenta la dimensión.

### Fracción de volumen

Fracción del hipercubo ocupada por la bola unitaria.

El experimento muestra que esta fracción disminuye rápidamente al aumentar la dimensión.

---

## 3.4 Reducción de varianza

Se implementan dos técnicas para reducir la varianza de las estimaciones de Monte Carlo:

1. Variables antitéticas.
2. Variables de control.

Ambas técnicas se comparan con Monte Carlo simple utilizando el mismo número de evaluaciones de la función.

---

### Variables antitéticas

Archivo:

```text
Parte2-MonteCarlo/3.4.ReduccionDeVarianza/VariablesAntiteticas.py
```

La técnica busca generar una relación negativa entre ambas evaluaciones para que sus variaciones se compensen.

El experimento compara:

- Estimación.
- Varianza.
- Error estándar.
- Intervalo de confianza.
- Error absoluto.
- Factor de reducción de varianza.
- Reducción porcentual de varianza.
- `Speedup` estadístico equivalente.

---

### Variables de control

Archivo:

```text
Parte2-MonteCarlo/3.4.ReduccionDeVarianza/VariablesControl.py
```

En la implementación se utiliza una variable de control relacionada con la variable de interés y su coeficiente se estima a partir de las muestras generadas.

El método se compara con Monte Carlo simple utilizando el mismo número de evaluaciones.

---

## 3.5 Cuando un generador arruina el resultado

En esta sección se analiza cómo la calidad de un generador pseudoaleatorio puede afectar una aplicación de Monte Carlo multidimensional.

Archivo:

```text
Parte2-MonteCarlo/3.5.GeneradorArruinaResultado/RANDUMonteCarlo.py
```

Se compara:

- RANDU.
- Mersenne Twister MT19937.

El experimento estima el volumen de la bola unitaria tridimensional.

Los puntos tridimensionales se construyen utilizando ternas de valores pseudoaleatorios consecutivos.

Con RANDU, las ternas presentan una estructura geométrica en planos. Esta estructura puede observarse en:

```text
puntos_3d_randu.png
```

En comparación, los puntos producidos por MT19937 presentan una distribución visualmente más uniforme:

```text
puntos_3d_mt19937.png
```

Además de la visualización, se comparan:

- Número de puntos dentro de la bola.
- Estimación del volumen.
- Error estándar.
- Intervalo de confianza del 95%.
- Error absoluto.

Este experimento muestra que superar pruebas estadísticas simples de uniformidad o correlación no garantiza que un generador sea adecuado para todas las aplicaciones de Monte Carlo, especialmente cuando se utilizan valores consecutivos para construir puntos multidimensionales.

---

# Requisitos

Para ejecutar los programas se requiere:

- Python 3
- Matplotlib
- NumPy
- SciPy

Las dependencias se encuentran en:

```text
requirements.txt
```

El contenido del archivo es:

```text
matplotlib
numpy
scipy
```

---

# Instalación

Primero se debe clonar o descargar el repositorio.

Posteriormente, desde la carpeta principal del proyecto, instalar las dependencias mediante:

```bash
pip install -r requirements.txt
```

---

# Ejecución

Cada programa puede ejecutarse individualmente desde una terminal utilizando:

```bash
python nombre_archivo.py
```

Por ejemplo:

```bash
python Parte2-MonteCarlo/3.4.ReduccionDeVarianza/VariablesAntiteticas.py
```

También puede ingresarse directamente a la carpeta correspondiente:

```bash
cd Parte2-MonteCarlo/3.4.ReduccionDeVarianza
```

y ejecutar:

```bash
python VariablesAntiteticas.py
```

Algunos programas generan automáticamente archivos `.png` correspondientes a:

- Histogramas.
- Pruebas espectrales.
- Gráficas de convergencia.
- Análisis de volumen.
- Visualizaciones tridimensionales.

---

# Reproducibilidad

Para facilitar la reproducción de los experimentos se utilizó principalmente la semilla:

```text
8103
```

Los tamaños de muestra y demás parámetros utilizados se encuentran definidos directamente dentro de cada programa.

Entre los experimentos se utilizan diferentes cantidades de muestras dependiendo del análisis realizado, incluyendo tamaños de hasta:

```text
N = 1000000
```

Los resultados pueden variar al modificar:

- La semilla.
- El número de muestras.
- Los parámetros de los generadores.
- Los parámetros particulares de cada experimento.

---

# Documentación

Los fundamentos matemáticos, resultados, tablas, gráficas, análisis e interpretación de los experimentos se encuentran desarrollados en los documentos PDF correspondientes a cada parte de la tarea.

El código fuente contenido en este repositorio permite reproducir los experimentos realizados y generar las gráficas utilizadas en la documentación.

Se adjuntan las carpetas `.zip` de cada parte del trabajo, las cuales incluyen el archivo `.tex` y una carpeta con las figuras utilizadas.