-- Consulta 1
-- Lista los conductores que han tenido más o una asignación, ordenados por cantidad.
SELECT
    c.nombres AS nombre_conductor,
    COUNT(ac.id_asignacion) AS total_asignaciones
FROM conductor c
JOIN asignacion_conductor ac
    ON c.id_conductor = ac.id_conductor
GROUP BY c.nombres
HAVING COUNT(ac.id_asignacion) >= 1
ORDER BY total_asignaciones DESC;


-- Consulta 2
--Muestra los tipos de incidencias que se repiten al menos una vez, 
--ordenados de mayor a menor frecuencia.
SELECT
    i.tipo AS tipo_incidencia,
    COUNT(i.id_incidencia) AS total_reportes
FROM incidencia i
GROUP BY i.tipo
HAVING COUNT(i.id_incidencia) >= 1
ORDER BY total_reportes DESC;

-- Consulta 3
-- Muestra los buses con retraso y calcula un retraso ajustado sumando 10 minutos
SELECT
    b.placa AS placa_bus,
    r.retraso_minutos AS retraso_original,
    r.retraso_minutos + 10 AS retraso_ajustado
FROM bus b
JOIN registro_control r
    ON b.id_bus = r.id_bus
WHERE r.retraso_minutos > 0;

-- Consulta 4
-- Muestra las incidencias y el promedio de retrasos por empresa de transporte
SELECT
    e.nombre AS empresa,
    COUNT(i.id_incidencia) AS total_incidencias,
    AVG(rc.retraso_minutos) AS promedio_retraso
FROM empresa_transporte e
JOIN bus b
    ON e.id_empresa = b.id_empresa
JOIN incidencia i
    ON b.id_bus = i.id_bus
JOIN registro_control rc
    ON b.id_bus = rc.id_bus
GROUP BY e.nombre
HAVING COUNT(i.id_incidencia) >= 1
ORDER BY total_incidencias DESC;
