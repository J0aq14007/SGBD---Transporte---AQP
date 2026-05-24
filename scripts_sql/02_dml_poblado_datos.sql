
-- tabla  EMPRESA_TRANSPORTE
INSERT INTO empresa_transporte(nombre, ruc, telefono, correo) VALUES
('SantaClara', '12345678901', '987654321', 'aqpbus@SantaClara.com'),
('AQPMasivo', '10987654321', '912345678', 'aqpbus@AQPmasivo.com'),
('LosCanarios', '10293847561', '987321654', 'aqpbus@loscanarios.com'),
('Graficos', '11223344556', '999888777', 'aqpbus@GraficosSA.com'),
('Cotum', '11987654321', '955443322', 'aqpbus@Cotum.com');


--tabla  TERMINAL
INSERT INTO terminal(nombre, direccion, distrito, capacidad_buses) VALUES
('Terminal Norte', 'Av. Sol 123', 'Paucarpata', 40),
('Terminal Sur', 'Av. Los Incas 456', 'José Luis Bustamante', 50),
('Terminal Centro', 'Av. La Marina 789', 'Cercado', 30),
('Terminal Este', 'Av. Lima 321', 'Mariano Melgar', 35),
('Terminal Oeste', 'Av. Libertad 654', 'Cayma', 50);


--tabla centro_control
INSERT INTO centro_control (nombre , ubicacion, telefono, horario_operacion)
VALUES ('Centro Cayma', 'Av Ejercito 001', '977211322', '6:00 AM - 10:00 PM'),
('Centro Paucarpata', 'Av. Dolores 222', '988112233', '7:00 AM - 9:00 PM'),
('Centro Cercado', 'Av. Goyeneche 333', '977445566', '24 horas'),
('Centro Socabaya', 'Av. Socabaya 444', '966778899', '5:00 AM - 11:00 PM'),
('Centro Yanahuara', 'Av. Yanahuara 555', '955667788', '8:00 AM - 8:00 PM');



--tabla pasajero
INSERT INTO pasajero (nombres, correo, telefono)
VALUES ('Adriano Guetat', 'correoreal@dominioreal.com','986123543'),
('Lucía Torres', 'lucia.torres@mail.com','987654321'),
('Carlos Díaz', 'carlos.diaz@mail.com','912345678'),
('María López', 'maria.lopez@mail.com','933221144'),
('José Ramos', 'jose.ramos@mail.com','955667788');


--tabla conductor
INSERT INTO conductor(nombres, licencia, telefono, fecha_ingreso)
VALUES('Manuel Perez', 'Q32453286', '913653286', '2025-02-03');


--tabla paradero
INSERT INTO paradero(nombre, direccion, referencia)
VALUES('Paradero UNSA', 'Av. Independencia 500', 'Puerta principal de la UNSA');
