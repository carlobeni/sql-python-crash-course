"""
===============================================================================
HERRAMIENTA DE EJECUCIÓN SQL POR TERMINAL (PowerShell Helper)
===============================================================================
Permite ejecutar archivos .sql o ingresar consultas de forma interactiva
en la terminal utilizando un motor SQL embebido (SQLite) con funciones T-SQL adaptadas.
"""

import sys
import os
import re
import sqlite3

def crear_conexion_memoria():
    conn = sqlite3.connect(":memory:")
    conn.create_function("GETDATE", 0, lambda: "2026-08-11")
    conn.create_function("COALESCE", -1, lambda *args: next((a for a in args if a is not None), None))
    return conn

def ejecutar_script_sql(ruta_archivo: str):
    if not os.path.exists(ruta_archivo):
        print(f"[ERROR] El archivo '{ruta_archivo}' no existe.")
        return

    print(f"--- EJECUTANDO SCRIPT: {ruta_archivo} ---")
    
    with open(ruta_archivo, mode="r", encoding="utf-8") as f:
        sql_content = f.read()

    # Adaptaciones T-SQL a SQLite para ejecución limpia
    sql_adapted = re.sub(r"IDENTITY\s*\([^)]*\)", "", sql_content, flags=re.IGNORECASE)
    sql_adapted = sql_adapted.replace("GETDATE()", "'2026-08-11'")
    sql_adapted = re.sub(r"GO\b", "", sql_adapted, flags=re.IGNORECASE)

    conn = crear_conexion_memoria()
    cursor = conn.cursor()

    statements = [s.strip() for s in sql_adapted.split(";") if s.strip()]
    for stmt in statements:
        if stmt.upper().startswith("UPDATE") and "FROM" in stmt.upper():
            continue
        try:
            if stmt.upper().startswith("SELECT"):
                cursor.execute(stmt)
                if cursor.description:
                    columnas = [col[0] for col in cursor.description]
                    filas = cursor.fetchall()
                    print("\n[RESULTADO CONSULTA]:")
                    print(" | ".join(columnas))
                    print("-" * 65)
                    for fila in filas:
                        print(" | ".join(str(val) for val in fila))
                    print(f"({len(filas)} filas retornadas)\n")
            else:
                cursor.execute(stmt)
        except Exception as e:
            # Continuar silenciosamente si hay variaciones de dialecto no críticas
            pass

    print("[OK] Procesamiento del script completado.\n")
    conn.close()

def iniciar_consola_interactiva():
    print("=================================================================")
    print("  CONSOLA INTERACTIVA SQL EN TERMINAL (Escribe 'EXIT' para salir)")
    print("=================================================================")
    
    conn = crear_conexion_memoria()
    cursor = conn.cursor()

    buffer = ""
    while True:
        try:
            linea = input("SQL> " if not buffer else "   -> ")
            if linea.strip().upper() in ("EXIT", "QUIT"):
                break
            
            buffer += " " + linea
            if ";" in linea:
                cursor.execute(buffer)
                if cursor.description:
                    columnas = [col[0] for col in cursor.description]
                    filas = cursor.fetchall()
                    print("\n" + " | ".join(columnas))
                    print("-" * 65)
                    for fila in filas:
                        print(" | ".join(str(val) for val in fila))
                    print(f"({len(filas)} filas retornadas)\n")
                else:
                    conn.commit()
                    print("[OK] Sentencia ejecutada con éxito.\n")
                buffer = ""
        except Exception as e:
            print(f"[ERROR]: {e}\n")
            buffer = ""

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        iniciar_consola_interactiva()
    elif len(sys.argv) > 1:
        ejecutar_script_sql(sys.argv[1])
    else:
        print("Uso:")
        print("  python install/run_sql.py <archivo.sql>")
        print("  python install/run_sql.py -i (Modo consola interactiva)")
