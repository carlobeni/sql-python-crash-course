"""
===============================================================================
EJERCICIO INTEGRADOR FINAL DÍA 7: EVALUACIÓN TÉCNICA EXPRESS ITAÚ
Escenario: Scoring de Riesgo Crediticio y Pipeline End-to-End
===============================================================================
Objetivo: Simular el flujo completo de evaluación técnica:
1. Simulación de extracción de datos tipo SQL con JOINs y manejo de nulos.
2. Limpieza en Pandas: Imputación de nulos por mediana de grupo.
3. Detección y Capping de Outliers mediante IQR.
4. Transformación en 1 línea (List Comprehensions / lambdas) para etiquetado.
5. Exportación de métricas consolidadas.
"""

import pandas as pd
import numpy as np
import math

def ejecutar_simulacro_integrador():
    print("=================================================================")
    print("  SIMULACRO DE EVALUACIÓN TÉCNICA INTEGRADORA (PYTHON & SQL)")
    print("=================================================================\n")

    # --- PASO 1: SIMULACIÓN DE RESULTADO DE CONSULTA SQL CON LEFT JOIN ---
    print("1. Carga de Universo de Clientes (Simulación T-SQL Join)...")
    
    raw_db_data = [
        {"cliente_id": 1001, "nombre": "María González", "segmento": "Premium", "saldo_ars": 2500000.0, "mora_dias": 0, "ingreso": 850000.0},
        {"cliente_id": 1002, "nombre": "Juan Martínez", "segmento": "Retail", "saldo_ars": 45000.0, "mora_dias": 15, "ingreso": np.nan}, # Missing
        {"cliente_id": 1003, "nombre": "Tech Solutions S.A.", "segmento": "Corporate", "saldo_ars": 15800000.0, "mora_dias": 0, "ingreso": 5200000.0},
        {"cliente_id": 1004, "nombre": "Ana Fernández", "segmento": "Private", "saldo_ars": -120000.0, "mora_dias": 45, "ingreso": 1200000.0},
        {"cliente_id": 1005, "nombre": "Roberto Gómez", "segmento": "Retail", "saldo_ars": 0.0, "mora_dias": 0, "ingreso": 320000.0},
        {"cliente_id": 1006, "nombre": "Lucía Méndez", "segmento": "Retail", "saldo_ars": 98000000.0, "mora_dias": 0, "ingreso": 450000.0}, # Outlier Saldo
        {"cliente_id": 1007, "nombre": "Esteban Quito", "segmento": "Premium", "saldo_ars": 750000.0, "mora_dias": 0, "ingreso": np.nan}, # Missing
    ]

    df = pd.DataFrame(raw_db_data)

    # --- PASO 2: REGLA DE ORO #1 Y #4 - IMPUTACIÓN INTELIGENTE EN PANDAS ---
    print("\n2. Tratamiento de Missings en Ingresos por Mediana de Segmento...")
    df['ingreso_imputado'] = df.groupby('segmento')['ingreso'].transform(
        lambda group: group.fillna(group.median())
    )
    
    # Si algún segmento tuviese todos NaN, llenar con la mediana global
    df['ingreso_imputado'] = df['ingreso_imputado'].fillna(df['ingreso_imputado'].median())
    print("   Ingresos Imputados correctamente sin bucles for.")

    # --- PASO 3: DETECCIÓN Y CAPPING DE OUTLIERS POR IQR ---
    print("\n3. Detección y Capping de Outliers en Saldo (IQR)...")
    Q1 = df['saldo_ars'].quantile(0.25)
    Q3 = df['saldo_ars'].quantile(0.75)
    IQR = Q3 - Q1
    lim_sup = Q3 + 1.5 * IQR
    lim_inf = Q1 - 1.5 * IQR

    print(f"   Límite Superior IQR: ${lim_sup:,.2f}")
    df['saldo_limpio'] = np.clip(df['saldo_ars'], lim_inf, lim_sup)

    # --- PASO 4: REGLA DE ORO #3 - SINTAXIS ÁGIL EN 1 LÍNEA (LIST COMPREHENSION) ---
    print("\n4. Evaluación de Semáforo de Riesgo (1 Línea funcional)...")
    # Regla: Si mora > 30 o saldo < 0 -> ALTO_RIESGO; si mora > 0 -> MEDIO_RIESGO; else -> BAJO_RIESGO
    df['semaforo_riesgo'] = [
        "ALTO_RIESGO" if (row['mora_dias'] > 30 or row['saldo_ars'] < 0)
        else ("MEDIO_RIESGO" if row['mora_dias'] > 0 else "BAJO_RIESGO")
        for _, row in df.iterrows() # Usado solo para expresión inline demo
    ]

    # Versión Vectorizada pura con np.select (Recomendada en producción):
    condiciones = [
        (df['mora_dias'] > 30) | (df['saldo_ars'] < 0),
        df['mora_dias'] > 0
    ]
    opciones = ["ALTO_RIESGO", "MEDIO_RIESGO"]
    df['semaforo_riesgo_vec'] = np.select(condiciones, opciones, default="BAJO_RIESGO")

    # --- PASO 5: RESUMEN FINAL Y REPORTE EJECUTIVO ---
    print("\n=================================================================")
    print("  REPORTE FINAL CONSOLIDADO (EVALUACIÓN SUPERADA >= 70%)")
    print("=================================================================")
    
    columnas_reporte = ['cliente_id', 'nombre', 'segmento', 'saldo_limpio', 'ingreso_imputado', 'semaforo_riesgo_vec']
    print(df[columnas_reporte].to_string(index=False))

    resumen = df.groupby('semaforo_riesgo_vec').agg(
        total_clientes=('cliente_id', 'count'),
        saldo_promedio=('saldo_limpio', 'mean'),
        ingreso_promedio=('ingreso_imputado', 'mean')
    ).reset_index()

    print("\nResumen Estadístico por Categoría de Riesgo:")
    print(resumen.to_string(index=False))

if __name__ == "__main__":
    ejecutar_simulacro_integrador()
