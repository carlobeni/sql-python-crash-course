"""
===============================================================================
EJERCICIO PRÁCTICO DÍA 5: ANÁLISIS DE DATOS VECTORIZADO CON PANDAS & NUMPY
Escenario: Consolidación y Scoring de Cartera de Cuentas (Itaú)
===============================================================================
Objetivo: Integrar datasets de Clientes y Movimientos usando Pandas sin bucles for,
aplicar filtros booleanos avanzados con .loc, agrupaciones vectorizadas y uniones merge.
"""

import pandas as pd
import numpy as np

def ejecutar_analisis_cartera():
    print("--- 1. CREACIÓN DE DATAFRAMES Y UNIONES VECTORIZADAS ---")
    
    # Dataset 1: Clientes
    df_clientes = pd.DataFrame({
        'cliente_id': [1001, 1002, 1003, 1004, 1005],
        'nombre': ['María González', 'Juan Martínez', 'Tech Solutions S.A.', 'Ana Fernández', 'Roberto Gómez'],
        'segmento': ['Premium', 'Retail', 'Corporate', 'Private', 'Retail'],
        'sucursal': ['Centro', 'Palermo', 'Belgrano', 'Centro', 'Palermo']
    })

    # Dataset 2: Cuentas Bancarias
    df_cuentas = pd.DataFrame({
        'cuenta_id': [501, 502, 503, 504, 505],
        'cliente_id': [1001, 1001, 1002, 1003, 1004],
        'tipo_cuenta': ['CUENTA_CORRIENTE', 'CAJA_AHORRO', 'CAJA_AHORRO', 'CUENTA_CORRIENTE', 'CUENTA_CORRIENTE'],
        'saldo_ars': [2500000.0, 125000.0, 45000.0, 15800000.0, -120000.0]
    })

    # 1. UNIÓN CON MERGE (LEFT JOIN para mantener clientes aunque no tengan cuenta)
    df_merged = pd.merge(df_clientes, df_cuentas, on='cliente_id', how='left')
    print("Consolidado Clientes-Cuentas (Merge):")
    print(df_merged[['cliente_id', 'nombre', 'segmento', 'tipo_cuenta', 'saldo_ars']])

    # 2. FILTRADO BOOLEANO AVANZADO CON .LOC (Regla de Oro: & y ~ con paréntesis)
    # Seleccionar clientes Premium o Corporate con saldo positivo > 1,000,000 ARS
    filtro_alto_patrimonio = (
        (df_merged['segmento'].isin(['Premium', 'Corporate'])) &
        (df_merged['saldo_ars'] > 1000000.0)
    )
    
    df_vip = df_merged.loc[filtro_alto_patrimonio, ['cliente_id', 'nombre', 'segmento', 'saldo_ars']]
    print("\nClientes de Alto Patrimonio (Filtrados con .loc):")
    print(df_vip)

    # 3. TRANSFORMACIÓN VECTORIZADA CON NUMPY (Sin bucles FOR - Regla de Oro #4)
    # Asignar categoría de riesgo usando np.select o np.where
    condiciones = [
        df_merged['saldo_ars'] < 0,
        (df_merged['saldo_ars'] >= 0) & (df_merged['saldo_ars'] < 100000),
        df_merged['saldo_ars'] >= 100000
    ]
    opciones = ['ALTO_RIESGO', 'RIESGO_MEDIO', 'BAJO_RIESGO']
    
    df_merged['categoria_riesgo'] = np.select(condiciones, opciones, default='SIN_CUENTA')
    
    # 4. AGREGACIÓN CON GROUPBY Y RESUMEN ESTADÍSTICO
    resumen_sucursal = df_merged.groupby('sucursal').agg(
        total_clientes=('cliente_id', 'nunique'),
        saldo_promedio=('saldo_ars', 'mean'),
        saldo_total=('saldo_ars', 'sum')
    ).reset_index()

    print("\nResumen Estadístico por Sucursal (GroupBy vectorizado):")
    print(resumen_sucursal)

if __name__ == "__main__":
    ejecutar_analisis_cartera()
