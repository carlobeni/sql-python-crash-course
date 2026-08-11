# Test de Preguntas Desafiantes - Día 2: SQL Avanzado

Evaluación práctica orientada a Joins, Subqueries, Vistas y Optimización T-SQL.

---

### Pregunta 1: Trampa de Filtro en LEFT JOIN
Dadas las tablas `Clientes` (1,000 filas) y `Prestamos` (200 clientes tienen préstamos activos). Se ejecuta la siguiente consulta:

```sql
SELECT c.cliente_id, c.nombre, p.monto_prestamo
FROM Clientes c
LEFT JOIN Prestamos p ON c.cliente_id = p.cliente_id
WHERE p.estado_prestamo = 'MOROSO';
```

¿Cuántas filas como máximo retornará esta consulta y de qué tipo de unión se trata en la práctica?

- A) Retornará 1,000 filas; los clientes sin préstamo tendrían `NULL` en `monto_prestamo`.
- B) Retornará únicamente las filas de clientes que posean un préstamo moroso, comportándose equivalente a un `INNER JOIN`.
- C) Retornará 800 filas que corresponden a los clientes sin préstamos morosos.
- D) Se producirá un error de compilación porque no se puede usar `WHERE` tras un `LEFT JOIN`.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** Esta es la **Regla de Oro #2**. Al evaluar `WHERE p.estado_prestamo = 'MOROSO'`, cualquier cliente de la tabla `Clientes` que no coincida con `Prestamos` tendrá `p.estado_prestamo = NULL`. Como la condición `NULL = 'MOROSO'` evalúa a `UNKNOWN` (falso), esas filas son filtradas. El `LEFT JOIN` pierde su cualidad de conservar todas las filas de la tabla izquierda y actúa como un `INNER JOIN`. Para conservar el `LEFT JOIN`, la condición debía ir en el `ON`.
</details>

---

### Pregunta 2: Diferencia entre WHERE y HAVING
Dada la consulta:

```sql
SELECT 
    sucursal_id, 
    COUNT(cuenta_id) AS total_cuentas,
    SUM(saldo) AS total_saldo
FROM Cuentas
WHERE saldo > 1000
GROUP BY sucursal_id
HAVING COUNT(cuenta_id) > 5;
```

¿Cuál es la función exacta del filtro `WHERE saldo > 1000` en comparación con `HAVING COUNT(cuenta_id) > 5`?

- A) `WHERE` filtra los grupos que no alcanzan un saldo promedio de 1000, mientras que `HAVING` elimina filas individuales.
- B) `WHERE` descarta las cuentas individuales con saldo <= 1000 antes de realizar el agrupamiento por sucursal; `HAVING` descarta las sucursales resultantes que tengan 5 o menos cuentas computadas.
- C) Ambos filtros realizan exactamente la misma tarea y podrían intercambiarse libremente.
- D) `HAVING` se ejecuta antes del agrupamiento `GROUP BY` y `WHERE` después.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** La cláusula `WHERE` filtra las filas individuales en el paso 2 de la ejecución lógica (antes del agrupamiento). `HAVING` evalúa la condición sobre los datos agregados por `GROUP BY` en el paso 4. Las cuentas con saldo <= 1000 ni siquiera entran a la cuenta de `COUNT(cuenta_id)`.
</details>

---

### Pregunta 3: Optimización de Consultas (Sargability)
Un desarrollador nota que la siguiente consulta tarda más de 30 segundos en responder sobre una tabla de 10 millones de transacciones con un índice en `fecha_transaccion`:

```sql
SELECT * FROM Transacciones
WHERE DATEDIFF(day, fecha_transaccion, '2026-08-01') = 0;
```

¿Cuál es la forma óptima de reescribir esta consulta para habilitar un **Index Seek** y mejorar el rendimiento?

- A) `WHERE CAST(fecha_transaccion AS DATE) = '2026-08-01'`
- B) `WHERE fecha_transaccion >= '2026-08-01' AND fecha_transaccion < '2026-08-02'`
- C) `WHERE DATEPART(yy, fecha_transaccion) = 2026 AND DATEPART(mm, fecha_transaccion) = 8 AND DATEPART(dd, fecha_transaccion) = 1`
- D) `WHERE CONVERT(VARCHAR, fecha_transaccion, 112) = '20260801'`

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** Para que una consulta sea **Sargable** (Search Argumentable) y el motor SQL pueda usar un **Index Seek**, no se deben aplicar funciones (`DATEDIFF`, `CAST`, `CONVERT`, `DATEPART`) sobre la columna indexada en la cláusula `WHERE`. La opción B deja la columna `fecha_transaccion` limpia en ambos lados del operador relacional.
</details>

---

### Pregunta 4: Funciones de Fecha T-SQL
¿Qué valor retornará la expresión `DATEDIFF(month, '2026-01-31', '2026-02-01')` en SQL Server?

- A) `0` (porque transcurrió solo 1 día entre ambas fechas).
- B) `1` (porque calcula el número de límites de meses cruzados entre las dos fechas).
- C) `31` (número de días en el primer mes).
- D) Lanza un error por diferencia menor a 30 días.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** `DATEDIFF` en T-SQL no calcula meses enteros de 30 días ni tiempo exacto; simplemente cuenta el número de **fronteras del intervalo especificado** (`datepart`) cruzadas. De enero a febrero hay 1 cambio de mes, por lo que devuelve `1`.
</details>
