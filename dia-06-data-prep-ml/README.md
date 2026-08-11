# Día 6: Data Prep - Data Preparation Transversal & Matplotlib/ML

Bienvenido al Día 6 del Plan Intensivo de Preparación Acelerada para Evaluación Técnica (Itaú).

---

## Objetivos del Día
1. Tratar valores faltantes (**Missings**): Detección (`isnull()`, `isna()`) y estrategias de Imputación (media/mediana, ffill/bfill) vs Eliminación (`dropna()`).
2. Detección y tratamiento de **Outliers** (Valores Atípicos) mediante el Rango Intercuartílico (**IQR**) y **Z-Score**, así como visualización gráfica con Boxplots.
3. Categorización y Discretización de variables continuas (**Binning**): `pd.cut` vs `pd.qcut` y su relación con `CASE WHEN` en SQL.
4. Comprender conceptos de preprocesamiento en **Scikit-Learn** (`StandardScaler`, `MinMaxScaler`, `OneHotEncoder`).

---

## Teoría Explicada

### 1. Tratamiento de Missings (Valores Faltantes)

En análisis financiero, los datos nulos pueden generar sesgos en las métricas o fallos en los modelos.

#### A. Detección
* En Pandas: `df['col'].isnull()` o `df['col'].isna()`.
* Conteo global: `df.isnull().sum()`

#### B. Eliminación vs Imputación
* **Eliminación (`dropna()`):** Recomendada solo si la proporción de nulos es baja (< 5%) o si la fila carece de identificadores esenciales.
* **Imputación por Tendencia Central:**
  * **Media (`df['col'].fillna(df['col'].mean())`):** Sensible a valores extremos (outliers).
  * **Mediana (`df['col'].fillna(df['col'].median())`):** Robusta frente a outliers. Preferida en distribuciones asimétricas (como ingresos o saldos).
* **Imputación por Secuencia:** `ffill` (forward fill) o `bfill` (backward fill). Utilizado en series temporales financieras.

```python
# Imputación por mediana agrupada por segmento
df['ingreso_imputado'] = df.groupby('segmento')['ingreso'].transform(
    lambda group: group.fillna(group.median())
)
```

---

### 2. Detección y Tratamiento de Outliers

#### A. Método del Rango Intercuartílico (IQR - Interquartile Range)
Método robusto para distribuciones no normales.

* **Primer Cuartil ($Q1$ / Percentil 25):** `Q1 = df['col'].quantile(0.25)`
* **Tercer Cuartil ($Q3$ / Percentil 75):** `Q3 = df['col'].quantile(0.75)`
* **$IQR = Q3 - Q1$**
* **Límite Inferior:** $L_{inf} = Q1 - 1.5 \times IQR$
* **Límite Superior:** $L_{sup} = Q3 + 1.5 \times IQR$

Todo valor por debajo de $L_{inf}$ o por encima de $L_{sup}$ es considerado un outlier.

```python
Q1 = df['monto'].quantile(0.25)
Q3 = df['monto'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

# Acotamiento / Capping de Outliers (Winsorización)
df['monto_capped'] = np.clip(df['monto'], limite_inferior, limite_superior)
```

#### B. Método Z-Score
Asume que los datos siguen una Distribución Normal ($\mu$, $\sigma$).
$$Z = \frac{x - \mu}{\sigma}$$
Valores con $|Z| > 3$ se clasifican como outliers.

---

### 3. Categorización y Discretización de Variables (Binning)

Conversión de variables numéricas continuas en categorías discretas:

* **`pd.cut(x, bins)` (Bins de Ancho Constante):** Divide el rango de datos en intervalos de igual amplitud matemática.
* **`pd.qcut(x, q)` (Bins de Frecuencia / Cuantiles Igualitarios):** Divide los datos de forma que cada categoría contenga aproximadamente la misma cantidad de observaciones.

#### Comparativa con `CASE WHEN` en SQL

| Operación en Pandas | Equivalente T-SQL |
| :--- | :--- |
| `pd.cut(df['edad'], bins=[0, 18, 65, 100], labels=['Joven', 'Adulto', 'Senior'])` | `CASE WHEN edad <= 18 THEN 'Joven' WHEN edad <= 65 THEN 'Adulto' ELSE 'Senior' END` |
| `pd.qcut(df['ingreso'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])` | `NTILE(4) OVER (ORDER BY ingreso)` |

---

### 4. Preprocesamiento con Scikit-Learn

Antes de entrenar un modelo predictivo, las variables deben escalarse para evitar que features de magnitud elevada dominen el algoritmo:

* **`StandardScaler`**: Normalización Z-score ($\mu = 0, \sigma = 1$).
* **`MinMaxScaler`**: Escala al rango $[0, 1]$.
* **`OneHotEncoder` / `pd.get_dummies()`**: Convierte variables categóricas nominales en columnas binarias.

> **Prevención de Data Leakage:** El escalador (`fit`) se debe calcular únicamente sobre el conjunto de entrenamiento (train) y posteriormente aplicarse (`transform`) sobre el conjunto de validación o prueba.
