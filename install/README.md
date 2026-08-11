# Guía de Instalación y Ejecución de SQL por Terminal (PowerShell)

Esta guía explica cómo instalar y configurar las herramientas necesarias para ejecutar consultas SQL de forma interactiva en la terminal PowerShell o ejecutar archivos de script `.sql` previamente programados.

---

## 1. Opciones de Herramientas para Terminal

Existen dos alternativas principales para trabajar con SQL desde la terminal en Windows:

| Herramienta | Motor | Descripción / Caso de Uso |
| :--- | :--- | :--- |
| **`sqlcmd`** | Microsoft SQL Server | Utilidad oficial de línea de comandos para T-SQL. Ideal para simular el entorno oficial Itaú. |
| **`sqlite3`** | SQLite | Motor ligero sin servidor. Ideal para pruebas rápidas y locales sin configurar servicios. |
| **`run_sql.py`** | Python + SQLite/DuckDB | Script de soporte incluido en este repositorio para ejecutar archivos `.sql` directamente con Python. |

---

## 2. Instalación de Herramientas

### Opción A: Instalación de `sqlcmd` (Microsoft SQL Server CLI)

Para ejecutar código T-SQL nativo en PowerShell mediante `sqlcmd`:

1. Abre PowerShell como Administrador e instala `sqlcmd` usando Windows Package Manager (`winget`):
   ```powershell
   winget install Microsoft.Sqlcmd
   ```
2. Verifica la instalación ejecutando:
   ```powershell
   sqlcmd -?
   ```

*(Nota: Si usas SQL Server Express o LocalDB, asegúrate de tener iniciado el servicio de SQL Server).*

---

### Opción B: Instalación de `sqlite3` CLI

1. Instala `sqlite3` mediante `winget`:
   ```powershell
   winget install SQLite.SQLite
   ```
2. O bien descarga los binarios de la página oficial de SQLite y agrega la carpeta al `PATH` de Windows.

---

## 3. Guía de Ejecución en Terminal (PowerShell)

### A. Ejecutar consultas SQL de forma interactiva (Modo Consola)

#### Usando `sqlcmd` (T-SQL / SQL Server):
```powershell
# Conectarse a una instancia local (ej. LocalDB o SQL Server local)
sqlcmd -S "(localdb)\MSSQLLocalDB" -d master

# Una vez dentro del prompt 1>, escribe tus comandos y finaliza con 'GO':
1> CREATE DATABASE banco_db;
2> GO
3> USE banco_db;
4> GO
5> SELECT GETDATE() AS fecha_actual;
6> GO
7> QUIT
```

#### Usando `sqlite3`:
```powershell
# Abrir o crear una base de datos local llamada banco.db
sqlite3 banco.db

# Escribir comandos directamente finalizando con punto y coma (;):
sqlite> CREATE TABLE prueba (id INT, nombre TEXT);
sqlite> INSERT INTO prueba VALUES (1, 'Carlos');
sqlite> SELECT * FROM prueba;
sqlite> .exit
```

---

### B. Ejecutar scripts preprogramados (`.sql`) desde PowerShell

#### 1. Ejecutar un archivo `.sql` con `sqlcmd`:
```powershell
# Sintaxis: sqlcmd -S <servidor> -d <base_datos> -i <archivo.sql>
sqlcmd -S "(localdb)\MSSQLLocalDB" -d banco_db -i .\dia-01-sql-core\ejercicio_practico.sql
```

#### 2. Guardar el resultado de la ejecución en un archivo de texto de salida:
```powershell
sqlcmd -S "(localdb)\MSSQLLocalDB" -d banco_db -i .\dia-01-sql-core\ejercicio_practico.sql -o .\resultado_dia1.txt
```

#### 3. Ejecutar una consulta directa en una sola línea de PowerShell (parámetro `-Q`):
```powershell
sqlcmd -S "(localdb)\MSSQLLocalDB" -d banco_db -Q "SELECT TOP 5 * FROM clientes_banco;"
```

#### 4. Ejecutar un archivo `.sql` con `sqlite3`:
```powershell
Get-Content .\dia-01-sql-core\ejercicio_practico.sql | sqlite3 banco.db
```

---

## 4. Ejecución Inmediata mediante Script de Soporte (`run_sql.py`)

Si no deseas configurar servidores de SQL Server en tu máquina, este repositorio incluye el script `run_sql.py` en la carpeta `install/` que utiliza el motor embebido de Python para ejecutar cualquier archivo `.sql`:

### Modos de uso de `run_sql.py`:

1. **Ejecutar un archivo `.sql` completo:**
   ```powershell
   python .\install\run_sql.py .\dia-01-sql-core\ejercicio_practico.sql
   ```

2. **Modo consola interactiva REPL (para escribir SQL en vivo):**
   ```powershell
   python .\install\run_sql.py -i
   ```
