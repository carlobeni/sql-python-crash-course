# Test de Preguntas Desafiantes - Día 6: Data Prep & ML

Evaluación sobre Imputación de Missings, Métodos de Outliers (IQR / Z-Score), Binning y Preprocesamiento.

---

### Pregunta 1: Diferencia Crítica entre `pd.cut` y `pd.qcut`
Tienes una variable `ingreso` fuertemente sesgada a la derecha donde el 90% de las personas ganan entre $100,000 y $500,000, pero un 1% gana $50,000,000. Necesitas dividir a los clientes en 4 grupos con la **misma cantidad de personas por grupo** para análisis de cuartiles.

¿Qué función debes utilizar obligatoriamente?

- A) `pd.cut(df['ingreso'], bins=4)`
- B) `pd.qcut(df['ingreso'], q=4)`
- C) `np.histogram(df['ingreso'], bins=4)`
- D) `scipy.stats.zscore(df['ingreso'])`

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** `pd.cut` divide el rango de valores (min a max) en 4 intervalos numéricos de igual ancho, provocando que casi todas las personas queden amontonadas en el primer bin y el último bin tenga solo a los millonarios. `pd.qcut` divide por cuantiles (percentiles), garantizando que **cada uno de los 4 bins contenga exactamente el 25% de la población**.
</details>

---

### Pregunta 2: Detección de Outliers con IQR
En una distribución de saldos con $Q1 = 50,000$ ARS y $Q3 = 200,000$ ARS:
¿A partir de qué monto superior un cliente es etiquetado formalmente como **Outlier** según el método de IQR con factor 1.5?

- A) $200,000$ ARS
- B) $350,000$ ARS
- C) $425,000$ ARS
- D) $500,000$ ARS

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: C**

**Explicación:** 
1. Pasos de cálculo: $IQR = Q3 - Q1 = 200,000 - 50,000 = 150,000$.
2. Límite Superior: $L_{sup} = Q3 + 1.5 \times IQR = 200,000 + 1.5 \times (150,000) = 200,000 + 225,000 = 425,000$ ARS.
Todo monto $> 425,000$ ARS es un Outlier.
</details>

---

### Pregunta 3: Imputación de Missings en Distribuciones Asimétricas
¿Por qué se prefiere la **Mediana** sobre la **Media** para imputar saldos o ingresos nulos en modelos de scoring crediticio?

- A) Porque la mediana siempre calcula un número entero.
- B) Porque la media es altamente sensible a valores extremadamente altos (outliers), sesgando el valor imputado hacia arriba, mientras que la mediana es una medida de posición robusta.
- C) Porque la mediana elimina automáticamente las filas nulas del DataFrame.
- D) Porque Scikit-Learn no soporta imputaciones con la media.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** Las variables monetarias (ingresos, saldos, patrimonio) suelen tener distribución asimétrica a la derecha (right-skewed). La media se ve arrastrada por los millonarios, resultando en un valor imputado irrealmente alto para clientes de ingresos típicos. La mediana representa el percentil 50 real y no se ve afectada por valores extremos atípicos.
</details>

---

### Pregunta 4: Data Leakage en Preprocesamiento de ML
¿Cuál de los siguientes flujos de preprocesamiento incurre en el error grave conocido como **Data Leakage (Fuga de Datos)**?

- A) Dividir en Train/Test y ajustar (`fit`) el `StandardScaler` solo con el conjunto de Train.
- B) Ajustar (`fit_transform`) el `StandardScaler` sobre todo el dataset **antes** de realizar la división en conjuntos de Entrenamiento y Evaluación (Train/Test Split).
- C) Imputar nulos utilizando la mediana calculada dentro de cada fold durante validación cruzada.
- D) Aplicar `OneHotEncoder` convirtiendo variables de texto a dummies.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** Si aplicas `fit` a todo el dataset antes del split, las estadísticas del conjunto de evaluación/test (media y desviación estándar) se filtran dentro de los datos de entrenamiento. Esto distorsiona la evaluación del modelo, ofreciendo métricas artificialmente optimistas que luego fallan en producción.
</details>
