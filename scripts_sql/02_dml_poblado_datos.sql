-- #TABLAS INDEPENDIENTES

-- tabla  EMPRESA_TRANSPORTE
INSERT INTO empresa_transporte(nombre, ruc, telefono, correo) 
VALUES  ('SantaClara', '12345678901', '987654321', 'aqpbus@SantaClara.com'),
        ('AQPMasivo', '10987654321', '912345678', 'aqpbus@AQPmasivo.com'),
        ('LosCanarios', '10293847561', '987321654', 'aqpbus@loscanarios.com'),
        ('Graficos', '11223344556', '999888777', 'aqpbus@GraficosSA.com'),
        ('Cotum', '11987654321', '955443322', 'aqpbus@Cotum.com');


--tabla  TERMINAL
INSERT INTO terminal(nombre, direccion, distrito, capacidad_buses) 
VALUES  ('Terminal Norte', 'Av. Sol 123', 'Paucarpata', 40),
        ('Terminal Sur', 'Av. Los Incas 456', 'José Luis Bustamante', 50),
        ('Terminal Centro', 'Av. La Marina 789', 'Cercado', 30),
        ('Terminal Este', 'Av. Lima 321', 'Mariano Melgar', 35),
        ('Terminal Oeste', 'Av. Libertad 654', 'Cayma', 50);


--tabla centro_control
INSERT INTO centro_control (nombre , ubicacion, telefono, horario_operacion)
VALUES  ('Centro Cayma', 'Av Ejercito 001', '977211322', '6:00 AM - 10:00 PM'),
        ('Centro Paucarpata', 'Av. Dolores 222', '988112233', '7:00 AM - 9:00 PM'),
        ('Centro Cercado', 'Av. Goyeneche 333', '977445566', '24 horas'),
        ('Centro Socabaya', 'Av. Socabaya 444', '966778899', '5:00 AM - 11:00 PM'),
        ('Centro Yanahuara', 'Av. Yanahuara 555', '955667788', '8:00 AM - 8:00 PM');



--tabla pasajero
INSERT INTO pasajero (nombres, correo, telefono)
VALUES  ('Adriano Guetat', 'correoreal@dominioreal.com','986123543'),
        ('Lucía Torres', 'lucia.torres@mail.com','987654321'),
        ('Carlos Díaz', 'carlos.diaz@mail.com','912345678'),
        ('María López', 'maria.lopez@mail.com','933221144'),
        ('José Ramos', 'jose.ramos@mail.com','955667788');


--tabla conductor
INSERT INTO conductor(nombres, licencia, telefono, fecha_ingreso)
VALUES  ('Manuel Perez', 'Q32453286', '913653286', '2025-02-03'),
        ('Luis Torres', 'L12345678', '987654321', '2024-05-10'),
        ('Anuel Gómez', 'A87654321', '912345678', '2023-11-20'),
        ('Pedro Ramos', 'P11223344', '933221144', '2022-07-15'),
        ('Santiago Díaz', 'S55667788', '955667788', '2021-03-01');


--tabla paradero
INSERT INTO paradero(nombre, direccion, referencia)
VALUES  ('Paradero UNSA', 'Av. Independencia 500', 'Puerta principal de la UNSA'),
        ('Paradero PlazaVea', 'Av. Ejército 200', 'Frente a Plaza Vea Cayma'),
        ('Paradero Mall', 'Av. Kennedy 300', 'Entrada principal del Mall Aventura'),
        ('Paradero Estadio', 'Av. Independencia 400', 'Frente al Estadio Melgar'),
        ('Paradero Hospital', 'Av. Goyeneche 600', 'Entrada principal del Hospital Goyeneche');


-- #TABLAS DEPENDIENTES

--tabla ruta
INSERT INTO ruta(nombre_ruta, codigo_ruta, tiempo_estimado, id_empresa)
VALUES  ('Ruta Centro - Cayma', 'R001', 45, 1),
        ('Ruta Paucarpata - Cercado', 'R002', 35, 2),
        ('Ruta Yanahuara - Socabaya', 'R003', 50, 3),
        ('Ruta Mariano Melgar - Centro', 'R004', 40, 4),
        ('Ruta Cerro Colorado - UNSA', 'R005', 55, 5);

--tabla bus
INSERT INTO bus(placa, capacidad, estado, id_empresa, id_terminal)
VALUES  ('V8A-123', 40, 'Activo', 1, 1),
        ('C7B-456', 35, 'Activo', 2, 2),
        ('M9D-789', 50, 'Mantenimiento', 3, 3),
        ('P1F-321', 45, 'Activo', 4, 4),
        ('X5G-654', 30, 'Inactivo', 5, 5);

--tabla horario
INSERT INTO horario(hora_salida, hora_llegada, frecuencia, id_ruta)
VALUES  ('06:00', '06:45', '15 minutes', 1),
        ('07:00', '07:35', '20 minutes', 2),
        ('08:00', '08:50', '25 minutes', 3),
        ('09:00', '09:40', '30 minutes', 4),
        ('10:00', '10:55', '15 minutes', 5);

--tabla notificacion
INSERT INTO notificacion(id_centro, id_pasajero, mensaje, fecha_envio, tipo)
VALUES  (1, 1, 'Retraso en la ruta R001', '2026-05-20 08:30:00', 'Retraso'),
        (2, 2, 'Desvío temporal por tráfico', '2026-05-20 09:00:00', 'Aviso'),
        (3, 3, 'Ruta restablecida', '2026-05-20 09:30:00', 'Informativo'),
        (4, 4, 'Cambio de horario', '2026-05-20 10:00:00', 'Horario'),
        (5, 5, 'Bus fuera de servicio', '2026-05-20 11:00:00', 'Incidencia');

--tabla asignacion conductor
INSERT INTO asignacion_conductor(fecha_asignacion,turno,estado,id_conductor,id_bus)
VALUES  ('2026-05-22', 'Mañana', 'Vigente',1,1),
        ('2026-05-22', 'Tarde', 'Vigente',2,2),
        ('2026-05-23', 'Mañana', 'Vigente',3,3),
        ('2026-05-23', 'Tarde', 'Vigente',4,4),
        ('2026-05-23', 'Mañana', 'Vigente',5,5);

--tabla incidencia
INSERT INTO incidencia(id_bus,id_centro,id_pasajero,descripcion,tipo,fecha_reporte)
VALUES  (1,1,1,'El bus x llego tarde hoy, tenia cosas importantes que hacer', 'Retraso', '2026-05-20 15:36:00'),
        (2,2,2,'El conductor del bus x conduce muy rapido', 'Exceso de velocidad', '2026-05-21 11:16:00'),
        (3,3,3,'El bus x no parece recibir mantenimiento', 'Bus en mal estado', '2026-05-21 08:10:00'),
        (4,4,4,'El conductor del bus x parecia estar en estado de ebriedad', 'Conductor en mal estado', '2026-05-23 10:50:00'),
        (5,5,5,'El bus x choco en la avenida x', 'Choque', '2026-05-20 15:36:00');

--tabla registro_control
INSERT INTO registro_control(id_bus,id_centro,fecha_hora,retraso_minutos,observacion)
VALUES  (1,1,'2026-05-20 06:59:00',-1, 'Llego temprano'),
        (2,2,'2026-05-20 08:15:00',15, 'Se retraso por el trafico'),
        (3,3,'2026-05-21 10:20:00',20, 'Se retraso por el cambio de ruta'),
        (4,4,'2026-05-21 12:00:00',0, 'Llego a tiempo'),
        (5,5,'2026-05-22 19:00:00',120, 'Choco y tuvo que regresar a la base');


-- #UPDATE Y WHERE DE TABLAS
--UPDATE'S DE EMPRESA_TRANSPORTE
UPDATE empresa_transporte 
SET telefono = '900111222' 
WHERE nombre = 'SantaClara';

UPDATE empresa_transporte 
SET correo = 'contacto@aqpmasivo.com' 
WHERE nombre = 'AQPMasivo';

UPDATE empresa_transporte 
SET ruc = '12312312312' 
WHERE nombre = 'LosCanarios';

--UPDATE'S DE  PASAJERO
UPDATE pasajero 
SET telefono = '999888777' 
WHERE nombres = 'Lucía Torres';

UPDATE pasajero 
SET correo = 'carlos.diaz@update.com' 
WHERE nombres = 'Carlos Díaz';

UPDATE pasajero 
SET nombres = 'María López García' 
WHERE correo = 'maria.lopez@mail.com';

--UPDATE'S DE  CONDUCTOR
UPDATE conductor 
SET telefono = '911222333' 
WHERE nombres = 'Manuel Perez';

UPDATE conductor 
SET fecha_ingreso = '2025-05-01' 
WHERE nombres = 'Luis Torres';

UPDATE conductor 
SET licencia = 'A99999999' 
WHERE nombres = 'Anuel Gómez';

--UPDATE'S DE BUS
UPDATE bus
SET estado = 'Mantenimiento'
WHERE placa = 'V8A-123';

UPDATE bus
SET capacidad = 45
WHERE id_bus = 2;

UPDATE bus
SET id_terminal = 3
WHERE placa = 'M9D-789';



