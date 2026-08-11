-- ============================================================================
-- EJERCICIO PRÁCTICO DÍA 2: SQL AVANZADO (JOINS, AGREGACIONES, VISTAS & TUNING)
-- Escenario: Evaluación de Desempeño Operativo y Riesgo Crediticio Itaú
-- ============================================================================

-- 1. ESTRUCTURA DE TABLAS E INSERCIÓN DE DATOS
----------------------------------------------------------------------------
IF OBJECT_ID('movimientos_cuenta', 'U') IS NOT NULL DROP TABLE movimientos_cuenta;
IF OBJECT_ID('tarjetas_credito', 'U') IS NOT NULL DROP TABLE tarjetas_credito;
IF OBJECT_ID('cuentas', 'U') IS NOT NULL DROP TABLE cuentas;
IF OBJECT_ID('clientes', 'U') IS NOT NULL DROP TABLE clientes;

CREATE TABLE clientes (
    cliente_id INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    sucursal_origen VARCHAR(50) NOT NULL,
    fecha_alta DATE NOT NULL
);

CREATE TABLE cuentas (
    cuenta_id INT PRIMARY KEY,
    cliente_id INT FOREIGN KEY REFERENCES clientes(cliente_id),
    tipo_cuenta VARCHAR(20) NOT NULL,
    saldo DECIMAL(18,2) NOT NULL
);

CREATE TABLE tarjetas_credito (
    tarjeta_id INT PRIMARY KEY,
    cliente_id INT FOREIGN KEY REFERENCES clientes(cliente_id),
    limite_credito DECIMAL(18,2) NOT NULL,
    estado_tarjeta VARCHAR(20) NOT NULL CHECK (estado_tarjeta IN ('ACTIVA', 'BLOQUEADA', 'CANCELADA'))
);

CREATE TABLE movimientos_cuenta (
    movimiento_id INT PRIMARY KEY,
    cuenta_id INT FOREIGN KEY REFERENCES cuentas(cuenta_id),
    fecha_movimiento DATETIME NOT NULL,
    tipo_movimiento VARCHAR(10) CHECK (tipo_movimiento IN ('DEBITO', 'CREDITO')),
    monto DECIMAL(18,2) NOT NULL
);

-- Poblado
INSERT INTO clientes VALUES 
(1, 'Carlos Benítez', 'Centro', '2023-05-10'),
(2, 'Ana Belén Gómez', 'Palermo', '2024-01-15'),
(3, 'Esteban Quito', 'Belgrano', '2025-06-20'),
(4, 'Lucía Méndez', 'Centro', '2026-02-10');

INSERT INTO cuentas VALUES 
(101, 1, 'CAJA_AHORRO', 450000.00),
(102, 1, 'CUENTA_CORRIENTE', 1200000.00),
(103, 2, 'CAJA_AHORRO', 85000.00),
(104, 3, 'CUENTA_CORRIENTE', 3200000.00);

INSERT INTO tarjetas_credito VALUES 
(501, 1, 1000000.00, 'ACTIVA'),
(502, 2, 300000.00, 'CANCELADA'),
(503, 4, 1500000.00, 'ACTIVA');

INSERT INTO movimientos_cuenta VALUES 
(9001, 101, '2026-08-01 10:30:00', 'CREDITO', 150000.00),
(9002, 101, '2026-08-05 14:15:00', 'DEBITO', 50000.00),
(9003, 102, '2026-08-03 09:00:00', 'DEBITO', 200000.00),
(9004, 104, '2026-08-09 18:20:00', 'CREDITO', 500000.00);


-- 2. REQUERIMIENTOS TÉCNICOS AVANZADOS
----------------------------------------------------------------------------

-- REQUERIMIENTO 1 (LEFT JOIN Correcto sin trampa WHERE):
-- Generar un reporte de TODOS los clientes, mostrando su saldo total en cuentas
-- y su límite de crédito de tarjetas ACTIVAS. Si el cliente no posee tarjeta activa,
-- debe figurar con límite de crédito 0 (usar COALESCE).
SELECT 
    c.cliente_id,
    c.nombre,
    c.sucursal_origen,
    COALESCE(SUM(ct.saldo), 0.00) AS saldo_total_cuentas,
    COALESCE(tc.limite_credito, 0.00) AS limite_tarjeta_activa
FROM clientes c
LEFT JOIN cuentas ct ON c.cliente_id = ct.cliente_id
-- NOTA CLAVE: El filtro por estado_tarjeta se coloca en la cláusula ON del LEFT JOIN para preservar el universo de clientes
LEFT JOIN tarjetas_credito tc ON c.cliente_id = tc.cliente_id AND tc.estado_tarjeta = 'ACTIVA'
GROUP BY c.cliente_id, c.nombre, c.sucursal_origen, tc.limite_credito;


-- REQUERIMIENTO 2 (Subquery y Agregaciones con HAVING):
-- Obtener las sucursales donde el promedio de saldo en Cuentas Corrientes sea superior
-- al saldo promedio general de todas las cuentas del banco.
SELECT 
    c.sucursal_origen,
    COUNT(ct.cuenta_id) AS total_cuentas_corrientes,
    AVG(ct.saldo) AS saldo_promedio_sucursal
FROM clientes c
INNER JOIN cuentas ct ON c.cliente_id = ct.cliente_id
WHERE ct.tipo_cuenta = 'CUENTA_CORRIENTE'
GROUP BY c.sucursal_origen
HAVING AVG(ct.saldo) > (SELECT AVG(saldo) FROM cuentas);


-- REQUERIMIENTO 3 (Creación de Vista Consolidada y Formateo de Fechas):
-- Crear una vista `vw_monitoreo_movimientos_recientes` que traiga los movimientos
-- de los últimos 30 días con la fecha formateada en formato argentino (DD/MM/YYYY)
-- y el número de cliente.
GO
CREATE VIEW vw_monitoreo_movimientos_recientes AS
SELECT 
    m.movimiento_id,
    c.cliente_id,
    c.nombre AS nombre_cliente,
    m.cuenta_id,
    m.tipo_movimiento,
    m.monto,
    CONVERT(VARCHAR(10), m.fecha_movimiento, 103) AS fecha_movimiento_fmt,
    DATEDIFF(day, m.fecha_movimiento, GETDATE()) AS dias_transcurridos
FROM movimientos_cuenta m
INNER JOIN cuentas ct ON m.cuenta_id = ct.cuenta_id
INNER JOIN clientes c ON ct.cliente_id = c.cliente_id
WHERE m.fecha_movimiento >= DATEADD(day, -30, GETDATE());
GO

-- Probar la vista creada
SELECT * FROM vw_monitoreo_movimientos_recientes;
