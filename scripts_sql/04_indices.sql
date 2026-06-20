--  1. Pasajeros Sec Scan
EXPLAIN ANALYZE
SELECT *
FROM pasajero
WHERE correo = 'lucia.torres@mail.com';

-- Crear indice pasajero_correo
CREATE INDEX idx_pasajero_correo
ON pasajero(correo);

-- Pasajeros Index Scan
EXPLAIN ANALYZE
SELECT *
FROM pasajero
WHERE correo = 'lucia.torres@mail.com';

-- 2. Bus Sec Scan	
EXPLAIN ANALYZE
SELECT *
FROM bus
WHERE placa = 'V8A-123';

-- Crear indice bus_placa
CREATE INDEX idx_bus_placa
ON bus(placa);

-- Bus Index Scan
EXPLAIN ANALYZE
SELECT *
FROM bus
WHERE placa = 'V8A-123';

-- 3. Incidencias Sec Scan
EXPLAIN ANALYZE
SELECT *
FROM incidencia
WHERE tipo = 'Choque';

-- Crear indice incidencia_tipo
CREATE INDEX idx_incidencia_tipo
ON incidencia(tipo);

-- Incidencia Index Scan
EXPLAIN ANALYZE
SELECT *
FROM incidencia
WHERE tipo = 'Choque';