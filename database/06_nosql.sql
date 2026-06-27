CREATE TABLE rutas_postgres (
    id SERIAL PRIMARY KEY,
    nombre_ruta VARCHAR(100) NOT NULL,
    codigo_ruta VARCHAR(10) NOT NULL,
    informacion JSONB
);

INSERT INTO rutas_postgres
(nombre_ruta, codigo_ruta, informacion)
VALUES
(
    'Ruta Centro - Cayma',
    'R001',
    '{
        "hora_salida":"06:00",
        "hora_llegada":"06:45",
        "frecuencia":"15 minutes",
        "tiempo_estimado":45
    }'
);

INSERT INTO rutas_postgres
(nombre_ruta, codigo_ruta, informacion)
VALUES
(
    'Ruta Paucarpata - Cercado',
    'R002',
    '{
        "hora_salida":"07:00",
        "hora_llegada":"07:35",
        "frecuencia":"20 minutes",
        "tiempo_estimado":35
    }'
);

INSERT INTO rutas_postgres
(nombre_ruta, codigo_ruta, informacion)
VALUES
(
    'Ruta Yanahuara - Socabaya',
    'R003',
    '{
        "hora_salida":"08:00",
        "hora_llegada":"08:50",
        "frecuencia":"25 minutes",
        "tiempo_estimado":50
    }'
);

SELECT
    nombre_ruta,
    informacion->>'hora_salida' AS hora_salida,
    informacion->>'hora_llegada' AS hora_llegada,
    informacion->>'frecuencia' AS frecuencia
FROM rutas_postgres;

SELECT *
FROM rutas_postgres
WHERE informacion->>'hora_salida' = '06:00';

SELECT *
FROM rutas_postgres
WHERE (informacion->>'tiempo_estimado')::INTEGER > 40;

-- En el modelo relacional la información de las rutas y sus horarios
-- se almacena en tablas separadas (RUTA y HORARIO), por lo que se
-- requiere un JOIN para consultar los datos completos.

-- En el modelo documental utilizando JSONB, los datos del horario se
-- almacenan dentro del mismo registro de la ruta, permitiendo obtener
-- toda la información mediante una sola consulta.

-- Además, si en el futuro se requiere agregar nuevas propiedades como
-- "tipo_servicio", "dias_operacion" o "color_ruta", estas pueden
-- incorporarse al documento JSON sin modificar la estructura de la
-- tabla ni crear nuevas relaciones. 