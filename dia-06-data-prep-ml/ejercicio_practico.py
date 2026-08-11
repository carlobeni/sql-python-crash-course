"""
===============================================================================
EJERCICIO PRÁCTICO DÍA 6: PIPELINE DE DATA PREPARATION Y PREPROCESAMIENTO
Escenario: Limpieza, Detección de Outliers e Imputación de Cartera Itaú
===============================================================================
Objetivo: Construir un pipeline modular de Data Prep en Python que realice:
1. Imputación inteligente de valores faltantes por segmento.
2. Detección y tratamiento de outliers por Rango Intercuartílico (IQR).
3. Discretización de scoring mediante pd.qcut / pd.cut.
4. Escalado estandarizado con Scikit-Learn (StandardScaler).
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def pipeline_data_prep():
    print("--- 1. CARGA DE DATASET FINANCIERO SINTÉTICO ---")
    
    np.random.seed(42)
    n = 200
    
    data = {
        'cliente_id': np.arange(1001, 1001 + n),
        'segmento': np.random.choice(['Retail', 'Premium', 'Corporate'], size=n, p=[0.6, 0.3, 0.1]),
        'ingreso_mensual': np.random.exponential(scale=300000, size=n) + 150000,
        'edad': np.random.randint(18, 75, size=n).astype(float),
        'score_crediticio': np.random.normal(loc=650, scale=100, size=n)
    }

    df = pd.DataFrame(data)

    # Introducir Missings artificiales en ingreso_mensual
    indices_missing = np.random.choice(df.index, size=20, replace=False)
    df.loc[indices_missing, 'ingreso_mensual'] = np.nan

    # Introducir Outliers artificiales extremadamente altos
    df.loc[10, 'ingreso_mensual'] = 25000000.0  # 25 Millones ARS
    df.loc[25, 'ingreso_mensual'] = 18000000.0  # 18 Millones ARS

    print(f"Total filas: {len(df)} | Nulos en ingreso_mensual: {df['ingreso_mensual'].isnull().sum()}")

    # --- PASO 2: IMPUTACIÓN DE MISSINGS (Mediana por Segmento) ---
    print("\n--- 2. IMPUTACIÓN DE MISSINGS ---")
    df['ingreso_imputado'] = df.groupby('segmento')['ingreso_mensual'].transform(
        lambda g: g.fillna(g.median())
    )
    print(f"Nulos restantes tras imputación: {df['ingreso_imputado'].isnull().sum()}")

    # --- PASO 3: DETECCIÓN Y CAPPING DE OUTLIERS POR IQR ---
    print("\n--- 3. TRATAMIENTO DE OUTLIERS (MÉTODO IQR) ---")
    Q1 = df['ingreso_imputado'].quantile(0.25)
    Q3 = df['ingreso_imputado'].quantile(0.75)
    IQR = Q3 - Q1
    limite_inf = Q1 - 1.5 * IQR
    limite_sup = Q3 + 1.5 * IQR

    outliers_detectados = df[df['ingreso_imputado'] > limite_sup]
    print(f"Límite superior IQR calculado: ${limite_sup:,.2f}")
    print(f"Total Outliers detectados: {len(outliers_detectados)}")

    # Capping (Winsorización) para no perder los registros
    df['ingreso_clean'] = np.clip(df['ingreso_imputado'], limite_inf, limite_sup)

    # --- PASO 4: DISCRETIZACIÓN Y BINNING (pd.qcut vs pd.cut) ---
    print("\n--- 4. CATEGORIZACIÓN / BINNING ---")
    # pd.qcut para garantizar 4 grupos con igual cantidad de clientes (Cuartiles de Ingreso)
    df['cuartil_ingreso'] = pd.qcut(df['ingreso_clean'], q=4, labels=['Q1_Bajo', 'Q2_MedioBajo', 'Q3_MedioAlto', 'Q4_Alto'])

    # pd.cut para rangos fijos de edad
    df['rango_etario'] = pd.cut(df['edad'], bins=[0, 30, 50, 100], labels=['Joven', 'Adulto', 'Senior'])

    print("Distribución homogénea con pd.qcut (Cuartiles):")
    print(df['cuartil_ingreso'].value_counts())

    # --- PASO 5: ESCALADO CON SCIKIT-LEARN (StandardScaler) ---
    print("\n--- 5. ESCALADO DE FEATURES (StandardScaler) ---")
    scaler = StandardScaler()
    features_num = ['ingreso_clean', 'edad', 'score_crediticio']
    
    df_scaled = pd.DataFrame(
        scaler.fit_transform(df[features_num]),
        columns=[f"{col}_std" for col in features_num]
    )

    df_final = pd.concat([df[['cliente_id', 'segmento', 'cuartil_ingreso', 'rango_etario']], df_scaled], axis=1)
    
    print("Muestra del Dataset Final Procesado y Listo para Modelo:")
    print(df_final.head())

if __name__ == "__main__":
    pipeline_data_prep()
