"""
===============================================================================
EJERCICIO PRÁCTICO DÍA 3: PROCESADOR DE ARCHIVOS Y ESTRUCTURAS PYTHON PURO
Escenario: Validación de Transacciones Sospechosas y Anti-Lavado de Dinero (AML)
===============================================================================
Objetivo: Procesar una cadena simulada de datos de transacciones en formato CSV,
deduplicar clientes, clasificar movimientos y calcular saldos en Python puro
sin utilizar librerías externas (Pandas/NumPy).
"""

# Datos de entrada simulados (CSV con cabecera)
RAW_CSV_DATA = """transaccion_id,cuit_cliente,tipo_operacion,monto,sucursal
TX-1001,20-35888999-1,DEPOSITO,150000.00,Centro
TX-1002,27-40111222-4,TRANSFERENCIA_OUT,50000.00,Palermo
TX-1003,20-35888999-1,TRANSFERENCIA_OUT,200000.00,Centro
TX-1004,30-71222333-8,DEPOSITO,5000000.00,Belgrano
TX-1005,23-31555666-9,EXTRACCION,8000.00,Centro
TX-1006,20-35888999-1,DEPOSITO,45000.00,Centro
TX-1007,27-40111222-4,DEPOSITO,120000.00,Palermo
"""

def procesar_transacciones_aml(csv_data: str):
    print("--- 1. PROCESANDO RAW DATA CON PYTHON BASE ---")
    
    lineas = csv_data.strip().split("\n")
    cabecera = lineas[0].split(",")
    filas = lineas[1:]

    # Estructuras de control
    cuits_unicos = set()
    totales_por_cuit = {}
    operaciones_por_sucursal = {}
    transacciones_alto_monto = []

    UMBRAL_ALTO_MONTO = 150000.00

    for linea in filas:
        if not linea.strip():
            continue

        campos = linea.split(",")
        tx_id = campos[0]
        cuit_raw = campos[1]
        tipo_op = campos[2]
        monto = float(campos[3])
        sucursal = campos[4]

        # A. Normalización de CUIT (String manipulation)
        cuit_limpio = cuit_raw.replace("-", "").strip()
        cuits_unicos.add(cuit_limpio)

        # B. Acumulación por cliente usando dict.setdefault() o dict.get()
        saldo_actual = totales_por_cuit.get(cuit_limpio, 0.0)
        if tipo_op in ("DEPOSITO", "TRANSFERENCIA_IN"):
            totales_por_cuit[cuit_limpio] = saldo_actual + monto
        else:
            totales_por_cuit[cuit_limpio] = saldo_actual - monto

        # C. Conteo de transacciones por sucursal
        operaciones_por_sucursal[sucursal] = operaciones_por_sucursal.get(sucursal, 0) + 1

        # D. Filtrado de transacciones de alto monto (Tuplas para registros inmutables)
        if monto >= UMBRAL_ALTO_MONTO:
            registro_tx = (tx_id, cuit_limpio, tipo_op, monto, sucursal)
            transacciones_alto_monto.append(registro_tx)

    # --- RESULTADOS Y SALIDA ---
    print(f"Total CUITs únicos atendidos (usando Set O(1)): {len(cuits_unicos)}")
    print("\nSaldos netos consolidados por CUIT:")
    for cuit, saldo in totales_por_cuit.items():
        print(f"  - CUIT {cuit}: ${saldo:,.2f}")

    print("\nTransacciones de Alto Monto (>= $150,000):")
    for tx in transacciones_alto_monto:
        print(f"  [ALERTA AML] ID: {tx[0]} | Cliente: {tx[1]} | Tipo: {tx[2]} | Monto: ${tx[3]:,.2f} | Suc: {tx[4]}")

    print("\nDistribución de operaciones por Sucursal:")
    for suc, cantidad in operaciones_por_sucursal.items():
        print(f"  - Sucursal {suc}: {cantidad} movimiento(s)")

if __name__ == "__main__":
    procesar_transacciones_aml(RAW_CSV_DATA)
