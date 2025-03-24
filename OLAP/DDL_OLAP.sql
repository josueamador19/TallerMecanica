USE DW_TallerMecanica
GO



-- Dimension Tiempo
CREATE TABLE DimTiempo (
    id_tiempo INT PRIMARY KEY,
    anio INT,
    mes INT,
    dia INT,
    trimestre INT
);


-- Subdimensiones TipoCliente y Genero
CREATE TABLE SubDimTipoCliente (
    id_tipo_cliente INT PRIMARY KEY,
    descripcion VARCHAR(20)
);

CREATE TABLE SubDimGenero (
    id_genero INT PRIMARY KEY,
    descripcion VARCHAR(10)
);

-- Dimension Clientes
CREATE TABLE DimClientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100),
    id_tipo_cliente INT,
    id_genero INT,
    estatus VARCHAR(20),
    FOREIGN KEY (id_tipo_cliente) REFERENCES SubDimTipoCliente(id_tipo_cliente),
    FOREIGN KEY (id_genero) REFERENCES SubDimGenero(id_genero)
);


CREATE TABLE SubDimMarca (
    id_marca INT PRIMARY KEY,
    descripcion VARCHAR(50)
);
-- Dimension Veiículos
CREATE TABLE DimVehiculos (
    id_vehiculo INT PRIMARY KEY,
    id_marca INT,
    modelo VARCHAR(50),
    anio INT,
    FOREIGN KEY (id_marca) REFERENCES SubDimMarca(id_marca)
);
-- Subdimensiones Puesto y Especializacion
CREATE TABLE SubDimPuesto (
    id_puesto INT PRIMARY KEY,
    descripcion VARCHAR(50)
);

CREATE TABLE SubDimEspecializacion (
    id_especializacion INT PRIMARY KEY,
    descripcion VARCHAR(100)
);


-- Dimension Empleados
CREATE TABLE DimEmpleados (
    id_empleado INT PRIMARY KEY,
    nombre VARCHAR(100),
    id_puesto INT,
    turno VARCHAR(20),
    id_especializacion INT,
    FOREIGN KEY (id_puesto) REFERENCES SubDimPuesto(id_puesto),
    FOREIGN KEY (id_especializacion) REFERENCES SubDimEspecializacion(id_especializacion)
);


-- Dimension Servicios
CREATE TABLE DimServicios (
    id_servicio INT PRIMARY KEY,
    descripcion VARCHAR(255),
    costo_unitario DECIMAL(10, 2)
);

-- Tabla de Hechos Ordenes de Servicio
CREATE TABLE HechosOrdenesServicio (
    id_orden INT PRIMARY KEY,
    id_tiempo INT,
    id_cliente INT,
    id_vehiculo INT,
    id_empleado INT,
    cantidad_servicios INT,
    costo_total DECIMAL(10, 2),
    FOREIGN KEY (id_tiempo) REFERENCES DimTiempo(id_tiempo),
    FOREIGN KEY (id_cliente) REFERENCES DimClientes(id_cliente),
    FOREIGN KEY (id_vehiculo) REFERENCES DimVehiculos(id_vehiculo),
    FOREIGN KEY (id_empleado) REFERENCES DimEmpleados(id_empleado)
);

-- Tabla de Hechos Detalle de Servicios
CREATE TABLE HechosDetalleServicios (
    id_detalle INT PRIMARY KEY,
    id_orden INT,
    id_servicio INT,
    cantidad INT,
    FOREIGN KEY (id_orden) REFERENCES HechosOrdenesServicio(id_orden),
    FOREIGN KEY (id_servicio) REFERENCES DimServicios(id_servicio)
);
