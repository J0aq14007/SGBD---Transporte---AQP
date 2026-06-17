-- Transaccion 1: la empresa y su bus se registren juntos. Si falla uno, no se guarda nada.
BEGIN;

INSERT INTO empresa_transporte (nombre, ruc, telefono, correo)
VALUES ('Transporte Andino', '12398745600', '987111222', 'contacto@andino.com');

INSERT INTO bus (placa, capacidad, estado, id_empresa, id_terminal)
VALUES ('Z9H-111', 40, 'Activo', currval('empresa_transporte_id_empresa_seq'), 1);

COMMIT;

--Transaccion 2: Se asigna un conductor y se actualiza el estado del bus en la misma operación.
BEGIN;

INSERT INTO asignacion_conductor (fecha_asignacion, turno, estado, id_conductor, id_bus)
VALUES ('2026-06-17', 'Mañana', 'Vigente', 2, 1);

UPDATE bus
SET estado = 'En servicio'
WHERE id_bus = 1;

COMMIT;

--Transaccion 3: Se registra la incidencia y se envía notificación al pasajero en la misma transacción.
BEGIN;

INSERT INTO incidencia (id_bus, id_centro, id_pasajero, descripcion, tipo, fecha_reporte)
VALUES (2, 2, 3, 'El bus tuvo un desperfecto mecánico', 'Bus en mal estado', NOW());

INSERT INTO notificacion (id_centro, id_pasajero, mensaje, fecha_envio, tipo)
VALUES (2, 3, 'Se reportó un desperfecto mecánico en su bus', NOW(), 'Incidencia');

COMMIT;

--Transaccion 4 (mas compleja): 
--Actualiza el tiempo estimado de la ruta R002.
--Inserta un nuevo horario asociado a esa ruta.
--Envía una notificación a un pasajero informando del cambio.

BEGIN;

-- Actualizar tiempo estimado de la ruta
UPDATE ruta
SET tiempo_estimado = 60
WHERE codigo_ruta = 'R002';

-- Insertar nuevo horario para la ruta actualizada
INSERT INTO horario (hora_salida, hora_llegada, frecuencia, id_ruta)
VALUES ('11:00', '12:00', INTERVAL '20 minutes', 
        (SELECT id_ruta FROM ruta WHERE codigo_ruta = 'R002'));

-- Registrar notificación a un pasajero sobre el cambio
INSERT INTO notificacion (id_centro, id_pasajero, mensaje, fecha_envio, tipo)
VALUES (2, 2, 'La ruta R002 ha sido reprogramada con nuevo horario', NOW(), 'Horario');

COMMIT;


