# Simulacro de Examen Integrado - Día 7

Examen de Práctica Intensiva (20 Preguntas Desafiantes: 10 de SQL y 10 de Python / Pandas / Data Prep).

---

## Módulo 1: SQL & T-SQL (Preguntas 1 a 10)

### Pregunta 1 (SQL)
¿Qué ocurre al ejecutar `SELECT COUNT(*) FROM Clientes WHERE email <> NULL;`?
- A) Retorna la cantidad de clientes que poseen un email registrado (no nulo).
- B) Retorna la cantidad de clientes sin email (nulo).
- C) Retorna `0`.
- D) Lanza un error de sintaxis.
<details><summary><b>Respuesta</b></summary><b>C</b>. Las comparaciones directas con `NULL` evalúan a `UNKNOWN`, por lo que el `WHERE` descarta el 100% de las filas.</details>

---

### Pregunta 2 (SQL)
¿En qué lugar debe colocarse una condición de filtrado sobre la tabla secundaria en un `LEFT JOIN` para evitar eliminar registros de la tabla principal que no coincidan?
- A) En la cláusula `WHERE`.
- B) En la cláusula `HAVING`.
- C) En la cláusula `ON` del `LEFT JOIN`.
- D) En la cláusula `GROUP BY`.
<details><summary><b>Respuesta</b></summary><b>C</b>. Ubicar la condición en la cláusula `ON` preserva el universo completo de la tabla izquierda (Regla de Oro #2).</details>

---

### Pregunta 3 (SQL)
¿Cuál es el orden de ejecución lógica interno en una consulta SQL?
- A) `SELECT` -> `FROM` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `ORDER BY`
- B) `FROM` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT` -> `ORDER BY`
- C) `FROM` -> `SELECT` -> `WHERE` -> `ORDER BY` -> `GROUP BY`
- D) `WHERE` -> `FROM` -> `GROUP BY` -> `HAVING` -> `SELECT`
<details><summary><b>Respuesta</b></summary><b>B</b>. `FROM` determina el origen, luego se aplica `WHERE`, `GROUP BY`, `HAVING`, `SELECT` y finalmente `ORDER BY`.</details>

---

### Pregunta 4 (SQL)
Dada la tabla `Cuentas(cuenta_id, cliente_id, saldo)`. ¿Cuál de las siguientes consultas falla por sintaxis?
- A) `SELECT cliente_id, SUM(saldo) FROM Cuentas GROUP BY cliente_id HAVING SUM(saldo) > 50000;`
- B) `SELECT cliente_id, SUM(saldo) AS total FROM Cuentas WHERE total > 50000 GROUP BY cliente_id;`
- C) `SELECT cliente_id, AVG(saldo) FROM Cuentas WHERE saldo > 1000 GROUP BY cliente_id;`
- D) `SELECT cliente_id FROM Cuentas GROUP BY cliente_id;`
<details><summary><b>Respuesta</b></summary><b>B</b>. El alias `total` definido en `SELECT` no existe aún cuando el motor ejecuta `WHERE`.</details>

---

### Pregunta 5 (SQL)
¿Qué función se utiliza para evitar que una suma retorne `NULL` cuando una de las columnas sumadas contiene nulos?
- A) `ISNULL()` o `COALESCE()`
- B) `NULLIF()`
- C) `CONVERT()`
- D) `CAST()`
<details><summary><b>Respuesta</b></summary><b>A</b>. `COALESCE(col, 0)` o `ISNULL(col, 0)` reemplazan el nulo por 0 antes de realizar la suma.</details>

---

### Pregunta 6 (SQL)
¿Qué diferencia existe entre `DELETE FROM Tabla` y `TRUNCATE TABLE Tabla`?
- A) `DELETE` borra el esquema y `TRUNCATE` no.
- B) `TRUNCATE` elimina todos los registros de forma más rápida sin registrar cada borrado fila por fila en el log de transacciones y reinicia identificadores autoincrementales.
- C) `TRUNCATE` acepta cláusula `WHERE` y `DELETE` no.
- D) Son exactamente idénticas.
<details><summary><b>Respuesta</b></summary><b>B</b>. `TRUNCATE` es una operación DDL rápida que resetea la tabla y no acepta `WHERE`.</details>

---

### Pregunta 7 (SQL)
Para calcular los meses transcurridos entre la `fecha_alta` de un cliente y la fecha actual en T-SQL, ¿cuál es la sintaxis correcta?
- A) `MONTH(GETDATE() - fecha_alta)`
- B) `DATEDIFF(month, fecha_alta, GETDATE())`
- C) `DATEADD(month, fecha_alta, GETDATE())`
- D) `CAST(fecha_alta AS MONTH)`
<details><summary><b>Respuesta</b></summary><b>B</b>. `DATEDIFF(intervalo, fecha_inicio, fecha_fin)` calcula la diferencia de unidades.</details>

---

### Pregunta 8 (SQL)
¿Por qué `WHERE YEAR(fecha_transaccion) = 2026` puede causar lentitud extrema en una tabla con 10 millones de filas?
- A) Porque el año 2026 no está indexado.
- B) Porque aplicar una función sobre la columna indexada en `WHERE` destruye la propiedad de **Sargability** e impide usar un **Index Seek**, forzando un **Index Scan / Table Scan**.
- C) Porque `YEAR()` solo funciona con cadenas de texto.
- D) Porque T-SQL requiere escribir `YEAR` en minúsculas.
<details><summary><b>Respuesta</b></summary><b>B</b>. Aplicar funciones sobre columnas filtradas rompe la Sargabilidad.</details>

---

### Pregunta 9 (SQL)
¿Qué tipo de unión genera un producto cartesiano entre dos tablas?
- A) `INNER JOIN`
- B) `FULL OUTER JOIN`
- C) `CROSS JOIN`
- D) `LEFT JOIN`
<details><summary><b>Respuesta</b></summary><b>C</b>. `CROSS JOIN` combina cada fila de la primera tabla con cada fila de la segunda.</details>

---

### Pregunta 10 (SQL)
¿Qué cláusula permite filtrar los resultados de una agregación (`GROUP BY`)?
- A) `WHERE`
- B) `HAVING`
- C) `ORDER BY`
- D) `OVER`
<details><summary><b>Respuesta</b></summary><b>B</b>. `HAVING` es el filtro que actúa sobre grupos agregados.</details>

---

## Módulo 2: Python, Pandas & Data Prep (Preguntas 11 a 20)

### Pregunta 11 (Python)
¿Cuál es la salida de `[x if x > 0 else 0 for x in [-2, 5, -1, 3]]`?
- A) `[5, 3]`
- B) `[0, 5, 0, 3]`
- C) `Error de Sintaxis`
- D) `[-2, 5, -1, 3]`
<details><summary><b>Respuesta</b></summary><b>B</b>. Es una expresión ternaria `if-else` en List Comprehension ejecutada para cada elemento.</details>

---

### Pregunta 12 (Python)
¿Cuál es el tiempo medio de complejidad algorítmica para verificar `x in conjunto` en un `set` de Python?
- A) $O(N)$
- B) $O(N^2)$
- C) $O(1)$
- D) $O(\log N)$
<details><summary><b>Respuesta</b></summary><b>C</b>. Los conjuntos en Python están implementados sobre Tablas Hash, logrando búsqueda en $O(1)$.</details>

---

### Pregunta 13 (Python)
¿Qué retorna `math.isnan(float('nan'))`?
- A) `False`
- B) `True`
- C) `None`
- D) Lanza una excepción `ValueError`
<details><summary><b>Respuesta</b></summary><b>B</b>. Retorna `True`, siendo la forma correcta de validar valores `NaN` en Python base.</details>

---

### Pregunta 14 (Pandas)
¿Qué ocurre si intentas filtrar un DataFrame con `df[df['saldo'] > 0 and df['mora'] == False]`?
- A) Filtra correctamente.
- B) Lanza `ValueError: The truth value of a Series is ambiguous`.
- C) Retorna un DataFrame vacío.
- D) Invierte el filtro.
<details><summary><b>Respuesta</b></summary><b>B</b>. Debe usarse `df[(df['saldo'] > 0) & (~df['mora'])]` con el operador bitwise `&` y paréntesis.</details>

---

### Pregunta 15 (Pandas)
¿Cuál es la diferencia principal entre `.loc` y `.iloc`?
- A) `.loc` usa posiciones enteras y `.iloc` usa nombres.
- B) `.loc` usa etiquetas/nombres de índice y `.iloc` usa posiciones enteras 0-indexed.
- C) No hay diferencia, son alias.
- D) `.loc` solo funciona con columnas numéricas.
<details><summary><b>Respuesta</b></summary><b>B</b>. `.loc` es por etiqueta; `.iloc` es por posición ordinal.</details>

---

### Pregunta 16 (Pandas)
¿Por qué se considera mala práctica utilizar `for index, row in df.iterrows():` en Pandas?
- A) Porque modifica los tipos de datos de las columnas a string.
- B) Porque es sumamente ineficiente y lento comparado con las operaciones vectorizadas de Pandas/NumPy.
- C) Porque causa un error de memoria en DataFrames de más de 100 filas.
- D) Porque no soporta números negativos.
<details><summary><b>Respuesta</b></summary><b>B</b>. Es una mala práctica (Regla de Oro #4). Recorrer fila por fila desacelera la ejecución exponencialmente.</details>

---

### Pregunta 17 (Data Prep)
¿Qué función de Pandas debes usar si quieres dividir una columna continua en 5 intervalos que contengan **exactamente la misma cantidad de observaciones** cada uno?
- A) `pd.cut(df['col'], bins=5)`
- B) `pd.qcut(df['col'], q=5)`
- C) `pd.get_dummies(df['col'])`
- D) `df['col'].quantile(5)`
<details><summary><b>Respuesta</b></summary><b>B</b>. `pd.qcut` realiza binning por cuantiles igualitarios.</details>

---

### Pregunta 18 (Data Prep)
En el método del IQR para detección de outliers, si $Q1 = 100$ y $Q3 = 300$, ¿cuál es el límite superior para considerar un dato como outlier?
- A) $400$
- B) $500$
- C) $600$
- D) $700$
<details><summary><b>Respuesta</b></summary><b>C</b>. $IQR = 300 - 100 = 200$. Límite superior $= Q3 + 1.5 \times IQR = 300 + 1.5(200) = 300 + 300 = 600$.</details>

---

### Pregunta 19 (Data Prep)
¿Qué método de imputación de nulos es más recomendable para una columna de ingresos monetarios con presencia de valores extremos (outliers)?
- A) Imputación con la Media.
- B) Imputación con la Mediana.
- C) Imputación con 0 en el 100% de los casos.
- D) Imputación con el valor máximo.
<details><summary><b>Respuesta</b></summary><b>B</b>. La mediana es insensible a valores atípicos (robusta) en distribuciones asimétricas.</details>

---

### Pregunta 20 (ML / Data Prep)
¿Qué es el **Data Leakage** al escalar datos con `StandardScaler`?
- A) La pérdida de datos durante la conversión a CSV.
- B) La filtración de información del conjunto de evaluación/test dentro del ajuste (`fit`) del transformador durante el entrenamiento.
- C) La eliminación accidental de filas sin aviso.
- D) La presencia de valores duplicados en el conjunto de datos.
<details><summary><b>Respuesta</b></summary><b>B</b>. Ajustar transformadores sobre todo el dataset antes del split contamina el modelo con información futura.</details>
