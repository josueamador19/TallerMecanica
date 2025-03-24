import oracledb


##Conexion a la base de datos de SQLDeveloper
conexion= oracledb.connect(
    user= "C##_BD_TALLER_MECANICA",
    password= "1234",
    dsn= "localhost/xe"
)

