import oracledb
import pyodbc

##Conexion a la base de datos de SQLDeveloper
try:
    conexion= oracledb.connect(
    user= "C##_BD_TALLER_MECANICA",
    password= "1234",
    dsn= "localhost/xe")
    print("La conexion con SQL Developer ha sido exitosa")
except Exception as exDeveloper:
    print(exDeveloper)

##Conexion a la base de datos de SQLServer

try:
    connection= pyodbc.connect('DRIVER={SQL Server};SERVER=AMADORDESKTOP\SQLEXPRESS;DATABASE=DW_TALLERMECANICA;Trusted_Connection=yes')
    print("La conexion  con SQL Server ha sido exitosa")
except Exception as exServer:
    print(exServer)


    