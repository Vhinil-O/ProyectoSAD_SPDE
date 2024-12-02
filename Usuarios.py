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
MONGO_COLECTION_1 = "Users"
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
BaseDatos = client[MONGO_BASEDATOS]
Colection_1 = BaseDatos[MONGO_COLECTION_1]
ID_USUARIO = ""

def EditarRegistro ():
    global ID_USUARIO
    if len(nombre.get())!=0 and len(email.get())!=0 and len(telefono.get())!=0 and len(producto.get())!=0:
        try:
            id_buscar = {"_id":ObjectId(ID_USUARIO)}
            nuevosValores = {"$set":{"nombre":nombre.get(), "email":email.get(), "telefono":telefono.get(), "producto":producto.get()}}
            Colection_1.update_one(id_buscar,nuevosValores)
            nombre.delete(0,END)
            email.delete(0,END)
            telefono.delete(0,END)
            producto.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else :
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
def mostrar_datos(nombre="", email="", telefono="", producto=""):
    Objeto_Buscar = {}
    if len(nombre) != 0:
        Objeto_Buscar["nombre"] = nombre
    if len(email) != 0:
        Objeto_Buscar["email"] = email
    if len(telefono) != 0:
        Objeto_Buscar["telefono"] = telefono
    if len(producto) != 0:
        Objeto_Buscar["producto"] = producto
    try:
        # Limpiar la tabla antes de llenarla
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
        # Insertar los datos de MongoDB en la tabla
        for documento in Colection_1.find(Objeto_Buscar):
            tabla.insert('', 0, text=str(documento["_id"]), values=(documento["nombre"], documento["email"], documento["telefono"], documento["producto"]))
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print(f"Error: Tiempo excedido - {errorTiempo}")
    except pymongo.errors.ConnectionFailure as errorConexion:
        print(f"Error: Fallo al conectarse a MongoDB - {errorConexion}")
def crearRegistro():
    if len(nombre.get())!=0 and len(email.get())!=0 and len(telefono.get())!=0 and len(producto.get())!=0:
        try:
            documento = {"nombre":nombre.get(), "email":email.get(), "telefono":telefono.get(), "producto":producto.get()}
            Colection_1.insert_one(documento)
            nombre.delete(0,END)
            email.delete(0,END)
            telefono.delete(0,END)
            producto.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
def dobleClickTabla(event):
    global ID_USUARIO
    ID_USUARIO = str(tabla.item(tabla.selection())["text"])
    documento = Colection_1.find({"_id":ObjectId(ID_USUARIO)})[0]
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    email.delete(0,END)
    email.insert(0,documento["email"])
    telefono.delete(0,END)
    telefono.insert(0,documento["telefono"])
    producto.delete(0,END)
    producto.insert(0,documento["producto"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    borrar["state"] = "normal"
def BorrarRegistro():
    global ID_USUARIO
    try:
        id_buscar = {"_id":ObjectId(ID_USUARIO)}
        Colection_1.delete_one(id_buscar)
        nombre.delete(0,END)
        email.delete(0,END)
        telefono.delete(0,END)
        producto.delete(0,END)    
    except pymongo.errors.ConnectionFailure as error:
        print (error)
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
    mostrar_datos()
def buscarRegistro():
    mostrar_datos(buscar_nombre.get(), buscar_email.get(), buscar_telefono.get(), buscar_producto.get())

ventana = Tk()
tabla = ttk.Treeview(ventana, columns=("col1", "col2", "col3", "col4"))
tabla.grid(row=1, column=0, columnspan=7)

# Encabezados de la tabla
tabla.heading("#0", text="ID")
tabla.heading("col1", text="Nombre")
tabla.heading("col2", text="Email")
tabla.heading("col3", text="Teléfono")
tabla.heading("col4", text="Producto")
# Ajustar columnas opcionalmente
tabla.column("#0", width=200)  # Ajustar la anchura del ID
tabla.column("col1", width=100)
tabla.column("col2", width=200)
tabla.column("col3", width=100)
tabla.column("col4", width=100)
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
#Producto
Label(ventana, text="Producto").grid(row=5,column=0,sticky=W+E)
producto = Entry(ventana)
producto.grid(row=5,column=1,sticky=W+E)
#Boton crear
crear = Button(ventana, text="Agregar Usuario", command=crearRegistro, bg="green", fg="white")
crear.grid(row=9,columnspan=2,sticky=W+E)
#Boton editar
editar = Button(ventana, text="Editar datos del Usuario", command=EditarRegistro, bg="yellow")
editar.grid(row=10,columnspan=2,sticky=W+E)
editar["state"] = "disabled"
#Boton borrar
borrar = Button(ventana, text="Borrar datos del Usuario", command=BorrarRegistro, bg="red",fg="white")
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
#Buscar Producto
Label(ventana, text="Buscar por Departamento").grid(row=15,column=0,sticky=W+E)
buscar_producto = Entry(ventana)
buscar_producto.grid(row=15,column=1,sticky=W+E)

#Boton buscar
buscar = Button(ventana, text="Buscar Usuario", command=buscarRegistro, bg="blue", fg="white")
buscar.grid(row=16,columnspan=2,sticky=W+E)

mostrar_datos()
ventana.mainloop()
