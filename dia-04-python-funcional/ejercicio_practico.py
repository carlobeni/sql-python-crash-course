"""
===============================================================================
EJERCICIO PRÁCTICO DÍA 4: PROGRAMACIÓN FUNCIONAL Y TRANSFORMACOES EN 1 LÍNEA
Escenario: Preprocesamiento Funcional de Scoring Financiero y Comisiones Itaú
===============================================================================
Objetivo: Implementar un motor de procesamiento de datos utilizando únicamente
expresiones funcionales en una sola línea (List Comprehensions, map, filter, lambdas)
y validaciones con el módulo math.
"""

import math

# Colección de prueba: (cliente_id, score_crediticio, ingreso_mensual, tiene_mora)
CLIENTES_DATA = [
    (101, 750, 2500000.0, False),
    (102, 580, 850000.0, True),
    (103, 820, 4200000.0, False),
    (104, 450, 400000.0, True),
    (105, 690, float('nan'), False), # Dato faltante / corrupto
    (106, 710, 1900000.0, False),
]

def ejecutar_pipeline_funcional():
    print("--- PIPELINE FUNCIONAL Y REGLAS DE ORO PYTHON ---")

    # 1. FILTRADO Y LIMPIEZA DE DATOS (Módulo math.isnan)
    # Conservar solo clientes con ingresos válidos (no NaN) y sin mora activa
    clientes_validos = list(
        filter(
            lambda c: not math.isnan(c[2]) and not c[3],
            CLIENTES_DATA
        )
    )
    print(f"1. Clientes válidos sin mora ni NaNs: {len(clientes_validos)}")

    # 2. TRANSFORMACIÓN EN 1 LÍNEA: LIST COMPREHENSION CON TERNARIO IF/ELSE (Regla de Oro #3)
    # Calcular la tasa de interés personalizada según el Score:
    # Score >= 700 -> Tasa PREFERENCIAL 15.5%
    # Score < 700  -> Tasa ESTÁNDAR 24.0%
    tasas_personalizadas = [
        (c[0], c[1], 15.5 if c[1] >= 700 else 24.0)
        for c in clientes_validos
    ]
    print("\n2. Tasas asignadas por cliente (List Comprehension en 1 línea):")
    for t in tasas_personalizadas:
        print(f"   Cliente {t[0]} | Score: {t[1]} -> Tasa: {t[2]}%")

    # 3. TRANSFORMACIÓN EN 1 LÍNEA USANDO MAP() Y LAMBDA:
    # Calcular la capacidad máxima de cuota mensual (30% del ingreso mensual)
    # y redondear al entero superior utilizando math.ceil
    capacidades_cuota = list(
        map(
            lambda c: (c[0], math.ceil(c[2] * 0.30)),
            clientes_validos
        )
    )
    print("\n3. Capacidad máxima de cuota calculada con map() + math.ceil:")
    for cap in capacidades_cuota:
        print(f"   Cliente {cap[0]} -> Cuota Máxima Sugerida: ${cap[1]:,}")

    # 4. EXPRESIÓN DE UNA SOLA LÍNEA COMPACTA FINALES (Detección de Clientes VIP):
    # Generar una lista de CUITs/IDs de clientes cuyos ingresos sean superiores a 2M y score >= 750
    vips = [c[0] for c in CLIENTES_DATA if not math.isnan(c[2]) and c[2] > 2000000.0 and c[1] >= 750]
    print(f"\n4. Clientes elegibles para atención VIP (Filtro 1 línea): {vips}")

if __name__ == "__main__":
    ejecutar_pipeline_funcional()
