-- Consulta 1


-- Consulta 2


-- Consulta 3
SELECT
    b.placa AS placa_bus,
    r.retraso_minutos AS retraso_original,
    r.retraso_minutos + 10 AS retraso_ajustado
FROM bus b
JOIN registro_control r
    ON b.id_bus = r.id_bus
WHERE r.retraso_minutos > 0;

-- Consulta 4
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