--ANtes: Seq Scan on pasajero
EXPLAIN ANALYZE
SELECT *
FROM pasajero
WHERE dni = '12345678';

CREATE INDEX idx_pasajero_dni
ON pasajero(dni);
--Despues: Index Scan using idx_pasajero_dni
EXPLAIN ANALYZE
SELECT *
FROM pasajero
WHERE dni = '12345678';

--ANtes: Seq Scan on bus	
EXPLAIN ANALYZE
SELECT *
FROM bus
WHERE placa = 'ABC-123';

CREATE INDEX idx_bus_placa
ON bus(placa);
--Despues: Index Scan using idx_bus_placa
EXPLAIN ANALYZE
SELECT *
FROM bus
WHERE placa = 'ABC-123';

----ANtes: Seq Scan on viaje

EXPLAIN ANALYZE
SELECT *
FROM viaje
WHERE fecha_salida = '2026-06-01';

CREATE INDEX idx_viaje_fecha_salida
ON viaje(fecha_salida);
--Despues: Index Scan using idx_viaje_fecha_salida
EXPLAIN ANALYZE
SELECT *
FROM viaje
WHERE fecha_salida = '2026-06-01';
