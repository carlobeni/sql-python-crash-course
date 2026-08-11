# Test de Preguntas Desafiantes - Día 5: Pandas & NumPy

Evaluación técnica sobre Indexación (`loc` vs `iloc`), Vectorización, Agregaciones y Joins en Pandas.

---

### Pregunta 1: Diferencia Crítica entre `loc` e `iloc`
Dado el siguiente DataFrame `df` cuyos índices enteros **no son secuenciales**:

```python
import pandas as pd

data = {'producto': ['CA', 'CC', 'TC'], 'tasa': [0.0, 0.15, 0.45]}
df = pd.DataFrame(data, index=[10, 20, 30])
```

¿Cuál es el resultado exacto de `df.loc[10:20, 'producto']` en comparación con `df.iloc[0:2, 0]`?

- A) Ambos retornan exactamente el mismo objeto Series con los valores `'CA'` y `'CC'`.
- B) `loc` da error porque `10` y `20` no son índices posicionales válidos; `iloc` funciona.
- C) `df.loc[10:20, 'producto']` busca las etiquetas de índice `10` y `20` (ambas inclusivas) retornando `'CA'` y `'CC'`. `df.iloc[0:2, 0]` accede a las posiciones ordinales 0 y 1 (exclusivo el 2), retornando también `'CA'` y `'CC'`.
- D) `iloc` incluye las filas 0, 1 y 2.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: C**

**Explicación:** `.loc` utiliza etiquetas (labels). Al pasar `10:20`, busca las etiquetas `10` y `20` inclusive. `.iloc` utiliza posiciones numéricas ordinales 0-based. El slice `0:2` toma los elementos en los índices ordinales `0` y `1` (excluyendo el `2`). En este caso específico terminan seleccionando los mismos datos pero por mecanismos completamente distintos.
</details>

---

### Pregunta 2: Filtros Booleanos Condicionales
Analiza la siguiente sentencia que intenta filtrar un DataFrame en Pandas:

```python
# Intento de filtrar clientes con saldo > 10000 y segmento Premium
df_filtrado = df[df['saldo'] > 10000 and df['segmento'] == 'Premium']
```

¿Qué ocurrirá al ejecutar esta instrucción?

- A) Filtra correctamente las filas que cumplen ambas condiciones.
- B) Lanza un `ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all()`.
- C) Convierte las Series a valores booleanos simples `True` o `False`.
- D) Aplica una operación de tipo `OR` en lugar de `AND`.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** En Python base, la palabra reservada `and` evalúa la verdad booleana de todo el objeto en su conjunto. Pandas no puede convertir una `Series` de múltiples valores booleanos a un único valor verdadero/falso. Se deben utilizar los operadores element-wise bitwise (`&` para AND, `|` para OR, `~` para NOT) y **envolver obligatoriamente cada condición entre paréntesis**: `df[(df['saldo'] > 10000) & (df['segmento'] == 'Premium')]`.
</details>

---

### Pregunta 3: Malas Prácticas de Rendimiento (Regla de Oro #4)
Se requiere calcular una columna `saldo_usd` a partir de `saldo_ars` (tipo de cambio 1200) para un DataFrame de 5 millones de registros. ¿Cuál de las opciones representa la mejor práctica en Pandas?

- A) `df['saldo_usd'] = [row['saldo_ars'] / 1200 for index, row in df.iterrows()]`
- B) `df['saldo_usd'] = df['saldo_ars'] / 1200`
- C) Usar un bucle `while` incrementando un contador de filas con `df.iloc[i]`.
- D) `df['saldo_usd'] = df['saldo_ars'].apply(lambda x: x / 1200)`

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** La opción B es una **operación puramente vectorial** ejecutada en C subyacente. La opción A (`iterrows`) es hasta 1000 veces más lenta. La opción D (`apply`) es más rápida que `iterrows` pero sigue siendo un loop en Python a nivel de elementos. La vectorización directa (Opción B) es la regla de oro para rendimiento.
</details>

---

### Pregunta 4: Comportamiento de `pd.merge()` con Nulos
Si realizas un `pd.merge(df_a, df_b, on='cliente_id', how='left')` y la columna `saldo` en `df_b` contenía valores enteros en filas que no tuvieron coincidencia:

¿De qué tipo de dato resulta la columna `saldo` en el DataFrame unificado final `df_merged`?

- A) Se mantiene como `int64` asignando 0 a las filas sin coincidencia.
- B) Se convierte automáticamente a `float64` porque `NaN` es un valor de punto flotante en NumPy/Pandas.
- C) Transforma la columna completa a tipo `string`.
- D) Produce un error de incompatibilidad de tipos.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** En las versiones estándar de Pandas (usando dtypes clásicos de NumPy), el valor `np.nan` es de tipo `float64`. Cuando una columna de enteros recibe valores nulos resultantes de un `LEFT JOIN` sin coincidencia, Pandas debe realizar un "upcasting" automático de `int64` a `float64` para poder representar la ausencia de datos (`NaN`).
</details>
