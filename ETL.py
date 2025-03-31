from tkinter import *
from tkinter import ttk,simpledialog,messagebox
import oracledb
import pyodbc
import pandas as pd
import numpy as np

conn_oltp = None
conn_olap = None
"""pensadas para etl"""
datos_antes_filtro_e = None
datos_despues_filtro_e = None
datos_despues_filtro_t = None

def get_credentials():
        user = simpledialog.askstring("Acceso a Oracle", "Usuario:")
        if user is None: return None, None  
        
        password = simpledialog.askstring("Acceso a Oracle", "Contraseña:", show="*")
        if password is None: return None, None 

        return user, password

def get_credentials_olap():
        
        database = simpledialog.askstring("Base de datos", "Database:")
        if database is None: return None, None 

        return  database

def get_connection_oltp():
        """Solicita credenciales y devuelve una conexión a la base de datos."""
        global conn_oltp
        user, password = get_credentials()
        
        if not user or not password:
            messagebox.showwarning("Cancelado", "No se ingresaron credenciales.")
            return None
        
        dsn = "localhost:1521/xe" 

        try:
            oracledb.init_oracle_client(lib_dir=r"C:\oraclexe\app\oracle\product\11.2.0\server\bin")
            conn_oltp = oracledb.connect(user=user, password=password, dsn=dsn)
            messagebox.showinfo("Éxito", "¡Conexión exitosa a Oracle!")
            statusoltp.config(text="Estado: conectado a " + user + " desde " + dsn)
            actualizar_menu_oltp()
            frame_tablas_oltp.place(x=0, y= 140)
            btn_cambiar_vista.place(x=100, y=35)
        except oracledb.DatabaseError as e:
            messagebox.showerror("Error de conexión", f"Error: {e}")

def get_connection_olap():
        """Solicita credenciales y devuelve una conexión a la base de datos."""
        global conn_olap
        server ="localhost"
        database = get_credentials_olap()
        
        if not server or not database:
            messagebox.showwarning("Cancelado", "No se ingresaron credenciales.")
            return None
        
        try:
            conn_olap = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes")
            messagebox.showinfo("Éxito", "¡Conexión exitosa a SQLSERVER!")
            statusolap.config(text="Estado: conectado a " + database + " desde " + server)
            frame_tablas_olap.place(x=1000,y=80)
            actualizar_menu_olap()
        except Exception as exServer:
            messagebox.showerror("Error de conexión", f"Error: {exServer}")
            
def obtener_tablas_oltp(conn):
    """Devuelve una lista con los nombres de las tablas del esquema."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM user_tables")  
        tablas = [tabla[0] for tabla in cursor.fetchall()]
        cursor.close()
        return tablas
    except oracledb.DatabaseError as e:
        messagebox.showerror("Error", f"No se pudieron obtener las tablas: {e}")
        return []

def actualizar_menu_oltp():
    """Actualiza el menú desplegable con las tablas de la BD."""
    tablas = obtener_tablas_oltp(conn_oltp)
    
    if not tablas:
        messagebox.showwarning("Aviso", "No hay tablas disponibles.")
        return

    # Actualizar el menú desplegable
    menu_opciones_oltp["menu"].delete(0, "end")  # Eliminar opciones anteriores
    for tabla in tablas:
        menu_opciones_oltp["menu"].add_command(label=tabla, command=lambda value=tabla: var_seleccion_oltp.set(value))
    
    # Establecer la primera opción como seleccionada
    var_seleccion_oltp.set(tablas[0] if tablas else "Ninguna")

def obtener_tablas_olap(conn):
    """Obtiene los nombres de las tablas en SQL Server."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        tablas = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tablas
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def actualizar_menu_olap():
    """Actualiza el menú desplegable con las tablas de la BD."""
    tablas = obtener_tablas_olap(conn_olap)
    
    if not tablas:
        messagebox.showwarning("Aviso", "No hay tablas disponibles.")
        return

    # Actualizar el menú desplegable
    menu_opciones_olap["menu"].delete(0, "end")  # Eliminar opciones anteriores
    for tabla in tablas:
        menu_opciones_olap["menu"].add_command(label=tabla, command=lambda value=tabla: var_seleccion_olap.set(value))
    
    # Establecer la primera opción como seleccionada
    var_seleccion_olap.set(tablas[0] if tablas else "Ninguna")

def cambiar_vista():
    global oltp_option
    """Alterna entre el menú de tablas y el área de consultas SQL."""
    if frame_tablas_oltp.winfo_ismapped():
        frame_tablas_oltp.place_forget()
        frame_tablas_extraidas.place_forget()
        btn_seleccionar_columnas_oltp.place_forget()
        frame_etl_options.place_forget()
        btn_aplicar_transformaciones.place_forget()
        frame_sql_consultas.place(x=0, y= 140)
        btn_cambiar_vista.config(text="Ver Menú de Tablas")
        
    else:
        frame_sql_consultas.place_forget()
        frame_tablas_extraidas.place_forget()
        btn_seleccionar_columnas_oltp.place_forget()
        frame_etl_options.place_forget()
        btn_aplicar_transformaciones.place_forget()
        frame_tablas_oltp.place(x=0, y= 140)
        btn_cambiar_vista.config(text="Ver Área de SQL")
        

def elegir_consulta():
    """Ejecuta la consulta SQL y muestra los campos disponibles para selección."""
    if not conn_oltp:
        messagebox.showwarning("Advertencia", "No hay conexión con la base de datos.")
        return

    consulta = entrada_sql.get("1.0", END).strip()
    if not consulta:
        messagebox.showwarning("Advertencia", "Ingrese una consulta SQL.")
        return
    global datos_antes_filtro_e
    cursor = conn_oltp.cursor()
    try:
        cursor.execute(consulta)
        columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de columnas
        datos = cursor.fetchall()
        datos_antes_filtro_e = pd.DataFrame(datos, columns=columnas)
        frame_tablas_extraidas.place(x=0,y=500)
        btn_seleccionar_columnas_oltp.place(x=20,y=800)
        # Limpiar selección anterior
        for widget in frame_tablas_extraidas.winfo_children():
            widget.destroy()

        global selected_columns
        selected_columns = {}

        # Crear checkboxes para cada columna
        for i, col in enumerate(datos_antes_filtro_e.columns):
            selected_columns[col] = BooleanVar()
            chk = Checkbutton(frame_tablas_extraidas, text=col, variable=selected_columns[col])
            chk.grid(row=i, column=0, sticky="w")

    except oracledb.DatabaseError as e:
        messagebox.showerror("Error", f"Error en la consulta: {e}")


def elegir_tabla_oltp():
    """Ejecuta la consulta SQL y muestra los campos disponibles para selección."""
    if not conn_oltp:
        messagebox.showwarning("Advertencia", "No hay conexión con la base de datos.")
        return

    consulta = "SELECT * FROM "+var_seleccion_oltp.get()
    if not consulta:
        messagebox.showwarning("Advertencia", "Elija una tabla")
        return
    global datos_antes_filtro_e
    cursor = conn_oltp.cursor()
    try:
        cursor.execute(consulta)
        columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de columnas
        datos = cursor.fetchall()
        datos_antes_filtro_e = pd.DataFrame(datos, columns=columnas)
        frame_tablas_extraidas.place(x=0,y=500)
        btn_seleccionar_columnas_oltp.place(x=20,y=800)
        # Limpiar selección anterior
        for widget in frame_tablas_extraidas.winfo_children():
            widget.destroy()

        global selected_columns
        selected_columns = {}

        # Crear checkboxes para cada columna
        for i, col in enumerate(datos_antes_filtro_e.columns):
            selected_columns[col] = BooleanVar()
            chk = Checkbutton(frame_tablas_extraidas, text=col, variable=selected_columns[col])
            chk.grid(row=i, column=0, sticky="w")

    except oracledb.DatabaseError as e:
        messagebox.showerror("Error", f"Error en la consulta: {e}")

def seleccionar_columnas():
    global datos_despues_filtro_e
    global datos_antes_filtro_e
    
    seleccionadas = [col for col, var in selected_columns.items() if var.get()]
    datos_despues_filtro_e = datos_antes_filtro_e[seleccionadas]
    frame_etl_options.place(x=500,y=10)
    btn_aplicar_transformaciones.place(x=500,y=800)
    for widget in frame_etl_options.winfo_children():
        widget.destroy()
    
    global selected_etl_columns , selected_concat_etl_columns, columns_type
    selected_etl_columns = {col: StringVar(value="Ninguno") for col in datos_despues_filtro_e.columns}
    selected_concat_etl_columns = {col: StringVar(value=datos_despues_filtro_e.columns[0]) for col in datos_despues_filtro_e.columns}
    
    for i,col in enumerate(datos_despues_filtro_e.columns):
        ttk.Label(frame_etl_options, text=col).grid(row=i, column=0,sticky="w")

        # Opciones según tipo de dato
        if datos_despues_filtro_e[col].dtype == np.datetime64:
            opciones = ["...","Ninguno", "Obtener Día", "Obtener Mes", "Obtener Año", "Obtener Hora"]
        elif datos_despues_filtro_e[col].dtype == 'object' or datos_despues_filtro_e[col].dtype.name == 'string':
            opciones = ["...","Ninguno", "Minúscula", "Mayúscula", "Concatenar"]
        elif np.issubdtype(datos_despues_filtro_e[col].dtype, np.int64):
            datos_despues_filtro_e[col] = datos_despues_filtro_e[col].astype(str)
            opciones = ["...", "Ninguno", "Concatenar"]
        else:
            opciones = ["...", "Ninguno", "Concatenar"]

        # Menú de transformación
        ttk.OptionMenu(frame_etl_options, selected_etl_columns[col], *opciones).grid(row=i, column=1,sticky="w")
        
        # Si es concatenación, se muestra otro menú de selección de columna
        if "Concatenar" in opciones:
            ttk.Label(frame_etl_options, text="Concatenar con:").grid(row=i, column=2,sticky="w")
            ttk.OptionMenu(frame_etl_options, selected_concat_etl_columns[col], "...","Ninguno", *datos_despues_filtro_e.columns).grid(row=i, column=3,sticky="w")

def aplicar_transformaciones():
    global datos_despues_filtro_e
    global datos_despues_filtro_t
    datos_despues_filtro_t = datos_despues_filtro_e.copy()

    for col, var in selected_etl_columns.items():
        operacion = var.get()

        if operacion == "Minúscula":
            datos_despues_filtro_t["Minúscula "+col] = datos_despues_filtro_t[col].astype(str).str.lower()
        elif operacion == "Mayúscula":
            datos_despues_filtro_t["Mayúscula "+col] = datos_despues_filtro_t[col].astype(str).str.upper()
        elif operacion == "Obtener Día":
            datos_despues_filtro_t["Dia de: " +col] = pd.to_datetime(datos_despues_filtro_t[col], errors="coerce").dt.day
        elif operacion == "Obtener Mes":
            datos_despues_filtro_t["Mes de: " +col] = pd.to_datetime(datos_despues_filtro_t[col], errors="coerce").dt.month
        elif operacion == "Obtener Año ":
            datos_despues_filtro_t["Año de: " +col] = pd.to_datetime(datos_despues_filtro_t[col], errors="coerce").dt.year
        elif operacion == "Obtener Hora":
            datos_despues_filtro_t["Hora de: " +col] = pd.to_datetime(datos_despues_filtro_t[col], errors="coerce").dt.strftime("%H:%M:%S")
        elif operacion == "Concatenar":
            col_concat = selected_concat_etl_columns[col].get()
            datos_despues_filtro_t[col+"+"+col_concat] = datos_despues_filtro_t[col].astype(str) + " " + datos_despues_filtro_t[col_concat].astype(str)
    
    LabelOlap.place(x=1000,y=0)
    statusolap.place(x=1000,y=20)
    botonIngresar_Olap.place(x=1000,y=35)

def elegir_tabla_olap():
    """Ejecuta la consulta SQL y muestra los campos disponibles para selección."""
    if not conn_olap:
        messagebox.showwarning("Advertencia", "No hay conexión con la base de datos.")
        return

    consulta = "SELECT * FROM "+var_seleccion_olap.get()
    if not consulta:
        messagebox.showwarning("Advertencia", "Elija una tabla")
        return
    cursor = conn_olap.cursor()
    try:
        cursor.execute(consulta)
        columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de columnas
        frame_inserciones.place(x=1000,y=500)
        btn_insertar_datos.place(x=1000,y=800)
        # Limpiar selección anterior
        for widget in frame_inserciones.winfo_children():
            widget.destroy()

        global selected_columns_olap
        selected_columns_olap = {}
        global selected_columns_to_transfer
        selected_columns_to_transfer = {}
        # Crear checkboxes para cada columna
        for i, col in enumerate(columnas):
            selected_columns_olap[col] = BooleanVar()
            chk = Checkbutton(frame_inserciones, text=col, variable=selected_columns_olap[col])
            chk.grid(row=i, column=0, sticky="w")
            ttk.Label(frame_inserciones, text="llenar campo con: ").grid(row=i, column=1,sticky="w")
            menu_var = StringVar(value="Ninguno")
            selected_columns_to_transfer[col] = menu_var
            menu = ttk.OptionMenu(frame_inserciones, menu_var, "...","Ninguno",*datos_despues_filtro_t.columns)
            menu.grid(row=i, column=2,sticky="w")
            
    except oracledb.DatabaseError as e:
        messagebox.showerror("Error", f"Error en la consulta: {e}")

"""sin terminar"""
def insertar_datos():
    global conn_olap
    if not conn_olap:
        return
    
    cursor = conn_olap.cursor()


    columnas_seleccionadas = [col for col, var in selected_columns_olap.items() if var.get()]

    if not columnas_seleccionadas:
        messagebox.showwarning("Advertencia", "No se seleccionaron columnas.")
        return
    datos_a_insertar = []
    for _, fila in datos_despues_filtro_t.iterrows():
        valores = []
        insertar = False
        for col in columnas_seleccionadas:
            col_origen = selected_columns_to_transfer[col].get()  # Columna del DataFrame elegida
            if col_origen == "Ninguno" or col_origen == "...":
                valores.append(None)  # Evitar valores no deseados
            else:
                valores.append(fila[col_origen])  # Tomar el valor de la columna seleccionada
                insertar = True
        if insertar:
            datos_a_insertar.append(tuple(valores+valores))
    
    
    if not datos_a_insertar:
        messagebox.showwarning("Advertencia", "No hay datos válidos para insertar.")
        return
    
    # Construir consulta SQL dinámica
    placeholders = ", ".join(["?" for _ in columnas_seleccionadas])
    columnas_str = ", ".join(columnas_seleccionadas)
    query = f"""
    INSERT INTO {var_seleccion_olap.get()} ({columnas_str})
    SELECT {placeholders}
    WHERE NOT EXISTS (
    SELECT 1 FROM {var_seleccion_olap.get()} WHERE { " AND ".join([f"{col} = ?" for col in columnas_seleccionadas]) }
    );
    """
    

    try:
        cursor.executemany(query, datos_a_insertar)
        conn_olap.commit()
        messagebox.showinfo("Éxito", "Datos insertados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron insertar los datos: {e}")

    


raiz=Tk()
raiz.geometry("2500x1400")
raiz.title("ETL Bases de datos II")

LabelOltp =Label(text="Conectarse a base de origen")
LabelOltp.place(x=0,y=0)
statusoltp =Label(text="Estado: desconectado")
statusoltp.place(x=0,y=20)
botonIngresar_Oltp= Button(raiz, text="Conectar",command=get_connection_oltp)
botonIngresar_Oltp.place(x=10,y=35)

frame_tablas_oltp = Frame(raiz)

var_seleccion_oltp = StringVar()
var_seleccion_oltp.set("Cargando...")
menu_opciones_oltp = OptionMenu(frame_tablas_oltp, var_seleccion_oltp, "Cargando...")
menu_opciones_oltp.pack(pady=10)
btn_elegir_tabla_oltp = Button(frame_tablas_oltp, text="Elegir tabla", command=elegir_tabla_oltp)
btn_elegir_tabla_oltp.pack(pady=5)

frame_sql_consultas = Frame(raiz)
entrada_sql = Text(frame_sql_consultas, height=5, width=40)
entrada_sql.pack(pady=5)
btn_elegir_sql = Button(frame_sql_consultas, text="Elegir Consulta", command=elegir_consulta)
btn_elegir_sql.pack(pady=5)

btn_cambiar_vista = Button(raiz, text="Ver Área de consultas SQL", command=cambiar_vista)

frame_tablas_extraidas = Frame(raiz)
btn_seleccionar_columnas_oltp = Button(raiz, text="Seleccionar Columnas", command=seleccionar_columnas)


frame_etl_options = Frame(raiz)
btn_aplicar_transformaciones = Button(raiz, text="Aplicar transformaciones", command=aplicar_transformaciones)


LabelOlap =Label(text="Conectarse a base de destino")
statusolap =Label(text="Estado: desconectado")
botonIngresar_Olap= Button(raiz, text="Conectar",command=get_connection_olap)


frame_tablas_olap = Frame(raiz)
var_seleccion_olap = StringVar()
var_seleccion_olap.set("Cargando...")
menu_opciones_olap = OptionMenu(frame_tablas_olap, var_seleccion_olap, "Cargando...")
menu_opciones_olap.pack(pady=10)
btn_elegir_tabla_olap = Button(frame_tablas_olap, text="Elegir tabla", command=elegir_tabla_olap)
btn_elegir_tabla_olap.pack(pady=5)

frame_inserciones = Frame(raiz)
btn_insertar_datos = Button(raiz, text="Insertar datos", command=insertar_datos)


raiz.mainloop()