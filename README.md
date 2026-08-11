# SQL & Python 7-Day Prep Kit

Repositorio de preparación acelerada para evaluaciones técnicas de nivel profesional en SQL (T-SQL), Python Base, Programación Funcional, Pandas, NumPy y Data Preparation.

---

## Estructura del Repositorio

El contenido está organizado en 7 jornadas diarias de estudio práctico junto con un módulo de instalación y soporte por terminal:

* **[install/](file:///d:/TestSQLPython/install/README.md)**: Guía de configuración, administración de servicios SQL Server (`Get-Service`, `Start-Service`), sintaxis correcta de `sqlcmd` en PowerShell, conexión con Python (`sqlalchemy`/`pyodbc`) y ejecutor auxiliar `run_sql.py`.
* **[dia-01-sql-core/](file:///d:/TestSQLPython/dia-01-sql-core/README.md)**: Modelado E/R, DDL/DML, Operadores, Manejo de NULLs, Orden de Ejecución Lógica e Ingesta de CSVs.
* **[dia-02-sql-avanzado/](file:///d:/TestSQLPython/dia-02-sql-avanzado/README.md)**: Uniones (`INNER`, `LEFT`, `RIGHT`, `FULL`), Trampa de filtros en Joins, **Funciones de Ventana** (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, acumulados), **CTEs (`WITH`) y Tablas Temporales (`#temp`)**, Subqueries, Vistas y Tuning.
* **[dia-03-python-base/](file:///d:/TestSQLPython/dia-03-python-base/README.md)**: Estructuras de datos (Strings, Listas, Tuplas, Sets, Dicts), Mutabilidad, Complejidad Algorítmica $O(1)$ vs $O(N)$ y lectura/escritura de archivos (`with`).
* **[dia-04-python-funcional/](file:///d:/TestSQLPython/dia-04-python-funcional/README.md)**: Lambdas, `map()`, `filter()`, List Comprehensions con condicionales `if/else` en una línea y módulo `math`.
* **[dia-05-python-pandas-numpy/](file:///d:/TestSQLPython/dia-05-python-pandas-numpy/README.md)**: Arrays NumPy, Series/DataFrames, Selección `.loc` vs `.iloc`, Filtros booleanos condicionales, Agregaciones `groupby()` / `merge()` y **Manipulación de Fechas (`.dt`) / Cadenas (`.str`)**.
* **[dia-06-data-prep-ml/](file:///d:/TestSQLPython/dia-06-data-prep-ml/README.md)**: Imputación de Missings por mediana, Detección de Outliers (IQR / Z-Score), Binning (`pd.cut` vs `pd.qcut`) y Scikit-Learn (StandardScaler).
* **[dia-07-simulacro-examen/](file:///d:/TestSQLPython/dia-07-simulacro-examen/README.md)**: Checklist de las 4 Reglas de Oro, Simulacro de Examen Integrado (20 preguntas) y Caso Práctico Integrador.

---

## Contenido de Cada Día

Cada carpeta diaria incluye:
1. `README.md`: Explicación teórica exhaustiva con ejemplos de código y mejores prácticas.
2. `test_evaluacion.md`: Preguntas de opción múltiple / trampa con sus justificaciones técnicas desarrolladas.
3. `ejercicio_practico.py` o `.sql`: Script práctico aplicativo con la solución incluida.

---

## Inicio Rápido

### 1. Verificar e Iniciar el Servicio de SQL Server en PowerShell
Para comprobar si el motor de SQL Server está ejecutándose:

```powershell
Get-Service -Name "*SQL*"
```

Si el servicio `MSSQL$SQLEXPRESS` está detenido, inícialo con:
```powershell
Start-Service -Name "MSSQL$SQLEXPRESS"
```

Para conectarte vía `sqlcmd` (usando `localhost` para evitar errores de ruta en PowerShell):
```powershell
sqlcmd -S "localhost\SQLEXPRESS" -E -d master
```

### 2. Probar scripts de SQL desde PowerShell sin servidor (SQLite runner)
Para ejecutar cualquier archivo `.sql` de forma inmediata mediante Python:

```powershell
python .\install\run_sql.py .\dia-01-sql-core\ejercicio_practico.sql
```

Para abrir una consola interactiva SQL REPL en la terminal:
```powershell
python .\install\run_sql.py -i
```

Para más detalles, consulta la **[Guía de Instalación y Administración](file:///d:/TestSQLPython/install/README.md)**.

### 3. Ejecutar ejercicios de Python
Para ejecutar los scripts de Python de cualquier día:

```powershell
python .\dia-03-python-base\ejercicio_practico.py
python .\dia-04-python-funcional\ejercicio_practico.py
python .\dia-05-python-pandas-numpy\ejercicio_practico.py
python .\dia-06-data-prep-ml\ejercicio_practico.py
python .\dia-07-simulacro-examen\ejercicio_integrador.py
```

