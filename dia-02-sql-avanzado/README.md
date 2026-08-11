# Día 2: SQL Avanzado - Joins, Subqueries, Vistas & Tuning

Bienvenido al Día 2 del Plan Intensivo de Preparación Acelerada para Evaluación Técnica (Itaú).

---

## Objetivos del Día
1. Dominar todos los tipos de uniones relacionales: `INNER`, `LEFT`, `RIGHT`, `FULL OUTER` y `CROSS JOIN`.
2. Resolver agregaciones con `GROUP BY`, `HAVING` y funciones integradas de fecha (`DATEDIFF`, `DATEADD`) y conversión (`CAST`, `CONVERT`).
3. Construir **Funciones de Ventana (Window Functions)**: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()` y sumas acumuladas (`OVER (PARTITION BY ... ORDER BY ...)`).
4. Escribir **Common Table Expressions (CTEs - `WITH ... AS`)** y utilizar **Tablas Temporales (`#temp`)**.
5. Construir Subqueries complejas y Vistas (`CREATE VIEW`).
6. Comprender los principios fundamentales de SQL Tuning (índices clustered/non-clustered, index scan vs index seek, sargability).

---

## Teoría Explicada

### 1. Uniones de Tablas (Joins)

* **`INNER JOIN`**: Retorna solo los registros que coinciden en ambas tablas.
* **`LEFT JOIN` (LEFT OUTER JOIN)**: Retorna todos los registros de la tabla izquierda y las coincidencias de la derecha. Si no hay coincidencia, llena con `NULL`.
* **`RIGHT JOIN`**: Retorna todos los registros de la tabla derecha y coincidencias de la izquierda.
* **`FULL OUTER JOIN`**: Retorna todos los registros cuando hay coincidencia en la izquierda O en la derecha.
* **`CROSS JOIN`**: Producto cartesiano (combina cada fila de la primera tabla con cada fila de la segunda).

```sql
-- Ejemplo de LEFT JOIN para identificar clientes sin cuenta bancaria activa
SELECT 
    c.cliente_id, 
    c.nombre_completo,
    b.cuenta_id
FROM Clientes c
LEFT JOIN Cuentas b ON c.cliente_id = b.cliente_id
WHERE b.cuenta_id IS NULL; -- Filtro de anti-join
```

---

### Regla de Oro Itaú #2: La Trampa de Filtros en `LEFT JOIN`

> **Importante para la Evaluación:**
> Poner un filtro sobre una columna de la tabla derecha dentro de la cláusula `WHERE` convierte automáticamente el `LEFT JOIN` en un `INNER JOIN`, debido a que la condición descarta las filas donde esa columna es `NULL`.
> 
> Para mantener el `LEFT JOIN` intacto, debes colocar el filtro de la tabla derecha **dentro de la cláusula `ON`** de la unión.

```sql
-- INCORRECTO: Se comporta como INNER JOIN (descarta clientes sin tarjetas o con tarjeta cancelada)
SELECT c.cliente_id, c.nombre, t.numero_tarjeta
FROM Clientes c
LEFT JOIN Tarjetas t ON c.cliente_id = t.cliente_id
WHERE t.estado = 'ACTIVA'; -- t.estado es NULL para clientes sin tarjeta, por lo que WHERE lo elimina.

-- CORRECTO: Mantiene el LEFT JOIN (retorna TODOS los clientes, tengan o no tarjeta activa)
SELECT c.cliente_id, c.nombre, t.numero_tarjeta
FROM Clientes c
LEFT JOIN Tarjetas t ON c.cliente_id = t.cliente_id AND t.estado = 'ACTIVA';
```

---

### 2. Agregaciones y Funciones Integradas

#### Cláusulas `GROUP BY` y `HAVING`
* `WHERE`: Filtra filas individuales antes de agrupar.
* `HAVING`: Filtra grupos después de la agregación. Opera con funciones como `SUM()`, `AVG()`, `COUNT()`, `MAX()`, `MIN()`.

#### Funciones de Fecha en T-SQL
* `DATEDIFF(datepart, startdate, enddate)`: Diferencia entre dos fechas.
  * Ejemplo: `DATEDIFF(day, '2026-08-01', '2026-08-11')` -> Retorna `10`.
  * Ejemplo: `DATEDIFF(month, fecha_alta, GETDATE())`
* `DATEADD(datepart, number, date)`: Suma un intervalo a una fecha.
  * Ejemplo: `DATEADD(month, -3, GETDATE())` -> Retorna la fecha de hace 3 meses.

#### Funciones de Conversión de Tipos
* `CAST(expresion AS tipo_dato)`: Sintaxis ANSI Estándar. `CAST('2026-08-11' AS DATE)`.
* `CONVERT(tipo_dato, expresion, [estilo])`: Específico de T-SQL. Permite formatear fechas con códigos de estilo (ej. `103` para `dd/mm/yyyy`).

```sql
-- Agregación con funciones de fecha y HAVING
SELECT 
    c.segmento,
    COUNT(DISTINCT c.cliente_id) AS total_clientes,
    AVG(b.saldo_actual) AS saldo_promedio,
    CONVERT(VARCHAR(10), MAX(c.fecha_alta), 103) AS ultima_alta_formateada
FROM Clientes c
INNER JOIN Cuentas b ON c.cliente_id = b.cliente_id
WHERE c.fecha_alta >= DATEADD(year, -2, GETDATE())
GROUP BY c.segmento
HAVING AVG(b.saldo_actual) > 500000;
```

---

### 3. Funciones de Ventana (Window Functions)

A diferencia de `GROUP BY` (que colapsa múltiples filas en una sola), las **Funciones de Ventana** realizan cálculos sobre un conjunto de filas relacionadas sin colapsar el resultado, manteniendo cada fila individual intacta.

#### Sintaxis General:
`FUNCION() OVER (PARTITION BY columna_grupo ORDER BY columna_orden)`

* **`PARTITION BY`**: Divide el dataset en ventanas / particiones lógicas (opcional).
* **`ORDER BY`**: Define el orden dentro de cada partición (obligatorio para ranking y desplazamiento).

#### A. Funciones de Ranking: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`
* `ROW_NUMBER()`: Asigna un número secuencial único (1, 2, 3, 4) sin empates.
* `RANK()`: Asigna el mismo número a valores idénticos, pero **salta** posiciones en caso de empate (1, 2, 2, 4).
* `DENSE_RANK()`: Asigna el mismo número a valores idénticos **sin saltar** posiciones (1, 2, 2, 3).

```sql
-- Obtener la última transacción por cliente usando ROW_NUMBER()
WITH TransaccionesNumeradas AS (
    SELECT 
        transaccion_id,
        cliente_id,
        monto,
        fecha_transaccion,
        ROW_NUMBER() OVER (
            PARTITION BY cliente_id 
            ORDER BY fecha_transaccion DESC
        ) AS rn
    FROM Transacciones
)
SELECT transaccion_id, cliente_id, monto, fecha_transaccion
FROM TransaccionesNumeradas
WHERE rn = 1; -- Solo la transacción más reciente por cliente
```

#### B. Funciones de Desplazamiento: `LAG()` y `LEAD()`
* `LAG(columna, offset, default)`: Accede al valor de una fila **anterior** dentro de la ventana. Excelente para calcular variaciones entre transacciones consecutivas.
* `LEAD(columna, offset, default)`: Accede al valor de una fila **posterior**.

```sql
-- Calcular la variación de saldo respecto a la transacción anterior
SELECT 
    cliente_id,
    fecha_transaccion,
    monto AS monto_actual,
    LAG(monto, 1, 0) OVER (
        PARTITION BY cliente_id 
        ORDER BY fecha_transaccion ASC
    ) AS monto_anterior,
    monto - LAG(monto, 1, 0) OVER (
        PARTITION BY cliente_id 
        ORDER BY fecha_transaccion ASC
    ) AS diferencia_monto
FROM Transacciones;
```

#### C. Agregaciones Acumuladas (Running Totals)
```sql
-- Saldo acumulado (Running Total) por cliente a lo largo del tiempo
SELECT 
    cliente_id,
    fecha_transaccion,
    monto,
    SUM(monto) OVER (
        PARTITION BY cliente_id 
        ORDER BY fecha_transaccion ASC
    ) AS saldo_acumulado
FROM Transacciones;
```

---

### 4. Common Table Expressions (CTEs) y Tablas Temporales

#### A. CTEs (`WITH ... AS`)
Una **CTE** es un conjunto de resultados temporal nombrado que existe únicamente durante la ejecución de una única sentencia (`SELECT`, `INSERT`, `UPDATE` o `DELETE`). Es superior a las subconsultas en la cláusula `FROM` porque mejora significativamente la legibilidad y permite referencias múltiples o recursividad.

```sql
-- Estructura de CTE múltiple
WITH ResumenSaldos AS (
    SELECT 
        cliente_id,
        SUM(saldo_actual) AS total_saldo
    FROM Cuentas
    GROUP BY cliente_id
),
ClientesVIP AS (
    SELECT cliente_id, nombre_completo, segmento
    FROM Clientes
    WHERE segmento = 'Premium'
)
SELECT 
    v.cliente_id,
    v.nombre_completo,
    COALESCE(s.total_saldo, 0) AS saldo_total
FROM ClientesVIP v
LEFT JOIN ResumenSaldos s ON v.cliente_id = s.cliente_id
WHERE COALESCE(s.total_saldo, 0) > 1000000;
```

#### B. Tablas Temporales (`#temp`)
Las tablas temporales físicas se almacenan en la base de datos de sistema `tempdb` y persisten durante toda la sesión del usuario. Permiten crear índices para optimizar procesamientos pesados de múltiples pasos:

```sql
-- Crear e insertar en tabla temporal de sesión (#)
CREATE TABLE #ResumenRiesgo (
    cliente_id INT PRIMARY KEY,
    score_crediticio INT,
    total_deuda DECIMAL(18, 2)
);

INSERT INTO #ResumenRiesgo (cliente_id, score_crediticio, total_deuda)
SELECT c.cliente_id, c.score_crediticio, SUM(p.monto_pendiente)
FROM Clientes c
INNER JOIN Prestamos p ON c.cliente_id = p.cliente_id
GROUP BY c.cliente_id, c.score_crediticio;

-- Consultar la tabla temporal
SELECT * FROM #ResumenRiesgo WHERE total_deuda > 500000;

-- Eliminar explícitamente la tabla al finalizar
DROP TABLE #ResumenRiesgo;
```

---

### 5. Subqueries y Vistas (`CREATE VIEW`)

* **Subquery escalar:** Retorna un único valor de una fila/columna. Se puede usar en `SELECT` o `WHERE`.
* **Subquery correlacionada:** La subconsulta referencia columnas de la consulta externa y se evalúa por cada fila de esta.
* **Subquery en `FROM` (Derived Table):** Funciona como una tabla temporal en memoria. Debe llevar alias obligatorio.
* **Vistas (`CREATE VIEW`):** Consultas SQL guardadas en la base de datos como un objeto virtual. No almacenan datos físicamente (salvo vistas indexadas).

```sql
-- Ejemplo de Subquery en WHERE y creación de Vista
CREATE VIEW vw_resumen_clientes_riesgo AS
SELECT 
    cliente_id,
    nombre_completo,
    saldo_total
FROM (
    SELECT 
        c.cliente_id,
        c.nombre_completo,
        SUM(b.saldo_actual) AS saldo_total
    FROM Clientes c
    INNER JOIN Cuentas b ON c.cliente_id = b.cliente_id
    GROUP BY c.cliente_id, c.nombre_completo
) AS Resumen
WHERE saldo_total < (SELECT AVG(saldo_actual) FROM Cuentas);
```

---

### 6. Nociones Básicas de SQL Tuning

* **Index Scan vs Index Seek:**
  * **Index Seek:** El motor accede directamente a las páginas de datos mediante un árbol B-Tree utilizando un índice adecuado. (Rápido y Óptimo).
  * **Index Scan / Table Scan:** El motor lee todas las filas de la tabla o índice de principio a fin. (Lento y Costoso).
* **Sargability (Search Argumentable):** Evita aplicar funciones sobre columnas filtradas en la cláusula `WHERE`.
  * *Non-Sargable:* `WHERE YEAR(fecha_transaccion) = 2026` (Forza Table Scan).
  * *Sargable:* `WHERE fecha_transaccion >= '2026-01-01' AND fecha_transaccion < '2027-01-01'` (Permite Index Seek).

