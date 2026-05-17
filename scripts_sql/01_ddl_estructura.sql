CREATE DATABASE SISTEMA_DE_GESTION_DE_TRANSPORTE_AQP;
USE  SISTEMA_DE_GESTION_DE_TRANSPORTE_AQP;


-- tabla EMPRESA_TRANSPORTE (Independiente)
CREATE TABLE EMPRESA_TRANSPORTE (
    id_empresa INT,
    nombre VARCHAR(100) NOT NULL,
    ruc CHAR(11) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(100),
    PRIMARY KEY (id_empresa),
    CONSTRAINT UK_empresa_ruc UNIQUE (ruc)
);

--tabla TERMINAL(Independiente)
CREATE TABLE TERMINAL (
    id_terminal INT,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    distrito VARCHAR(100) NOT NULL,
    capacidad_buses INT,
    PRIMARY KEY (id_terminal)
);

-- tabla BUS (Depende de EMPRESA_TRANSPORTE y TERMINAL)
CREATE TABLE BUS (
    id_bus INT,
    placa CHAR(7) NOT NULL,
    capacidad INT NOT NULL,
    estado VARCHAR(20) NOT NULL,
    id_empresa INT,
    id_terminal INT,
    PRIMARY KEY (id_bus),
    CONSTRAINT UK_bus_placa UNIQUE (placa),
    CONSTRAINT FK_bus_empresa FOREIGN KEY (id_empresa) 
        REFERENCES EMPRESA_TRANSPORTE(id_empresa),
    CONSTRAINT FK_bus_terminal FOREIGN KEY (id_terminal) 
        REFERENCES TERMINAL(id_terminal)
);

--tabla UBICACION_BUS (Depende de BUS)
CREATE TABLE UBICACION_BUS (
    id_ubicacion INT ,
    latitud DECIMAL(9,6) NOT NULL,
    longitud DECIMAL(9,6) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    id_bus INT,
    PRIMARY KEY (id_ubicacion),
    CONSTRAINT FK_ubicacion_bus FOREIGN KEY (id_bus) 
        REFERENCES BUS(id_bus)
);

--tabla RUTA (Depende de EMPRESA_TRANSPORTE)
CREATE TABLE RUTA (
    id_ruta INT,
    nombre_ruta VARCHAR(100) NOT NULL,
    codigo_ruta VARCHAR(10) NOT NULL,
    tiempo_estimado INT, 
    id_empresa INT,
    PRIMARY KEY (id_ruta),
    CONSTRAINT UK_ruta_codigo UNIQUE (codigo_ruta),
    CONSTRAINT FK_ruta_empresa FOREIGN KEY (id_empresa) 
        REFERENCES EMPRESA_TRANSPORTE(id_empresa)
);

--tabla centro_control (Independiente)
CREATE TABLE centro_control (
    id_centro SMALLSERIAL
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    horario_operacion VARCHAR(19) NOT NULL,
    PRIMARY KEY (id_centro),

);

-- tabla conductor (Independiente)
CREATE TABLE conductor (
    id_conductor SMALLSERIAL,
    nombres VARCHAR(100) NOT NULL,
    licencia VARCHAR(20) NOT NULL,
    telefono VARCHAR(15),
    fecha_ingreso DATE NOT NULL,
    PRIMARY KEY (id_conductor),
    CONSTRAINT uk_conductor_licencia UNIQUE (licencia)
);

-- tabla paradero (Independiente)
CREATE TABLE paradero (
    id_paradero SMALLSERIAL,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    referencia VARCHAR(200),
    PRIMARY KEY (id_paradero)
);

-- tabla recorrido_ruta (Depende de ruta y paradero)
CREATE TABLE recorrido_ruta (
    id_recorrido SMALLSERIAL,
    orden_paradero INT NOT NULL,
    tiempo_llegada_estimado INTERVAL,
    id_ruta INT NOT NULL,
    id_paradero INT NOT NULL,
    PRIMARY KEY (id_recorrido),
    CONSTRAINT fk_recorrido_ruta
        FOREIGN KEY (id_ruta)
        REFERENCES ruta(id_ruta),
    CONSTRAINT fk_recorrido_paradero
        FOREIGN KEY (id_paradero)
        REFERENCES paradero(id_paradero)
);

-- tabla horario (Depende de ruta)
CREATE TABLE horario (
    id_horario SMALLSERIAL,
    hora_salida TIME NOT NULL,
    hora_llegada TIME NOT NULL,
    frecuencia INTERVAL,
    id_ruta INT NOT NULL,
    PRIMARY KEY (id_horario),
    CONSTRAINT fk_horario_ruta
        FOREIGN KEY (id_ruta)
        REFERENCES ruta(id_ruta)
);