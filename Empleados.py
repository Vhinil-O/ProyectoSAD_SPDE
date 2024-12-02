from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
import pymongo.errors
from bson.objectid import ObjectId

MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIME_OUT = 1000
MONGO_URI = "mongodb://" + MONGO_HOST + ":" + MONGO_PUERTO + "/"
MONGO_BASEDATOS = "PlantIA"
MONGO_COLECTION_1 = "Empleados"
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
BaseDatos = client[MONGO_BASEDATOS]
Colection_1 = BaseDatos[MONGO_COLECTION_1]
ID_EMPLEADO = ""

def EditarRegistro ():
    global ID_EMPLEADO
    if len(nombre.get())!=0 and len(email.get())!=0 and len(telefono.get())!=0 and len(departamento.get())!=0 and len(cargo.get())!=0 and len(sueldo.get())!=0 and len(estado.get())!=0:
        try:
            id_buscar = {"_id":ObjectId(ID_EMPLEADO)}
            nuevosValores = {"$set":{"nombre":nombre.get(), "email":email.get(), "telefono":telefono.get(), "departamento":departamento.get(), "cargo":cargo.get(), "sueldo":sueldo.get(), "estado":estado.get()}}
            Colection_1.update_one(id_buscar,nuevosValores)
            nombre.delete(0,END)
            email.delete(0,END)
            telefono.delete(0,END)
            departamento.delete(0,END)
            cargo.delete(0,END)
            sueldo.delete(0,END)
            estado.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else :
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
def mostrar_datos(nombre="", email="", telefono="", departamento="", cargo="", sueldo="", estado=""):
    Objeto_Buscar = {}
    if len(nombre) != 0:
        Objeto_Buscar["nombre"] = nombre
    if len(email) != 0:
        Objeto_Buscar["email"] = email
    if len(telefono) != 0:
        Objeto_Buscar["telefono"] = telefono
    if len(departamento) != 0:
        Objeto_Buscar["departamento"] = departamento
    if len(cargo) != 0:
        Objeto_Buscar["cargo"] = cargo
    if len(sueldo) != 0:
        Objeto_Buscar["sueldo"] = sueldo
    if len(estado) != 0:
        Objeto_Buscar["estado"] = estado
    
    try:
        # Limpiar la tabla antes de llenarla
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)

        # Insertar los datos de MongoDB en la tabla
        for documento in Colection_1.find(Objeto_Buscar):
            tabla.insert('', 0, text=str(documento["_id"]),
                         values=(documento["nombre"], documento["email"], documento["telefono"], 
                                 documento["departamento"], documento["cargo"], documento["sueldo"], 
                                 documento["estado"]))
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print(f"Error: Tiempo excedido - {errorTiempo}")
    except pymongo.errors.ConnectionFailure as errorConexion:
        print(f"Error: Fallo al conectarse a MongoDB - {errorConexion}")
def crearRegistro():
    if len(nombre.get())!=0 and len(email.get())!=0 and len(telefono.get())!=0 and len(departamento.get())!=0 and len(cargo.get())!=0 and len(sueldo.get())!=0 and len(estado.get())!=0:
        try:
            documento = {"nombre":nombre.get(), "email":email.get(), "telefono":telefono.get(), "departamento":departamento.get(), "cargo":cargo.get(), "sueldo":sueldo.get(), "estado":estado.get()}
            Colection_1.insert_one(documento)
            nombre.delete(0,END)
            email.delete(0,END)
            telefono.delete(0,END)
            departamento.delete(0,END)
            cargo.delete(0,END)
            sueldo.delete(0,END)
            estado.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
def dobleClickTabla(event):
    global ID_EMPLEADO
    ID_EMPLEADO = str(tabla.item(tabla.selection())["text"])
    documento = Colection_1.find({"_id":ObjectId(ID_EMPLEADO)})[0]
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    email.delete(0,END)
    email.insert(0,documento["email"])
    telefono.delete(0,END)
    telefono.insert(0,documento["telefono"])
    departamento.delete(0,END)
    departamento.insert(0,documento["departamento"])
    cargo.delete(0,END)
    cargo.insert(0,documento["cargo"])
    sueldo.delete(0,END)
    sueldo.insert(0,documento["sueldo"])
    estado.delete(0,END)
    estado.insert(0,documento["estado"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    borrar["state"] = "normal"
def BorrarRegistro():
    global ID_EMPLEADO
    try:
        id_buscar = {"_id":ObjectId(ID_EMPLEADO)}
        Colection_1.delete_one(id_buscar)
        nombre.delete(0,END)
        email.delete(0,END)
        telefono.delete(0,END)
        departamento.delete(0,END)
        cargo.delete(0,END)
        sueldo.delete(0,END)
        estado.delete(0,END)    
    except pymongo.errors.ConnectionFailure as error:
        print (error)
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
    mostrar_datos()
def buscarRegistro():
    mostrar_datos(buscar_nombre.get(), buscar_email.get(), buscar_telefono.get(), buscar_departamento.get(), buscar_cargo.get(), buscar_sueldo.get(), buscar_estado.get())

ventana = Tk()
tabla = ttk.Treeview(ventana, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
tabla.grid(row=1, column=0, columnspan=7)

# Encabezados de la tabla
tabla.heading("#0", text="ID")  # Para mostrar el _id de MongoDB
tabla.heading("col1", text="Nombre")
tabla.heading("col2", text="Email")
tabla.heading("col3", text="Teléfono")
tabla.heading("col4", text="Departamento")
tabla.heading("col5", text="Cargo")
tabla.heading("col6", text="Sueldo")
tabla.heading("col7", text="Estado")

# Ajustar columnas opcionalmente
tabla.column("#0", width=200)  # Ajustar la anchura del ID
tabla.column("col1", width=100)
tabla.column("col2", width=200)
tabla.column("col3", width=100)
tabla.column("col4", width=100)
tabla.column("col5", width=100)
tabla.column("col6", width=100)
tabla.column("col7", width=100)
tabla.bind("<Double-Button-1>",dobleClickTabla)
#Nombre
Label(ventana, text="Nombre").grid(row=2,column=0,sticky=W+E)
nombre = Entry(ventana)
nombre.grid(row=2,column=1,sticky=W+E)
#Email
Label(ventana, text="Email").grid(row=3,column=0,sticky=W+E)
email = Entry(ventana)
email.grid(row=3,column=1,sticky=W+E)
#Telefono
Label(ventana, text="Telefono").grid(row=4,column=0,sticky=W+E)
telefono = Entry(ventana)
telefono.grid(row=4,column=1,sticky=W+E)
#Departamento
Label(ventana, text="Departamento").grid(row=5,column=0,sticky=W+E)
departamento = Entry(ventana)
departamento.grid(row=5,column=1,sticky=W+E)
#Cargo
Label(ventana, text="Cargo").grid(row=6,column=0,sticky=W+E)
cargo = Entry(ventana)
cargo.grid(row=6,column=1,sticky=W+E)
#Sueldo
Label(ventana, text="Sueldo").grid(row=7,column=0,sticky=W+E)
sueldo = Entry(ventana)
sueldo.grid(row=7,column=1,sticky=W+E)
#Estado
Label(ventana, text="Estado").grid(row=8,column=0,sticky=W+E)
estado = Entry(ventana)
estado.grid(row=8,column=1,sticky=W+E)
#Boton crear
crear = Button(ventana, text="Agregar empleado", command=crearRegistro, bg="green", fg="white")
crear.grid(row=9,columnspan=2,sticky=W+E)
#Boton editar
editar = Button(ventana, text="Editar datos del empleado", command=EditarRegistro, bg="yellow")
editar.grid(row=10,columnspan=2,sticky=W+E)
editar["state"] = "disabled"
#Boton borrar
borrar = Button(ventana, text="Borrar datos del empleado", command=BorrarRegistro, bg="red",fg="white")
borrar.grid(row=11,columnspan=2,sticky=W+E)
borrar["state"] = "disabled"
#Buscar Nombre
Label(ventana, text="Buscar por Nombre").grid(row=12,column=0,sticky=W+E)
buscar_nombre = Entry(ventana)
buscar_nombre.grid(row=12,column=1,sticky=W+E)
buscar_nombre.focus()
#Buscar Email
Label(ventana, text="Buscar por Email").grid(row=13,column=0,sticky=W+E)
buscar_email = Entry(ventana)
buscar_email.grid(row=13,column=1,sticky=W+E)
#Buscar Telefono
Label(ventana, text="Buscar por Telefono").grid(row=14,column=0,sticky=W+E)
buscar_telefono = Entry(ventana)
buscar_telefono.grid(row=14,column=1,sticky=W+E)
#Buscar Departamento
Label(ventana, text="Buscar por Departamento").grid(row=15,column=0,sticky=W+E)
buscar_departamento = Entry(ventana)
buscar_departamento.grid(row=15,column=1,sticky=W+E)
#Buscar Cargo
Label(ventana, text="Buscar por Cargo").grid(row=16,column=0,sticky=W+E)
buscar_cargo = Entry(ventana)
buscar_cargo.grid(row=16,column=1,sticky=W+E)
#Buscar Sueldo
Label(ventana, text="Buscar por Sueldo").grid(row=17,column=0,sticky=W+E)
buscar_sueldo = Entry(ventana)
buscar_sueldo.grid(row=17,column=1,sticky=W+E)
#Buscar Estado
Label(ventana, text="Buscar por Estado").grid(row=18,column=0,sticky=W+E)
buscar_estado = Entry(ventana)
buscar_estado.grid(row=18,column=1,sticky=W+E)
#Boton buscar
buscar = Button(ventana, text="Buscar empleado", command=buscarRegistro, bg="blue", fg="white")
buscar.grid(row=19,columnspan=2,sticky=W+E)

mostrar_datos()
ventana.mainloop()


