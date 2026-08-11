# Día 2: SQL Avanzado - Joins, Subqueries, Vistas & Tuning

Bienvenido al Día 2 del Plan Intensivo de Preparación Acelerada para Evaluación Técnica (Itaú).

---

## Objetivos del Día
1. Dominar todos los tipos de uniones relacionales: `INNER`, `LEFT`, `RIGHT`, `FULL OUTER` y `CROSS JOIN`.
2. Resolver agregaciones con `GROUP BY`, `HAVING` y funciones integradas de fecha (`DATEDIFF`, `DATEADD`) y conversión (`CAST`, `CONVERT`).
3. Construir Subqueries complejas en cláusulas `WHERE` y `FROM`.
4. Crear y mantener Vistas (`CREATE VIEW`).
5. Comprender los principios fundamentales de SQL Tuning (índices clustered/non-clustered, index scan vs index seek).

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

### 3. Subqueries y Vistas (`CREATE VIEW`)

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

### 4. Nociones Básicas de SQL Tuning

* **Index Scan vs Index Seek:**
  * **Index Seek:** El motor accede directamente a las páginas de datos mediante un árbol B-Tree utilizando un índice adecuado. (Rápido y Óptimo).
  * **Index Scan / Table Scan:** El motor lee todas las filas de la tabla o índice de principio a fin. (Lento y Costoso).
* **Sargability (Search Argumentable):** Evita aplicar funciones sobre columnas filtradas en la cláusula `WHERE`.
  * *Non-Sargable:* `WHERE YEAR(fecha_transaccion) = 2026` (Forza Table Scan).
  * *Sargable:* `WHERE fecha_transaccion >= '2026-01-01' AND fecha_transaccion < '2027-01-01'` (Permite Index Seek).
