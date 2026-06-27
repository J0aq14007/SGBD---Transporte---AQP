EXPLAIN ANALYZE
SELECT *
FROM bus
WHERE placa = 'V8A-123';

CREATE INDEX idx_bus_placa
ON bus(placa);

EXPLAIN ANALYZE
SELECT *
FROM bus
WHERE placa = 'V8A-123';


EXPLAIN ANALYZE
SELECT *
FROM conductor
WHERE licencia = 'A99999999';

CREATE INDEX idx_conductor_licencia
ON conductor(licencia);

EXPLAIN ANALYZE
SELECT *
FROM conductor
WHERE licencia = 'A99999999';