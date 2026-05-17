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
        CONSTRAINT pk_cntr_cntrl_id_cntr PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    horario_operacion VARCHAR(19) NOT NULL,
);

--tabla pasajero (Independinte)
CREATE TABLE pasajero (
    id_pasajero SERIAL
        CONSTRAINT pk_psjr_id_psjr PRIMARY KEY,
    nombres VARCHAR(50) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NOT,
);