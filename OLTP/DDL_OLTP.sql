--DDL

-- Tabla de Clientes
CREATE TABLE Clientes (
    id_cliente NUMBER PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    fecha_registro DATE DEFAULT SYSDATE,
    tipo_cliente VARCHAR2(20) CHECK (tipo_cliente IN ('Particular', 'Empresa')),
    genero CHAR(1) CHECK (genero IN ('M', 'F', 'O')),
    fecha_nacimiento DATE,
    estatus VARCHAR2(20) CHECK (estatus IN ('Activo', 'Inactivo'))
);

-- Tabla de Vehículos
CREATE TABLE Vehiculos (
    id_vehiculo NUMBER PRIMARY KEY,
    id_cliente NUMBER NOT NULL,
    marca VARCHAR2(50) NOT NULL,
    modelo VARCHAR2(50) NOT NULL,
    anio NUMBER(4) NOT NULL,
    placa VARCHAR2(15) UNIQUE NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE
);

-- Tabla de Empleados
CREATE TABLE Empleados (
    id_empleado NUMBER PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    puesto VARCHAR2(50) NOT NULL,
    fecha_contratacion DATE,
    salario NUMBER(10, 2),
    turno VARCHAR2(20) CHECK (turno IN ('Mañana', 'Tarde', 'Noche')),
    especializacion VARCHAR2(100),
    estatus VARCHAR2(20) CHECK (estatus IN ('Activo', 'Inactivo'))
);

-- Tabla de Contactos (para Clientes y Empleados)
CREATE TABLE Contactos (
    id_contacto NUMBER PRIMARY KEY,
    telefono VARCHAR2(15),
    correo VARCHAR2(100),
    direccion VARCHAR2(255)
);

-- Relación Contacto-Cliente
CREATE TABLE Cliente_Contacto (
    id_cliente NUMBER NOT NULL,
    id_contacto NUMBER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_contacto) REFERENCES Contactos(id_contacto) ON DELETE CASCADE
);

-- Relación Contacto-Empleado
CREATE TABLE Empleado_Contacto (
    id_empleado NUMBER NOT NULL,
    id_contacto NUMBER NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (id_contacto) REFERENCES Contactos(id_contacto) ON DELETE CASCADE
);

-- Tabla de Ordenes de Servicio 
CREATE TABLE Ordenes_Servicio (
    id_orden NUMBER PRIMARY KEY,
    id_vehiculo NUMBER NOT NULL,
    fecha_recepcion DATE DEFAULT SYSDATE,
    id_cliente NUMBER NOT NULL,
    id_empleado NUMBER,
    tipo_orden VARCHAR2(50) CHECK (tipo_orden IN ('Mantenimiento', 'Reparación', 'Diagnóstico')),
    prioridad VARCHAR2(20) CHECK (prioridad IN ('Alta', 'Media', 'Baja')),
    estado VARCHAR2(20) CHECK (estado IN ('Pendiente', 'En Proceso', 'Completado', 'Cancelado')),
    FOREIGN KEY (id_vehiculo) REFERENCES Vehiculos(id_vehiculo) ON DELETE CASCADE,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE
);

-- Tabla de Servicios
CREATE TABLE Servicios (
    id_servicio NUMBER PRIMARY KEY,
    descripcion VARCHAR2(255) NOT NULL,
    costo NUMBER(10,2) NOT NULL
);

-- Detalle de Servicios
CREATE TABLE Detalle_Servicio (
    id_detalle NUMBER PRIMARY KEY,
    id_orden NUMBER NOT NULL,
    id_servicio NUMBER NOT NULL,
    cantidad NUMBER DEFAULT 1 NOT NULL,
    FOREIGN KEY (id_orden) REFERENCES Ordenes_Servicio(id_orden) ON DELETE CASCADE,
    FOREIGN KEY (id_servicio) REFERENCES Servicios(id_servicio) ON DELETE CASCADE
);

-- Tabla de Facturas
CREATE TABLE Facturas (
    id_factura NUMBER PRIMARY KEY,
    id_orden NUMBER NOT NULL,
    fecha_emision DATE DEFAULT SYSDATE,
    total NUMBER(10,2) NOT NULL,
    FOREIGN KEY (id_orden) REFERENCES Ordenes_Servicio(id_orden) ON DELETE CASCADE
);





