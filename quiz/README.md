# Conocimiento General en Lenguaje SQL

### P1. ¿Cuál de las siguientes no es una función de agregación?
* [ ] AVG()
* [ ] SUM()
* [x] **HAVING** *(Correcta)*
* [ ] COUNT()
* [ ] Ninguna de las anteriores

> **Explicación:** `AVG()`, `SUM()` y `COUNT()` son funciones de agregación que calculan un único valor resumen a partir de un conjunto de filas. `HAVING` no es una función, sino una cláusula SQL utilizada para filtrar grupos producidos por `GROUP BY`.

---

### P2. ¿Cuál de estas afirmaciones mejora el rendimiento de una consulta?
* [x] **Todas las anteriores son correctas** *(Correcta)*
* [ ] Evitar la condiciones IN ( SELECT...) sustituyéndolas por joins.
* [ ] Las condiciones (tanto de filtro como de join) deben ir siempre en el orden en que esté definido el índice
* [ ] Definir los campos a utilizar en el SELECT en lugar de usar SELECT *

> **Explicación:** Todas son buenas prácticas de optimización: sustituir subconsultas no correlacionadas o pesadas por `JOIN` permite al optimizador estructurar planes eficientes; respetar el orden de las columnas de un índice compuesto aprovecha el índice; y seleccionar solo columnas necesarias reduce el tráfico de I/O y memoria.

---

### P3. Si ejecuto la siguiente consulta, ¿cuál es la respuesta correcta?

```sql
SELECT COUNT(Personas.Nombre)
FROM Personas
WHERE (Personas.FechaNacimiento <= '1990/01/21'
  AND (Personas.Ciudad = 'Asunción' OR Personas.Departamento = 'Central'))
  OR (Personas.Departamento = 'Alto Paraná' AND Personas.EstadoCivil = 'Soltero')
```

**Datos de la tabla `Personas`:**
| Nombre | FechaNacimiento | EstadoCivil | Ciudad | Departamento |
|---|---|---|---|---|
| Rosa Rojas | 1993-05-18 | Soltero | Hernandarias | Alto Paraná |
| Juan Pérez | 1985-07-02 | Soltero | San Lorenzo | Central |
| Luz Díaz | 1970-12-03 | Soltero | Coronel Oviedo | Caaguazú |
| José Mora | 1989-10-25 | Casado | Ciudad del Este | Alto Paraná |
| David Rivas | 1977-03-31 | Casado | Luque | Central |

* [ ] 4
* [ ] 5
* [ ] 2
* [x] **Ninguna de las anteriores** *(Correcta)*

> **Explicación:**  
> Evaluando las condiciones:
> 1. **Rosa Rojas**: Cumple la segunda condición (`Alto Paraná` AND `Soltero`). *(Cuenta: 1)*
> 2. **Juan Pérez**: Nacido en 1985 (<= 1990) y de `Central`. Cumple la primera condición. *(Cuenta: 2)*
> 3. **Luz Díaz**: Nacida en 1970, pero es de Caaguazú (no cumple ni Central/Asunción ni Alto Paraná).
> 4. **José Mora**: Nacido en 1989, pero es de Alto Paraná (no Central/Asunción) y es Casado.
> 5. **David Rivas**: Nacido en 1977 (<= 1990) y de `Central`. Cumple la primera condición. *(Cuenta: 3)*  
> En total cumplen **3 personas**. Como 3 no figura en las opciones (4, 5, 2), la opción correcta es *Ninguna de las anteriores*.

---

### P4. Con respecto a los Constraint, dadas las siguientes definiciones, selecciona el conjunto de palabras asociados a cada una:
* **A:** Es una columna de tabla de base de datos relacional (o combinación de columnas) que identifica de forma única todos los registros de la tabla.
* **B:** Es un tipo de restricción de columna dentro de una tabla, que dicta que todos los valores en esa columna deben ser únicos.
* **C:** Es una columna o grupo de columnas en una tabla de base de datos relacional que proporciona un enlace entre los datos de dos tablas.

* [ ] A - UNIQUE, B - PRIMARY KEY, C - FOREIGN KEY
* [ ] A - FOREIGN KEY, B - PRIMARY KEY, C - UNIQUE
* [x] **A - PRIMARY KEY, B - UNIQUE, C - FOREIGN KEY** *(Correcta)*
* [ ] A - FOREIGN KEY, B - UNIQUE, C - PRIMARY KEY

> **Explicación:** La definición A describe la Clave Primaria (`PRIMARY KEY`), la B describe la restricción de unicidad (`UNIQUE`), y la C describe la Clave Foránea (`FOREIGN KEY`).

---

### P5. ¿Qué calcula la siguiente sentencia?

```sql
SELECT SUM(precio)
FROM producto
WHERE precio = MAX(precio)
```

* [x] **La sentencia es errónea** *(Correcta)*
* [ ] 25.000
* [ ] 50.000
* [ ] Ninguna de las respuestas

> **Explicación:** En SQL estándar no se permite colocar funciones de agregación como `MAX()` directamente dentro de la cláusula `WHERE`. Para filtrar por el máximo se requiere una subconsulta (`WHERE precio = (SELECT MAX(precio) FROM producto)`).

---

### P6. Para eliminar todas las filas de la tabla "productos", me conviene utilizar la sentencia "TRUNCATE TABLE productos"
* [x] **Verdadero** *(Correcta)*
* [ ] Falso

> **Explicación:** `TRUNCATE TABLE` desasigna las páginas de datos completas y genera un registro mínimo en el transaction log (a diferencia de `DELETE` sin `WHERE`, que registra cada fila borrada individualmente), siendo significativamente más rápido y eficiente.

---

### P7. Ambas sentencias retornan el mismo conjunto de resultados
* **Sentencia 1:**
  ```sql
  SELECT Nombre FROM Colaborador WHERE Salario > 2000000 and Salario < 5000000
  ```
* **Sentencia 2:**
  ```sql
  SELECT Nombre FROM Colaborador WHERE Salario BETWEEN 2000000 and 5000000
  ```

* [ ] Verdadero
* [x] **False** *(Correcta)*

> **Explicación:** El operador `BETWEEN val1 AND val2` es **inclusivo** (equivale a `>= 2000000 AND <= 5000000`). Por el contrario, la primera sentencia usa operadores estrictos (`>` y `<`), por lo que excluirá cualquier salario exactamente igual a 2.000.000 o 5.000.000.

---

### P8. Dada la consulta siguiente, selecciona cuál es la respuesta correcta para la unión entre las tablas A y B:

```sql
SELECT *
FROM A JOIN B
ON B.C1 = A.C1
```

* [x] **Combina los registros de la tabla “A” con los de la tabla “B” y se queda únicamente con los registros de los que cumplen la condición B.C1 = A.C1** *(Correcta)*
* [ ] La sentencia no es correcta
* [ ] Combina los registros de la tabla “A” con los de la tabla “B” y se queda con los registros de la tabla “A” que cumplan la condición B.C1 = A.C1 y con todos los registros de la tabla “B”
* [ ] Ninguna de las anteriores

> **Explicación:** La cláusula `JOIN` por defecto es un `INNER JOIN`, el cual devuelve exclusivamente las filas que tienen coincidencia en ambas tablas según el predicado `ON`.

---

## Sección II (Página 3 de 3)

### P9. Puedo utilizar la sentencia "DELETE FROM cliente", para eliminar la tabla de "cliente"
* [x] **Falso** *(Correcta)*
* [ ] Verdadero

> **Explicación:** `DELETE FROM` borra el contenido (las filas/registros), pero preserva la tabla, sus columnas y su estructura en el esquema. Para eliminar la tabla en su totalidad se debe usar `DROP TABLE cliente`.

---

### P10. ¿Cuál de las siguientes afirmaciones es correcta?
* [ ] La sentencia "SELECT COUNT (nombre_columna) FROM tabla" podría retornar la misma cantidad de filas que la sentencia "SELECT COUNT (*) FROM tabla"
* [ ] La sentencia "SELECT COUNT (*) FROM tabla" podría retornar más filas que la sentencia "SELECT COUNT (nombre_columna) FROM tabla"
* [ ] La sentencia "SELECT COUNT (nombre_columna) FROM tabla" podría retornar menos filas que la sentencia "SELECT COUNT (*) FROM tabla"
* [x] **Todas las anteriores son correctas** *(Correcta)*

> **Explicación:** `COUNT(*)` cuenta todas las filas de la tabla incluyendo nulos. `COUNT(columna)` ignora los valores `NULL`. Si la columna no tiene nulos, retornan el mismo valor; si tiene nulos, `COUNT(*)` retornará un valor mayor (o lo que es lo mismo, `COUNT(columna)` retornará menos). Por tanto, todas las afirmaciones son posibles.

---

### P11. Selecciona la opción correcta que muestre todos los colaboradores cuyo primer apellido sea Pérez, y que no vivan en la ciudad de Asunción, ordenados por departamento de la A a la Z.

* [ ] **Opción 1:**
  ```sql
  SELECT nombre, apellido, ciudad, departamento
  FROM colaboradores
  WHERE DISTINCT('Asunción') AND apellido LIKE 'Pérez%'
  ORDER BY departamento ASC
  ```
* [ ] **Opción 2:**
  ```sql
  SELECT nombre, apellido, ciudad, departamento
  FROM colaboradores
  WHERE ciudad < > 'Asunción' AND apellido = 'Pérez'
  ORDER BY departamento DESC
  ```
* [ ] **Opción 3:**
  ```sql
  SELECT nombre, apellido, ciudad, departamento
  FROM colaboradores
  WHERE ciudad != 'Asunción' AND apellido = 'Pérez%'
  ORDER BY departamento DESC
  ```
* [x] **Opción 4:** *(Correcta)*
  ```sql
  SELECT nombre, apellido, ciudad, departamento
  FROM colaboradores
  WHERE ciudad != 'Asunción' AND apellido LIKE 'Pérez%'
  ORDER BY departamento ASC
  ```
* [ ] Ninguna de las anteriores

> **Explicación:**
> * `ciudad != 'Asunción'` filtra correctamente la ciudad.
> * `apellido LIKE 'Pérez%'` permite identificar "primer apellido Pérez" contemplando casos con segundo apellido.
> * `ORDER BY departamento ASC` ordena de la A a la Z (ascendente).

---

### P12. ¿Por qué no es recomendado crear índices en tablas pequeñas?
* [x] **Porque al motor le toma menos tiempo escanear la tabla que atravesar el índice** *(Correcta)*
* [ ] Porque los índices ocupan mucho espacio
* [ ] Porque los índices no se utilizan en tablas pequeñas
* [ ] Todas las anteriores son correctas

> **Explicación:** Para tablas de pocas filas que caben en una o pocas páginas de disco/memoria, un Table Scan secuencial requiere menos lecturas de E/S que navegar por la estructura del árbol B-Tree del índice más el posterior lookup.

---

### P13. ¿Cuál de estas sentencias añade una fila a una tabla en una base de datos?
* [ ] UPDATE
* [x] **INSERT** *(Correcta)*
* [ ] ADDROW
* [ ] INCLUDE

> **Explicación:** `INSERT INTO` es la sentencia DML estándar encargada de insertar nuevas filas en una tabla existente.

---

### P14. Se necesita obtener todas las personas que tenga nulo en el campo ciudad, ¿cuál es la sentencia correcta?
* [ ] **Opción 1:** `SELECT Nombre FROM Personas WHERE Ciudad = NULL`
* [ ] **Opción 2:** `SELECT Nombre FROM Personas WHERE Ciudad = ''`
* [x] **Opción 3:** `SELECT Nombre FROM Personas WHERE Ciudad IS NULL` *(Correcta)*
* [ ] **Opción 4:** `SELECT Nombre FROM Personas WHERE ISNULL(CIUDAD)`

> **Explicación:** En SQL, `NULL` denota la ausencia de valor y no puede compararse mediante operadores convencionales como `=` o `!=` (que devuelven `UNKNOWN`). Para evaluar nulos se debe utilizar `IS NULL` o `IS NOT NULL`.

---

### P15. Si realizo cualquier operación con nulo, ¿cuál será el resultado?
* [ ] Depende de la opearción
* [ ] Dará error
* [ ] Mismo principcio de las operaciones ariméticas
* [x] **Nulo** *(Correcta)*

> **Explicación:** Siguiendo las reglas de la lógica trivalente de SQL, cualquier cálculo aritmético o concatenación estándar que involucre un valor `NULL` produce como resultado `NULL` (ejemplo: `10 + NULL = NULL`).

---

### P16. En términos del Lenguaje SQL en una Base de Datos Relacional, ¿qué representa el Nulo o Null?
* [ ] Es igual al 0 aritmético
* [ ] Es igual al '' (texto vacío)
* [ ] Las dos anteriores
* [x] **Ausencia de valor, es el equivalente al conjuntos vacío de la Teoría General de Conjuntos** *(Correcta)*
* [ ] Es un valor que se utiliza cuando no sabemos que datos cargar en una columna
* [ ] Es un valor que se utiliza cuando no sabemos que datos cargar en una tabla
* [ ] Es equivalente a un espacio vacío
* [ ] Ninguno de las Anteriores

> **Explicación:** `NULL` representa un dato desconocido, no aplicable o inexistente (ausencia de valor). No equivale al valor numérico `0` ni a una cadena de texto vacía `''`.

---

### P17. ¿Qué es una Clave Primaria o Primary Key?
* [ ] La columna más importante
* [ ] La columna principal
* [x] **La columna que representa a una fila de una tabla manera unívoca** *(Correcta)*
* [ ] Ninguna de las anteriores

> **Explicación:** Una clave primaria es una restricción que identifica de manera única e irrepetible cada registro dentro de una tabla, asegurando que no existan duplicados ni valores nulos en su definición.

---

### P18. ¿Cuántas claves primarias puede tener una tabla?
* [ ] Al menos una
* [ ] Según lo que sea necesario
* [x] **Una y solo una** *(Correcta)*
* [ ] Todas las anteriores

> **Explicación:** Una tabla en una base de datos relacional puede tener **únicamente una** restricción `PRIMARY KEY` (aunque esta clave primaria pueda ser compuesta por varias columnas).

---

### P19. ¿Qué tienen en común las siguientes sentencias?

```sql
SELECT * FROM clientes ;
DELETE FROM clientes_historico;
UPDATE clientes_historico_202601; SET estado = 'P' ;
```

*Premisas evaluadas:*
1. Todas son del tipo DML
2. Las tres son peligrosas de ejecutar en un ambiente productivo y de ser necesario, se las debe ejecutar con mucha conciencia en casos muy puntuales
3. Las tres no tienen Cláusula WHERE
4. Las tres realizan su operación sobre diferentes tablas
5. Son sentencias del tipo DDL

*Opciones a seleccionar:*
* [ ] Todas las anteriores
* [ ] 1 y 4 son correctas
* [ ] 1, 2 y 3
* [x] **1, 2, 3 y 4 son correctas** *(Correcta)*

> **Explicación:**
> * Son sentencias DML (Manipulación de Datos), no DDL (Definición de Datos, descartando la premisa 5).
> * Al carecer de cláusula `WHERE`, un `DELETE` o `UPDATE` afectará a la totalidad de las filas y un `SELECT *` puede degradar recursos/memoria en producción.
> * Cada una apunta a una tabla diferente (`clientes`, `clientes_historico`, `clientes_historico_202601`).

