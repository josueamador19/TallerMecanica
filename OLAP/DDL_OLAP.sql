CREATE DATABASE DW_TALLERMECANICA
GO
USE DW_TALLERMECANICA
GO
 
-- Dimension Tiempo
CREATE TABLE DIMTIEMPO (
    ID_TIEMPO INT PRIMARY KEY,
    ANIO INT,
    MES INT,
    DIA INT,
    TRIMESTRE INT
);

-- Subdimensiones TipoCliente y Genero
CREATE TABLE SUBDIMTIPOCLIENTE (
    ID_TIPO_CLIENTE INT PRIMARY KEY,
    DESCRIPCION VARCHAR(20)
);

CREATE TABLE SUBDIMGENERO (
    ID_GENERO INT PRIMARY KEY,
    DESCRIPCION VARCHAR(10)
);

-- Dimension Clientes
CREATE TABLE DIMCLIENTES (
    ID_CLIENTE INT PRIMARY KEY,
    NOMBRE VARCHAR(100),
    ID_TIPO_CLIENTE INT,
    ID_GENERO INT,
    ESTATUS VARCHAR(20),
    FOREIGN KEY (ID_TIPO_CLIENTE) REFERENCES SUBDIMTIPOCLIENTE(ID_TIPO_CLIENTE),
    FOREIGN KEY (ID_GENERO) REFERENCES SUBDIMGENERO(ID_GENERO)
);

CREATE TABLE SUBDIMMARCA (
    ID_MARCA INT PRIMARY KEY,
    DESCRIPCION VARCHAR(50)
);

-- Dimension Vei�culos
CREATE TABLE DIMVEHICULOS (
    ID_VEHICULO INT PRIMARY KEY,
    ID_MARCA INT,
    MODELO VARCHAR(50),
    ANIO INT,
    FOREIGN KEY (ID_MARCA) REFERENCES SUBDIMMARCA(ID_MARCA)
);

-- Subdimensiones Puesto y Especializacion
CREATE TABLE SUBDIMPUESTO (
    ID_PUESTO INT PRIMARY KEY,
    DESCRIPCION VARCHAR(50)
);

CREATE TABLE SUBDIMESPECIALIZACION (
    ID_ESPECIALIZACION INT PRIMARY KEY,
    DESCRIPCION VARCHAR(100)
);

-- Dimension Empleados
CREATE TABLE DIMEMPLEADOS (
    ID_EMPLEADO INT PRIMARY KEY,
    NOMBRE VARCHAR(100),
    ID_PUESTO INT,
    TURNO VARCHAR(20),
    ID_ESPECIALIZACION INT,
    FOREIGN KEY (ID_PUESTO) REFERENCES SUBDIMPUESTO(ID_PUESTO),
    FOREIGN KEY (ID_ESPECIALIZACION) REFERENCES SUBDIMESPECIALIZACION(ID_ESPECIALIZACION)
);

-- Dimension Servicios
CREATE TABLE DIMSERVICIOS (
    ID_SERVICIO INT PRIMARY KEY,
    DESCRIPCION VARCHAR(255),
    COSTO_UNITARIO DECIMAL(10, 2)
);

-- Tabla de Hechos Ordenes de Servicio
CREATE TABLE HECHOSORDENESSERVICIO (
    ID_ORDEN INT PRIMARY KEY,
    ID_TIEMPO INT,
    ID_CLIENTE INT,
    ID_VEHICULO INT,
    ID_EMPLEADO INT,
    CANTIDAD_SERVICIOS INT,
    COSTO_TOTAL DECIMAL(10, 2),
    FOREIGN KEY (ID_TIEMPO) REFERENCES DIMTIEMPO(ID_TIEMPO),
    FOREIGN KEY (ID_CLIENTE) REFERENCES DIMCLIENTES(ID_CLIENTE),
    FOREIGN KEY (ID_VEHICULO) REFERENCES DIMVEHICULOS(ID_VEHICULO),
    FOREIGN KEY (ID_EMPLEADO) REFERENCES DIMEMPLEADOS(ID_EMPLEADO)
);

-- Tabla de Hechos Detalle de Servicios
CREATE TABLE HECHOSDETALLESERVICIOS (
    ID_DETALLE INT PRIMARY KEY,
    ID_ORDEN INT,
    ID_SERVICIO INT,
    CANTIDAD INT,
    FOREIGN KEY (ID_ORDEN) REFERENCES HECHOSORDENESSERVICIO(ID_ORDEN),
    FOREIGN KEY (ID_SERVICIO) REFERENCES DIMSERVICIOS(ID_SERVICIO)
);