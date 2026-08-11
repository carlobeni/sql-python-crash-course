# Día 1: SQL Core - Bases de Datos & T-SQL Fundamentos

Bienvenido al Día 1 del Plan Intensivo de Preparación Acelerada para Evaluación Técnica en Python, SQL & Data Preparation (Itaú).

---

## Objetivos del Día
1. Repasar conceptos de modelado relacional (Diagramas E/R, Primary Key vs Foreign Key, Restricciones).
2. Dominar sentencias DDL (`CREATE`, `ALTER`, `DROP`) y DML (`INSERT`, `UPDATE`, `DELETE`).
3. Dominar operadores de filtrado de alta frecuencia (`IN`, `BETWEEN`, `IS NULL`, operadores lógicos y de comparación).
4. Comprender la prioridad y orden de ejecución lógica de las cláusulas SQL.
5. Cargar archivos `.csv` en tablas SQL y visualizar la información consolidada.

---

## Teoría Explicada

### 1. Modelado Relacional e Integridad de Datos

* **Diagrama Entidad-Relación (E/R):** Representación gráfica de la estructura lógica de la base de datos (entidades, atributos y relaciones).
* **Primary Key (PK - Clave Primaria):** Identificador único para cada registro en una tabla. No permite valores `NULL` ni duplicados.
* **Foreign Key (FK - Clave Foránea):** Campo que vincula un registro de una tabla con la clave primaria de otra tabla, garantizando la integridad referencial.
* **Restricciones (Constraints):**
  * `NOT NULL`: Garantiza que una columna no almacene valores nulos.
  * `UNIQUE`: Garantiza que todos los valores en una columna sean distintos.
  * `CHECK`: Evalúa una condición lógica antes de permitir insertar/actualizar un registro (ej. `edad >= 18`).
  * `DEFAULT`: Asigna un valor predeterminado si no se especifica uno.

```sql
-- Ejemplo de creación de tabla con restricciones de integridad
CREATE TABLE Clientes (
    cliente_id INT PRIMARY KEY IDENTITY(1,1),
    documento VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    saldo_cuenta DECIMAL(15,2) DEFAULT 0.00,
    CONSTRAINT CHK_saldo_positivo CHECK (saldo_cuenta >= 0)
);
```

---

### 2. Lenguaje SQL: DDL vs DML

* **DDL (Data Definition Language):** Modifica la estructura del esquema de la base de datos.
  * `CREATE`: Crea tablas, vistas, índices.
  * `ALTER`: Modifica columnas o restricciones existentes.
  * `DROP`: Elimina objetos permanentemente de la base de datos.
  * `TRUNCATE`: Elimina todos los registros de una tabla sin registrar borrados fila por fila (más rápido que `DELETE`).

```sql
-- Agregar una columna y una Foreign Key mediante ALTER TABLE
ALTER TABLE Clientes ADD ejecutivo_id INT NULL;

ALTER TABLE Clientes 
ADD CONSTRAINT FK_Clientes_Ejecutivos 
FOREIGN KEY (ejecutivo_id) REFERENCES Ejecutivos(ejecutivo_id);
```

* **DML (Data Manipulation Language):** Manipula los datos contenidos en las tablas.
  * `INSERT`: Inserta nuevos registros.
  * `UPDATE`: Actualiza registros existentes según una condición.
  * `DELETE`: Borra registros según una condición.

```sql
-- Insertar datos
INSERT INTO Clientes (documento, nombre, fecha_nacimiento, saldo_cuenta)
VALUES ('35999888', 'Carlos Benítez', '1992-05-15', 150000.50);

-- Actualizar con filtro
UPDATE Clientes
SET saldo_cuenta = saldo_cuenta * 1.05
WHERE saldo_cuenta < 50000;

-- Borrar datos condicionalmente
DELETE FROM Clientes
WHERE fecha_nacimiento < '1950-01-01';
```

---

### 3. Operadores y Filtros de Alta Frecuencia

| Operador | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `IN` | Evalúa si un valor coincide con cualquier elemento de una lista o subconsulta. | `WHERE tipo_cuenta IN ('CAHS', 'CC', 'INV')` |
| `BETWEEN` | Filtra en un rango inclusivo (`valor >= min AND valor <= max`). | `WHERE saldo BETWEEN 10000 AND 50000` |
| `IS NULL` / `IS NOT NULL` | Evalúa si una columna contiene un valor nulo (`NULL`). | `WHERE ejecutivo_id IS NULL` |
| `LIKE` | Búsqueda por patrones de texto (`%` comodín multicarácter, `_` carácter único). | `WHERE nombre LIKE 'CARLOS%'` |
| `AND` / `OR` / `NOT` | Operadores lógicos. `AND` tiene mayor precedencia que `OR`. | `WHERE (edad > 18 AND saldo > 0) OR es_vip = 1` |

---

### 4. Orden de Ejecución Lógica en SQL

Aunque la consulta se escribe en un orden específico, el motor de SQL la ejecuta internamente en el siguiente orden:

1. **`FROM` / `JOIN`**: Determina y une las tablas origen.
2. **`WHERE`**: Filtra las filas antes de agrupar.
3. **`GROUP BY`**: Agrupa las filas restantes por columnas clave.
4. **`HAVING`**: Filtra los grupos resultantes (opera sobre funciones de agregación).
5. **`SELECT`**: Evalúa expresiones y selecciona columnas.
6. **`DISTINCT`**: Elimina filas duplicadas del resultado.
7. **`ORDER BY`**: Ordena el conjunto de datos final.
8. **`TOP` / `LIMIT` / `OFFSET`**: Restringe la cantidad de filas retornadas.

> **Nota de Evaluación:** No se puede usar un alias definido en la cláusula `SELECT` dentro de la cláusula `WHERE`, dado que `WHERE` se ejecuta antes que `SELECT`.

---

### 5. Carga de Archivos CSV y Visualización de Información

En entornos reales de Data Preparation e ingesta de datos bancarios, es necesario importar archivos planos (`.csv` o `.txt`) a tablas relacionales SQL.

#### A. Método T-SQL Nativo en SQL Server: `BULK INSERT`

Para cargar un archivo CSV directamente en una tabla existente en SQL Server:

```sql
-- 1. Crear la tabla receptora con la estructura equivalente al CSV
CREATE TABLE clientes_importados (
    cliente_id INT,
    num_documento VARCHAR(20),
    nombre_completo VARCHAR(120),
    segmento VARCHAR(30),
    fecha_alta DATE,
    saldo_cuenta DECIMAL(18, 2)
);

-- 2. Ejecutar la ingesta masiva con BULK INSERT
BULK INSERT clientes_importados
FROM 'D:\TestSQLPython\dia-01-sql-core\datos_clientes.csv'
WITH (
    FIRSTROW = 2,               -- Omitir la fila de cabecera (nombres de columnas)
    FIELDTERMINATOR = ',',      -- Delimitador de columnas
    ROWTERMINATOR = '\n',       -- Delimitador de filas
    TABLOCK
);
```

#### B. Ingesta Directa vía Python + SQL (Pandas `to_sql`)

En Python se puede cargar un CSV con Pandas e insertarlo automáticamente en SQL Server o SQLite:

```python
import pandas as pd
import sqlite3

# 1. Leer el archivo CSV
df = pd.read_csv("dia-01-sql-core/datos_clientes.csv")

# 2. Conectar a la base de datos e insertar los datos
conn = sqlite3.connect("banco.db")
df.to_sql("clientes_banco", conn, if_exists="replace", index=False)

# 3. Consultar y visualizar la información cargada
df_resultado = pd.read_sql_query("SELECT * FROM clientes_banco WHERE saldo_cuenta > 50000", conn)
print(df_resultado)
```

#### C. Visualización e Inspección de Datos Cargados

Una vez importado el CSV, utiliza estas consultas para explorar y auditar la información:

```sql
-- Visualizar las primeras 10 filas de la tabla cargada
SELECT TOP 10 * 
FROM clientes_importados;

-- Auditar total de registros y volumen de saldos por segmento
SELECT 
    segmento,
    COUNT(*) AS total_registros,
    SUM(saldo_cuenta) AS saldo_total,
    AVG(saldo_cuenta) AS saldo_promedio
FROM clientes_importados
GROUP BY segmento
ORDER BY saldo_total DESC;
```

---

### Regla de Oro Itaú #1: Manejo de NULLs en SQL
* **Comparaciones con NULL:** En SQL Standard y T-SQL, comparar `columna = NULL` o `columna <> NULL` devuelve siempre `UNKNOWN` (falso en filtrados `WHERE`).
* **Sintaxis Correcta:** Usar siempre `IS NULL` o `IS NOT NULL`.
* **Funciones de reemplazo:** Usar `COALESCE(columna, valor_defecto)` (estándar ANSI) o `ISNULL(columna, valor_defecto)` (T-SQL) para manejar valores nulos en operaciones aritméticas o de concatenación.

```sql
-- Incorrecto (No retornará filas):
SELECT * FROM Clientes WHERE ejecutivo_id = NULL;

-- Correcto:
SELECT * FROM Clientes WHERE ejecutivo_id IS NULL;

-- Evitar que la suma resulte en NULL:
SELECT cliente_id, COALESCE(saldo_cuenta, 0) + COALESCE(credito_preaprobado, 0) AS total_disponible
FROM Clientes;
```
