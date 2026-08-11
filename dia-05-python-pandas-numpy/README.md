# Día 5: Python Data - Análisis de Datos con Pandas & NumPy

Bienvenido al Día 5 del Plan Intensivo de Preparación Acelerada para Evaluación Técnica (Itaú).

---

## Objetivos del Día
1. Comprender la estructura de arrays n-dimensionales en **NumPy** y la importancia de las operaciones vectorizadas frente a bucles `for`.
2. Dominar las estructuras principales de **Pandas**: `Series` y `DataFrames`.
3. Dominar la indexación explícita e implícita (`loc` vs `iloc`) y filtros booleanos condicionales.
4. Realizar agregaciones complejas con `groupby()` y uniones de estructuras con `merge()` y `concat()`.
5. Dominar la manipulación vectorial de **Fechas (`.dt`)** y **Cadenas de Texto (`.str`)**.

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

---

### 5. Manipulación Vectorial de Cadenas (`.str`) y Fechas (`.dt`)

#### A. Accesor de Cadenas (`.str`)
Permite aplicar métodos de strings a toda una columna de Pandas de forma vectorizada:

```python
df_transacciones = pd.DataFrame({
    'cliente': ['  juan perez ', 'MARIA GOMEZ', 'carlos benitez '],
    'fecha_raw': ['2026-08-01', '2026-08-05', '2026-08-10']
})

# Limpieza de espacios y formateo a mayúsculas
df_transacciones['cliente_limpio'] = df_transacciones['cliente'].str.strip().str.upper()

# Filtrar clientes cuyo nombre contiene 'GOMEZ'
df_gomez = df_transacciones[df_transacciones['cliente_limpio'].str.contains('GOMEZ', na=False)]
```

#### B. Accesor de Fechas (`.dt`)
Para manipular fechas, primero se convierte la columna con `pd.to_datetime()` y luego se utilizan sus propiedades:

```python
# Convertir columna a datetime
df_transacciones['fecha'] = pd.to_datetime(df_transacciones['fecha_raw'])

# Extraer componentes de fecha
df_transacciones['anio'] = df_transacciones['fecha'].dt.year
df_transacciones['mes'] = df_transacciones['fecha'].dt.month
df_transacciones['dia_nombre'] = df_transacciones['fecha'].dt.day_name()

# Formatear fecha a string personalizado
df_transacciones['fecha_formateada'] = df_transacciones['fecha'].dt.strftime('%d/%m/%Y')
```

