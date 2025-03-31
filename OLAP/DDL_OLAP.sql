 CREATE DATABASE DW_TALLERMECANICA


 USE DW_TALLERMECANICA;
 GO
-- Dimension Tiempo
create table dimtiempo (
   id_tiempo date primary key,
   anio      int,
   mes       int,
   dia       int,
   trimestre int
);

-- Subdimensiones TipoCliente y Genero
create table subdimtipocliente (
   id_tipo_cliente varchar(20) primary key
);

create table subdimgenero (
   id_genero varchar(10) primary key
);

-- Dimension Clientes
create table dimclientes (
   id_cliente      int primary key,
   nombre          varchar(100),
   id_tipo_cliente varchar(20),
   genero          varchar(10),
   estatus         varchar(20),
   foreign key ( id_tipo_cliente )
      references subdimtipocliente ( id_tipo_cliente ),
   foreign key ( genero )
      references subdimgenero ( id_genero )
);

create table subdimmarca (
   id_marca varchar(50) primary key
);

-- Dimension Vei�culos
create table dimvehiculos (
   id_vehiculo int primary key,
   id_marca    varchar(50),
   modelo      varchar(50),
   anio        int,
   foreign key ( id_marca )
      references subdimmarca ( id_marca )
);

-- Subdimensiones Puesto y Especializacion
create table subdimpuesto (
   id_puesto varchar(50) primary key
);

create table subdimespecializacion (
   id_especializacion varchar(100) primary key
);

-- Dimension Empleados
create table dimempleados (
   id_empleado     int primary key,
   nombre          varchar(100),
   puesto          varchar(50),
   turno           varchar(20),
   especializacion varchar(100),
   foreign key ( puesto )
      references subdimpuesto ( id_puesto ),
   foreign key ( especializacion )
      references subdimespecializacion ( id_especializacion )
);

-- Dimension Servicios
create table dimservicios (
   id_servicio    int primary key,
   descripcion    varchar(255),
   costo_unitario decimal(10,2)
);

-- Tabla de Hechos Ordenes de Servicio
create table hechosordenesservicio (
   id_orden           int primary key,
   id_tiempo          date,
   id_cliente         int,
   id_vehiculo        int,
   id_empleado        int,
   cantidad_servicios int,
   costo_total        decimal(10,2),
   foreign key ( id_tiempo )
      references dimtiempo ( id_tiempo ),
   foreign key ( id_cliente )
      references dimclientes ( id_cliente ),
   foreign key ( id_vehiculo )
      references dimvehiculos ( id_vehiculo ),
   foreign key ( id_empleado )
      references dimempleados ( id_empleado )
);

-- Tabla de Hechos Detalle de Servicios
create table hechosdetalleservicios (
   id_detalle  int primary key,
   id_orden    int,
   id_servicio int,
   cantidad    int,
   foreign key ( id_orden )
      references hechosordenesservicio ( id_orden ),
   foreign key ( id_servicio )
      references dimservicios ( id_servicio )
);