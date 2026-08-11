-- ============================================================================
-- EJERCICIO PRÁCTICO DÍA 1: MODELADO, DDL, DML Y FILTROS EN T-SQL
-- Escenario: Sistema de Monitoreo de Clientes y Transacciones Bancarias (Itaú)
-- ============================================================================

-- 1. CREACIÓN DE TABLAS (DDL) CON RESTRICCIONES DE INTEGRIDAD
----------------------------------------------------------------------------
-- Crear Tabla de Clientes
CREATE TABLE clientes_banco (
    cliente_id INT IDENTITY(1001, 1) PRIMARY KEY,
    num_documento VARCHAR(20) NOT NULL UNIQUE,
    nombre_completo VARCHAR(120) NOT NULL,
    segmento VARCHAR(30) NOT NULL CHECK (segmento IN ('Retail', 'Premium', 'Corporate', 'Private')),
    fecha_alta DATE NOT NULL DEFAULT GETDATE(),
    ejecutivo_asignado_id INT NULL,
    estado_cuenta VARCHAR(20) NOT NULL DEFAULT 'ACTIVA' CHECK (estado_cuenta IN ('ACTIVA', 'BLOQUEADA', 'CANCELADA'))
);

-- Crear Tabla de Cuentas Bancarias
CREATE TABLE cuentas_banco (
    cuenta_id INT IDENTITY(50001, 1) PRIMARY KEY,
    cliente_id INT NOT NULL,
    tipo_cuenta VARCHAR(20) NOT NULL CHECK (tipo_cuenta IN ('CAJA_AHORRO', 'CUENTA_CORRIENTE')),
    moneda VARCHAR(3) NOT NULL CHECK (moneda IN ('ARS', 'USD')),
    saldo_actual DECIMAL(18, 2) NOT NULL DEFAULT 0.00,
    limite_descubierto DECIMAL(18, 2) NOT NULL DEFAULT 0.00,
    CONSTRAINT FK_cuentas_clientes FOREIGN KEY (cliente_id) REFERENCES clientes_banco(cliente_id),
    CONSTRAINT CHK_saldo_limite CHECK (saldo_actual >= -limite_descubierto)
);

-- 2. POBLADO DE DATOS DE PRUEBA (DML)
----------------------------------------------------------------------------ö
INSERT INTO clientes_banco (num_documento, nombre_completo, segmento, fecha_alta, ejecutivo_asignado_id, estado_cuenta)
VALUES 
('20358889991', 'María González', 'Premium', '2025-01-15', 101, 'ACTIVA'),
('27401112224', 'Juan Pedro Martínez', 'Retail', '2025-03-20', NULL, 'ACTIVA'),
('30712223338', 'Tech Solutions S.A.', 'Corporate', '2024-06-10', 105, 'ACTIVA'),
('23315556669', 'Ana Lucía Fernández', 'Private', '2025-11-05', 101, 'BLOQUEADA'),
('20184445552', 'Roberto Gómez', 'Retail', '2026-02-01', NULL, 'ACTIVA');

INSERT INTO cuentas_banco (cliente_id, tipo_cuenta, moneda, saldo_actual, limite_descubierto)
VALUES 
(1001, 'CUENTA_CORRIENTE', 'ARS', 2500000.00, 500000.00),
(1001, 'CAJA_AHORRO', 'USD', 12500.00, 0.00),
(1002, 'CAJA_AHORRO', 'ARS', 45000.00, 0.00),
(1003, 'CUENTA_CORRIENTE', 'ARS', 15800000.00, 2000000.00),
(1004, 'CUENTA_CORRIENTE', 'ARS', -120000.00, 300000.00),
(1005, 'CAJA_AHORRO', 'ARS', 0.00, 0.00);

-- 3. CONSULTAS DE EVALUACIÓN Y FILTRADO AVANZADO (DML - SELECT)
----------------------------------------------------------------------------

-- REQUERIMIENTO 1:
-- Obtener todos los clientes activos del segmento 'Premium' o 'Private' que 
-- tengan un ejecutivo asignado (es decir, que ejecutivo_asignado_id NO sea NULL).
SELECT 
    cliente_id,
    num_documento,
    nombre_completo,
    segmento,
    ejecutivo_asignado_id
FROM clientes_banco
WHERE estado_cuenta = 'ACTIVA'
  AND segmento IN ('Premium', 'Private')
  AND ejecutivo_asignado_id IS NOT NULL;


-- REQUERIMIENTO 2 (Manejo de Nulos con COALESCE/ISNULL):
-- Generar un reporte de cuentas en ARS mostrando el saldo_actual, límite_descubierto
-- y el capital_total_disponible (saldo_actual + limite_descubierto).
-- Asegurarse de que si el limite_descubierto fuese NULL, la suma no retorne NULL.
SELECT 
    cuenta_id,
    cliente_id,
    tipo_cuenta,
    saldo_actual,
    COALESCE(limite_descubierto, 0.00) AS limite_descubierto,
    (saldo_actual + COALESCE(limite_descubierto, 0.00)) AS capital_total_disponible
FROM cuentas_banco
WHERE moneda = 'ARS'
  AND (saldo_actual + COALESCE(limite_descubierto, 0.00)) > 50000.00
ORDER BY capital_total_disponible DESC;


-- REQUERIMIENTO 3 (Actualización defensiva DML con UPDATE):
-- Incrementar en un 10% el limite_descubierto solo a aquellas cuentas corrientes en ARS 
-- cuyo cliente sea del segmento 'Corporate' y su saldo actual sea positivo.
UPDATE c
SET c.limite_descubierto = c.limite_descubierto * 1.10
FROM cuentas_banco c
INNER JOIN clientes_banco cb ON c.cliente_id = cb.cliente_id
WHERE c.tipo_cuenta = 'CUENTA_CORRIENTE'
  AND c.moneda = 'ARS'
  AND cb.segmento = 'Corporate'
  AND c.saldo_actual > 0;
