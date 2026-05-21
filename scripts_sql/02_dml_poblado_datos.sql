INSERT INTO centro_control (nombre , ubicacion, telefono, horario_operacion)
VALUES ("Centro Cayma", "Av Ejercito 001", "977211322", "6:00 AM - 10:00 PM"),

INSERT INTO pasajero (nombres, correo, telefono)
VALUES ("Adriano Guetat", "correoreal@dominioreal.com","986123543"),
-- tabla 1: EMPRESA_TRANSPORTE
INSERT INTO EMPRESA_TRANSPORTE (nombre, ruc, telefono, correo) VALUES
('SantaClara', '12345678901', '987654321', 'aqpbus@SantaClara.com'),

--tabla  2:TERMINAL
INSERT INTO TERMINAL (nombre, direccion, distrito, capacidad_buses) VALUES
('Terminal Norte', 'Av. Sol 123', 'Paucarpata', 40),

-- tabla conductor
INSERT INTO conductor(nombres, licencia, telefono, fecha_ingreso)
VALUES('Manuel Perez', 'Q32453286', '913653286', '2025-02-03');

--tabla paradero
INSERT INTO paradero(nombre, direccion, referencia)
VALUES('Paradero UNSA', 'Av. Independencia 500', 'Puerta principal de la UNSA');