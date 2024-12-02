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
MONGO_COLECTION_1 = "Provedores"
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
BaseDatos = client[MONGO_BASEDATOS]
Colection_1 = BaseDatos[MONGO_COLECTION_1]
ID_PROVEDORES = ""

def EditarRegistro ():
    global ID_PROVEDORES
    if len(empresa.get())!=0 and len(nombre_contacto.get())!=0 and len(telefono.get())!=0 and len(email.get())!=0 and len(producto.get())!=0 and len(precio_unitario.get())!=0 and len(ubicacion.get())!=0:
        try:
            id_buscar = {"_id":ObjectId(ID_PROVEDORES)}
            nuevosValores = {"$set":{"empresa":empresa.get(),"nombre_contacto":nombre_contacto.get(), "telefono":telefono.get(), "email":email.get(), "producto":producto.get(), "precio_unitario":precio_unitario.get(), "ubicacion":ubicacion.get()}}
            Colection_1.update_one(id_buscar,nuevosValores)
            empresa.delete(0,END)
            nombre_contacto.delete(0,END)
            telefono.delete(0,END)
            email.delete(0,END)
            producto.delete(0,END)
            precio_unitario.delete(0,END)
            ubicacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else :
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
def mostrar_datos(empresa="", nombre_contacto="", telefono="", email="", producto="", precio_unitario="",  ubicacion=""):
    Objeto_Buscar = {}
    if len(empresa) != 0:
        Objeto_Buscar["empresa"] = empresa
    if len(nombre_contacto) != 0:
        Objeto_Buscar["nombre_contacto"] = nombre_contacto
    if len(telefono) != 0:
        Objeto_Buscar["telefono"] = telefono
    if len(email) != 0:
        Objeto_Buscar["email"] = email
    if len(producto) != 0:
        Objeto_Buscar["producto"] = producto
    if len(precio_unitario) != 0:
        Objeto_Buscar["precio_unitario"] = precio_unitario
    if len(ubicacion) != 0:
        Objeto_Buscar["ubicacion"] = ubicacion
    
    try:
        # Limpiar la tabla antes de llenarla
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)

        # Insertar los datos de MongoDB en la tabla
        for documento in Colection_1.find(Objeto_Buscar):
            tabla.insert('', 0, text=str(documento["_id"]),
                        values=(documento["empresa"], documento["nombre_contacto"], documento["telefono"], documento["email"], documento["producto"], 
                        documento["precio_unitario"], documento["ubicacion"]))
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print(f"Error: Tiempo excedido - {errorTiempo}")
    except pymongo.errors.ConnectionFailure as errorConexion:
        print(f"Error: Fallo al conectarse a MongoDB - {errorConexion}")
def crearRegistro():
    if (empresa.get())!=0 and len(nombre_contacto.get())!=0 and len(telefono.get())!=0 and len(email.get())!=0 and len(producto.get())!=0 and len(precio_unitario.get())!=0 and len(ubicacion.get())!=0:
        try:
            documento = {"empresa":empresa.get(),"nombre_contacto":nombre_contacto.get(), "telefono":telefono.get(), "email":email.get(), "producto":producto.get(), "precio_unitario":precio_unitario.get(), "ubicacion":ubicacion.get()}
            Colection_1.insert_one(documento)
            empresa.delete(0,END)
            nombre_contacto.delete(0,END)
            telefono.delete(0,END)
            email.delete(0,END)
            producto.delete(0,END)
            precio_unitario.delete(0,END)
            ubicacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
def dobleClickTabla(event):
    global ID_PROVEDORES
    ID_PROVEDORES = str(tabla.item(tabla.selection())["text"])
    documento = Colection_1.find({"_id":ObjectId(ID_PROVEDORES)})[0]
    empresa.delete(0,END)
    empresa.insert(0,documento["empresa"])
    nombre_contacto.delete(0,END)
    nombre_contacto.insert(0,documento["nombre_contacto"])
    telefono.delete(0,END)
    telefono.insert(0,documento["telefono"])
    email.delete(0,END)
    email.insert(0,documento["email"])
    producto.delete(0,END)
    producto.insert(0,documento["producto"])
    precio_unitario.delete(0,END)
    precio_unitario.insert(0,documento["precio_unitario"])
    ubicacion.delete(0,END)
    ubicacion.insert(0,documento["ubicacion"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    borrar["state"] = "normal"
def BorrarRegistro():
    global ID_PROVEDORES
    try:
        id_buscar = {"_id":ObjectId(ID_PROVEDORES)}
        Colection_1.delete_one(id_buscar)
        empresa.delete(0,END)
        nombre_contacto.delete(0,END)
        telefono.delete(0,END)
        email.delete(0,END)
        producto.delete(0,END)
        precio_unitario.delete(0,END)
        ubicacion.delete(0,END)    
    except pymongo.errors.ConnectionFailure as error:
        print (error)
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
    mostrar_datos()
def buscarRegistro():
    mostrar_datos(buscar_nombre.get(), buscar_empresa.get(), buscar_nombre.get(), buscar_telefono.get(), buscar_email.get(), buscar_producto.get(), buscar_precio.get(), buscar_ubicacion.get())

ventana = Tk()
tabla = ttk.Treeview(ventana, columns=("col1", "col2", "col3", "col4","col5","col6","col7"))
tabla.grid(row=1, column=0, columnspan=7)

# Encabezados de la tabla
tabla.heading("#0", text="ID")
tabla.heading("col1", text="Empresa")
tabla.heading("col2", text="Nombre de contacto")
tabla.heading("col3", text="Telefono")
tabla.heading("col4", text="Email")
tabla.heading("col5", text="Producto")
tabla.heading("col6", text="Precio Unitario")
tabla.heading("col7", text="Ubicacion")

# Ajustar columnas opcionalmente
tabla.column("#0", width=175) 
tabla.column("col1", width=150)
tabla.column("col2", width=150)
tabla.column("col3", width=90)
tabla.column("col4", width=110)
tabla.column("col5", width=100)
tabla.column("col6", width=100)
tabla.column("col7", width=110)

tabla.bind("<Double-Button-1>",dobleClickTabla)
#Empresa
Label(ventana, text="Empresa").grid(row=2,column=0,sticky=W+E)
empresa = Entry(ventana)
empresa.grid(row=2,column=1,sticky=W+E)
#Nombre de contacto
Label(ventana, text="Nombre de contacto").grid(row=3,column=0,sticky=W+E)
nombre_contacto = Entry(ventana)
nombre_contacto.grid(row=3,column=1,sticky=W+E)
#Telefono
Label(ventana, text="Telefono").grid(row=4,column=0,sticky=W+E)
telefono = Entry(ventana)
telefono.grid(row=4,column=1,sticky=W+E)
#Email
Label(ventana, text="Email").grid(row=5,column=0,sticky=W+E)
email = Entry(ventana)
email.grid(row=5,column=1,sticky=W+E)
#Producto
Label(ventana, text="Producto").grid(row=6,column=0,sticky=W+E)
producto = Entry(ventana)
producto.grid(row=6,column=1,sticky=W+E)
#Precio Unitario
Label(ventana, text="Precio Unitario").grid(row=7,column=0,sticky=W+E)
precio_unitario = Entry(ventana)
precio_unitario.grid(row=7,column=1,sticky=W+E)
#Ubicacion
Label(ventana, text="Ubicacion").grid(row=8,column=0,sticky=W+E)
ubicacion = Entry(ventana)
ubicacion.grid(row=8,column=1,sticky=W+E)

#Boton crear
crear = Button(ventana, text="Agregar Provedor", command=crearRegistro, bg="green", fg="white")
crear.grid(row=9,columnspan=2,sticky=W+E)
#Boton editar
editar = Button(ventana, text="Editar Producto", command=EditarRegistro, bg="yellow")
editar.grid(row=10,columnspan=2,sticky=W+E)
editar["state"] = "disabled"
#Boton borrar
borrar = Button(ventana, text="Borrar Producto", command=BorrarRegistro, bg="red",fg="white")
borrar.grid(row=11,columnspan=2,sticky=W+E)
borrar["state"] = "disabled"
#Buscar Buscar por Empresa
Label(ventana, text="Buscar por Empresa").grid(row=12,column=0,sticky=W+E)
buscar_empresa = Entry(ventana)
buscar_empresa.grid(row=12,column=1,sticky=W+E)
buscar_empresa.focus()
#Buscar Buscar por Contacto
Label(ventana, text="Buscar por Contacto").grid(row=13,column=0,sticky=W+E)
buscar_nombre = Entry(ventana)
buscar_nombre.grid(row=13,column=1,sticky=W+E)

#Buscar Telefono
Label(ventana, text="Buscar por Telefono").grid(row=14,column=0,sticky=W+E)
buscar_telefono = Entry(ventana)
buscar_telefono.grid(row=14,column=1,sticky=W+E)
#Buscar email
Label(ventana, text="Buscar por email").grid(row=15,column=0,sticky=W+E)
buscar_email = Entry(ventana)
buscar_email.grid(row=15,column=1,sticky=W+E)
#Buscar producto
Label(ventana, text="Buscar por producto").grid(row=16,column=0,sticky=W+E)
buscar_producto = Entry(ventana)
buscar_producto.grid(row=16,column=1,sticky=W+E)
#Buscar precio
Label(ventana, text="Buscar por Precio Unitario").grid(row=17,column=0,sticky=W+E)
buscar_precio = Entry(ventana)
buscar_precio.grid(row=17,column=1,sticky=W+E)
#Buscar Ubicacion
Label(ventana, text="Buscar por Ubicacion").grid(row=18,column=0,sticky=W+E)
buscar_ubicacion = Entry(ventana)
buscar_ubicacion.grid(row=18,column=1,sticky=W+E)

#Boton buscar
buscar = Button(ventana, text="Buscar provedores", command=buscarRegistro, bg="blue", fg="white")
buscar.grid(row=19,columnspan=2,sticky=W+E)

mostrar_datos()
ventana.mainloop()