# Test de Preguntas Desafiantes - Día 1: SQL Core

Prueba tu nivel de conocimientos con estas preguntas diseñadas al estilo de la evaluación técnica de selección.

---

### Pregunta 1: Comparación con Valores Nulos
¿Cuál es el resultado exacto de la siguiente consulta SQL ejecutada sobre una tabla `Transacciones` que posee registros donde la columna `monto` contiene valores `NULL`?

```sql
SELECT COUNT(*) 
FROM Transacciones 
WHERE monto = NULL OR monto <> NULL;
```

- A) Retorna el total absoluto de filas de la tabla.
- B) Retorna únicamente el número de filas donde `monto` es `NULL`.
- C) Retorna 0 (Cero).
- D) Produce un error de sintaxis en el motor T-SQL.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: C**

**Explicación:** En SQL Tri-Valued Logic (`TRUE`, `FALSE`, `UNKNOWN`), cualquier comparación de igualdad (`=`) o desigualdad (`<>`) directa contra `NULL` evalúa a `UNKNOWN`. 
Dado que la cláusula `WHERE` solo incluye filas cuya condición evalúa a `TRUE`, ni `monto = NULL` ni `monto <> NULL` serán verdaderos para ninguna fila. Por ende, la consulta filtrará el 100% de los registros y `COUNT(*)` devolverá `0`. Para obtener todos los registros habría que usar `monto IS NULL OR monto IS NOT NULL`.
</details>

---

### Pregunta 2: Orden Lógico de Ejecución
Considera la siguiente consulta T-SQL que falla al ejecutarse:

```sql
SELECT 
    cliente_id, 
    saldo_cuenta * 1.21 AS saldo_con_iva
FROM Cuentas
WHERE saldo_con_iva > 100000;
```

¿Por qué falla esta consulta y cómo debe solucionarse manteniendo la lógica?

- A) Falla porque `1.21` debe escribirse como `CAST(1.21 AS DECIMAL)`.
- B) Falla porque el alias `saldo_con_iva` no está disponible en la cláusula `WHERE` debido al orden de ejecución lógica.
- C) Falla porque `WHERE` no permite operadores matemáticos de multiplicación.
- D) Falla porque falta la cláusula `GROUP BY cliente_id`.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** El motor SQL evalúa `FROM` -> `WHERE` -> `SELECT`. Cuando el motor procesa la cláusula `WHERE`, el bloque `SELECT` (donde se define el alias `saldo_con_iva`) aún no ha sido ejecutado. La solución correcta es repetir la expresión en el `WHERE`: `WHERE (saldo_cuenta * 1.21) > 100000` o usar una CTE / Subconsulta.
</details>

---

### Pregunta 3: Filtro de Rango Inclusive con `BETWEEN`
Dada la siguiente sentencia:

```sql
SELECT * FROM Movimientos
WHERE fecha_transaccion BETWEEN '2026-08-01' AND '2026-08-10';
```

Si la columna `fecha_transaccion` es de tipo `DATETIME` e incluye horas (ej. `'2026-08-10 14:30:00'`), ¿cuál de los siguientes registros **NO** será seleccionado?

- A) `'2026-08-01 00:00:00'`
- B) `'2026-08-05 23:59:59'`
- C) `'2026-08-10 00:00:00'`
- D) `'2026-08-10 18:45:00'`

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: D**

**Explicación:** La constante de texto `'2026-08-10'` se convierte implícitamente a `DATETIME` como `'2026-08-10 00:00:00'`. Dado que `BETWEEN` es inclusivo (`>= min AND <= max`), la fecha `'2026-08-10 18:45:00'` es estrictamente mayor que `'2026-08-10 00:00:00'`, por lo que **queda excluida**. Para incluir todo el día 10 de agosto, se debe usar `>= '2026-08-01' AND < '2026-08-11'`.
</details>

---

### Pregunta 4: Restricciones de Integridad
¿Qué sucede al ejecutar una instrucción `DELETE FROM Sucursales WHERE sucursal_id = 5;` si existe una tabla `Clientes` con una clave foránea `FK_Clientes_Sucursales` definida sin `ON DELETE CASCADE` y actualmente existen 10 clientes asignados a esa sucursal?

- A) Los 10 clientes en `Clientes` son borrados automáticamente.
- B) La columna `sucursal_id` en `Clientes` pasa a valer `NULL` automáticamente.
- C) Se lanza un error de violación de integridad referencial y la operación se cancela por completo (rollback).
- D) La sucursal se elimina pero los clientes conservan su valor `sucursal_id = 5` en estado huérfano.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: C**

**Explicación:** La Foreign Key sin acción en cascada (`RESTRICT` o `NO ACTION` por defecto) prohíbe la eliminación de un registro padre mientras tenga registros hijos asociados. La transacción aborta lanzando una excepción de integridad referencial.
</details>
