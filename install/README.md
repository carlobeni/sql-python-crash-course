# Guía de Instalación y Ejecución con Microsoft SQL Server 2022 Express & sqlcmd

Esta guía detalla el procedimiento oficial para instalar, configurar y ejecutar consultas T-SQL utilizando **Microsoft SQL Server 2022 Express** y la herramienta oficial de línea de comandos **`sqlcmd`** desde la terminal PowerShell.

---

## 1. Stack Tecnológico de Trabajo

| Componente | Nombre | Descripción |
| :--- | :--- | :--- |
| **Motor SQL** | Microsoft SQL Server 2022 Express | Motor relacional T-SQL oficial, 100% gratuito y compatible con los entornos corporativos Itaú / Azure. |
| **CLI / Terminal** | `sqlcmd` | Herramienta oficial de línea de comandos para la ejecución interactiva o por lotes de archivos `.sql`. |

---

## 2. Instalación de SQL Server 2022 Express y sqlcmd

### Paso 1: Instalación del Motor SQL Server 2022 Express

Abre una ventana de PowerShell como Administrador y ejecuta el siguiente comando mediante Windows Package Manager (`winget`):

```powershell
winget install Microsoft.SQLServer.2022.Express
```

*(Alternativamente, puedes realizar la descarga directa desde el sitio oficial de Microsoft: [SQL Server 2022 Express Downloads](https://www.microsoft.com/es-es/sql-server/sql-server-downloads)).*

### Paso 2: Verificación de la herramienta `sqlcmd`

Comprueba que el comando `sqlcmd` esté disponible en la terminal ejecutando:

```powershell
sqlcmd -?
```

---

## 3. Administración y Verificación de Servicios SQL en PowerShell

Antes de conectarte, es esencial verificar qué motores e instancias SQL están activos en tu equipo y saber cómo iniciarlos o detenerlos desde PowerShell.

### Paso 1: Ver los Servicios SQL Activos e Instalados

Abre PowerShell y ejecuta el siguiente comando para auditar el estado de los servicios de SQL Server:

```powershell
Get-Service -Name "*SQL*"
```

#### Ejemplo de salida en PowerShell:
```text
Status   Name               DisplayName                           
------   ----               -----------                           
Running  MSSQL$SQLEXPRESS   SQL Server (SQLEXPRESS)               
Stopped  SQLAgent$SQLEXP... SQL Server Agent (SQLEXPRESS)         
Running  SQLBrowser         SQL Server Browser                    
```

* Si `MSSQL$SQLEXPRESS` figura como **`Running`**, el servicio ya está listo para aceptar conexiones.
* Si figura como **`Stopped`**, debes iniciarlo según el siguiente paso.

---

### Paso 2: Iniciar o Detener el Servicio SQL Server Express

Si el servicio está detenido, ejecútalo desde PowerShell (modo Administrador):

#### Iniciar el servicio SQL Server Express:
```powershell
# Usando Cmdlet nativo de PowerShell
Start-Service -Name "MSSQL$SQLEXPRESS"

# O mediante comando NET clásico:
net start MSSQL$SQLEXPRESS
```

#### Detener el servicio:
```powershell
Stop-Service -Name "MSSQL$SQLEXPRESS"
# O bien:
net stop MSSQL$SQLEXPRESS
```

---

### Paso 3: Gestión de Instancias de LocalDB (`MSSQLLocalDB`)

Si utilizas LocalDB (instancia ligera de desarrollo integrada en Visual Studio / SQL Tools), puedes verificar e iniciar su estado con la CLI `sqllocaldb`:

```powershell
# Ver las instancias de LocalDB existentes y su estado
sqllocaldb info

# Ver el detalle de la instancia principal MSSQLLocalDB
sqllocaldb info MSSQLLocalDB

# Iniciar la instancia MSSQLLocalDB
sqllocaldb start MSSQLLocalDB

# Detener la instancia
sqllocaldb stop MSSQLLocalDB
```

---

## 4. Guía de Ejecución en PowerShell mediante `sqlcmd`

### ⚠️ Solución al Error Común en PowerShell: *"The system cannot find the file specified"*

En versiones recientes de `sqlcmd` (CLI basada en Go v16+), ejecutar:
`sqlcmd -S ".\SQLEXPRESS" -E -d master`
puede arrojar el error: `The system cannot find the file specified.`

**¿Por qué sucede?** En PowerShell, la secuencia `".\SQLEXPRESS"` entre comillas dobles es interpretada por el parser como un intento de ejecutar/abrir un archivo en el directorio actual.

**Solución Sintáctica Recomendada:** Usar comillas simples `' .\SQLEXPRESS '` o la palabra clave `"localhost\SQLEXPRESS"`:

```powershell
# Opción Recomendada A (localhost):
sqlcmd -S "localhost\SQLEXPRESS" -E -d master

# Opción Recomendada B (comillas simples):
sqlcmd -S '.\SQLEXPRESS' -E -d master

# Opción Recomendada C (LocalDB):
sqlcmd -S "(localdb)\MSSQLLocalDB" -d master
```

---

### A. Ejecución de Consultas Interactivas (Modo REPL)

Para abrir la consola interactiva T-SQL en directo:

```powershell
sqlcmd -S "localhost\SQLEXPRESS" -E -d master
```

#### Ejemplo de sesión interactiva en la consola `sqlcmd`:
```text
1> CREATE DATABASE banco_itau;
2> GO
3> USE banco_itau;
4> GO
5> SELECT @@VERSION AS version_sqlserver;
6> GO
7> QUIT
```

---

### B. Ejecución de Archivos Preprogramados (`.sql`)

Para ejecutar un script `.sql` completo del curso y procesar todas sus sentencias de forma automática:

#### 1. Ejecutar el script del Día 1:
```powershell
sqlcmd -S "localhost\SQLEXPRESS" -E -d master -i .\dia-01-sql-core\ejercicio_practico.sql
```

#### 2. Redireccionar el resultado de la ejecución a un archivo de salida (.txt):
```powershell
sqlcmd -S "localhost\SQLEXPRESS" -E -d master -i .\dia-01-sql-core\ejercicio_practico.sql -o .\resultado_ejecucion_dia1.txt
```

#### 3. Ejecutar una consulta directa de una sola línea (Parámetro `-Q`):
```powershell
sqlcmd -S "localhost\SQLEXPRESS" -E -d master -Q "SELECT name, create_date FROM sys.databases;"
```

---

## 5. Conexión Programática desde Python a SQL Server Express

Si deseas conectar tus scripts de Python a la instancia local de SQL Server Express utilizando `pyodbc` y `sqlalchemy`:

```python
import pandas as pd
import urllib
from sqlalchemy import create_engine

# String de conexión para SQL Server Express con Windows Authentication
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

params = urllib.parse.quote_plus(conn_str)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Probar lectura directa a DataFrame
df_bases = pd.read_sql("SELECT name, create_date FROM sys.databases;", engine)
print(df_bases)
```

---

## 6. Herramienta Auxiliar Alternativa (`run_sql.py`)

Si necesitas probar un archivo `.sql` de forma rápida en entornos donde no tengas permisos de administrador para iniciar el servicio de SQL Server, puedes utilizar el script de soporte en Python incluido en esta carpeta (que utiliza SQLite en memoria):

```powershell
# Ejecución directa con Python
python .\install\run_sql.py .\dia-01-sql-core\ejercicio_practico.sql

# Consola interactiva en Python
python .\install\run_sql.py -i
```

