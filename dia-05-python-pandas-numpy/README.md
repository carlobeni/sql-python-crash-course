# Día 5: Python Data - Análisis de Datos con Pandas & NumPy

Bienvenido al Día 5 del Plan Intensivo de Preparación Acelerada para Evaluación Técnica (Itaú).

---

## Objetivos del Día
1. Comprender la estructura de arrays n-dimensionales en **NumPy** y la importancia de las operaciones vectorizadas frente a bucles `for`.
2. Dominar las estructuras principales de **Pandas**: `Series` y `DataFrames`.
3. Dominar la indexación explícita e implícita (`loc` vs `iloc`) y filtros booleanos condicionales.
4. Realizar agregaciones complejas con `groupby()` y uniones de estructuras con `merge()` y `concat()`.

---

## Teoría Explicada

### 1. NumPy: Computación Vectorizada

NumPy proporciona el objeto `ndarray`, una estructura de memoria contigua optimizada para cálculo numérico de alto rendimiento.

* **Operaciones Vectoriales:** Operaciones matemáticas aplicadas a todo el arreglo simultáneamente sin necesidad de iterar manualmente elemento por elemento.
* **Broadcasting:** Capacidad de NumPy para realizar operaciones aritméticas sobre arreglos de diferentes formas (shapes) compatibles.

```python
import numpy as np

saldos_ars = np.array([150000.0, 45000.0, 1200000.0, 320000.0])

# Operación vectorial (Mucho más rápida que un loop en Python puro)
saldos_con_interes = saldos_ars * 1.05
saldos_dolares = saldos_ars / 1200.0
```

---

### 2. Pandas: Series y DataFrames

* **`Series`**: Arreglo unidimensional etiquetado (columna única con índice).
* **`DataFrame`**: Estructura bidimensional con columnas potencialmente heterogéneas y un índice común.

```python
import pandas as pd

df_cuentas = pd.DataFrame({
    'cliente_id': [101, 102, 103, 104],
    'segmento': ['Premium', 'Retail', 'Corporate', 'Retail'],
    'saldo_ars': [2500000.0, 45000.0, 15800000.0, 0.0],
    'mora': [False, True, False, False]
})
```

---

### 3. Indexación y Filtrado Booleano (`loc` vs `iloc`)

Diferenciación entre métodos de selección:

* **`.loc[filas, columnas]`**: Indexación basada en **ETIQUETAS / NOMBRES**.
  * Si se pasa un rango `'A':'C'`, es **INCLUSIVO** en ambos extremos.
  * Acepta condiciones booleanas.
* **`.iloc[filas, columnas]`**: Indexación basada en **POSICIONES ENTERAS** (0-indexed).
  * Los rangos `0:3` son **EXCLUSIVOS** del extremo derecho (igual que slicing de listas).

```python
# 1. Seleccionar filas por posición (primeras 2 filas, columnas 0 a 2)
df_sub = df_cuentas.iloc[0:2, 0:2]

# 2. Filtrado Booleano condicional (Operadores bitwise &, |, ~ obligatorios con paréntesis)
df_premium_sin_mora = df_cuentas.loc[
    (df_cuentas['segmento'] == 'Premium') & (~df_cuentas['mora']),
    ['cliente_id', 'saldo_ars']
]
```

---

### Regla de Oro Itaú #4: Operaciones Orientadas a DataFrames

> **Regla de Evaluación:**
> Se debe evitar el uso de bucles `for` (como `for index, row in df.iterrows():`) para recorrer DataFrames.
> **Uso de métodos vectorizados integrados:** `fillna()`, `dropna()`, `apply()`, `groupby()`, `merge()`.

```python
# INCORRECTO Y LENTO: Recorrer con bucle for
for i in range(len(df_cuentas)):
    if df_cuentas.loc[i, 'saldo_ars'] < 10000:
        df_cuentas.loc[i, 'categoria'] = 'BAJO'
    else:
        df_cuentas.loc[i, 'categoria'] = 'ALTO'

# CORRECTO Y VECTORIZADO: Usar np.where() o .apply()
df_cuentas['categoria'] = np.where(df_cuentas['saldo_ars'] < 10000, 'BAJO', 'ALTO')
```

---

### 4. Agregaciones (`groupby`) y Uniones (`merge` / `concat`)

#### GroupBy y Agregación Múltiple
```python
resumen_segmento = df_cuentas.groupby('segmento').agg(
    total_clientes=('cliente_id', 'count'),
    saldo_promedio=('saldo_ars', 'mean'),
    saldo_maximo=('saldo_ars', 'max')
).reset_index()
```

#### Uniones con `pd.merge()`
Combina DataFrames utilizando claves comunes (equivalente a los `JOIN`s de SQL):

```python
df_clientes = pd.DataFrame({'cliente_id': [101, 102], 'nombre': ['Carlos', 'Ana']})
df_saldos = pd.DataFrame({'cliente_id': [101, 102], 'saldo': [2500000, 45000]})

# LEFT JOIN en Pandas
df_merged = pd.merge(df_clientes, df_saldos, on='cliente_id', how='left')
```
