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
MONGO_COLECTION_1 = "Products"
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
BaseDatos = client[MONGO_BASEDATOS]
Colection_1 = BaseDatos[MONGO_COLECTION_1]
ID_PRODUCTO = ""

def EditarRegistro ():
    global ID_PRODUCTO
    if (tipo.get())!=0 and len(nombre.get())!=0 and len(tipo.get())!=0 and len(tamano.get())!=0 and len(precio.get())!=0 and len(color.get())!=0 and len(estilo.get())!=0:
        try:
            id_buscar = {"_id":ObjectId(ID_PRODUCTO)}
            nuevosValores = {"$set":{"nombre":nombre.get(), "tipo":tipo.get(), "tamano":tamano.get(), "precio":precio.get(), "color":color.get(), "estilo":estilo.get()}}
            Colection_1.update_one(id_buscar,nuevosValores)
            nombre.delete(0,END)
            tipo.delete(0,END)
            tamano.delete(0,END)
            precio.delete(0,END)
            color.delete(0,END)
            estilo.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else :
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
def mostrar_datos(nombre="", tipo="", tamano="", precio="", color="", estilo=""):
    Objeto_Buscar = {}
    if len(nombre) != 0:
        Objeto_Buscar["nombre"] = nombre
    if len(tipo) != 0:
        Objeto_Buscar["tipo"] = tipo
    if len(tamano) != 0:
        Objeto_Buscar["tamano"] = tamano
    if len(precio) != 0:
        Objeto_Buscar["precio"] = precio
    if len(color) != 0:
        Objeto_Buscar["color"] = color
    if len(estilo) != 0:
        Objeto_Buscar["estilo"] = estilo
    
    try:
        # Limpiar la tabla antes de llenarla
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)

        # Insertar los datos de MongoDB en la tabla
        for documento in Colection_1.find(Objeto_Buscar):
            tabla.insert('', 0, text=str(documento["_id"]),
                         values=(documento["nombre"], documento["tipo"], documento["tamano"], documento["precio"], documento["color"], 
                                 documento["estilo"],))
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print(f"Error: Tiempo excedido - {errorTiempo}")
    except pymongo.errors.ConnectionFailure as errorConexion:
        print(f"Error: Fallo al conectarse a MongoDB - {errorConexion}")
def crearRegistro():
    if (tipo.get())!=0 and len(nombre.get())!=0 and len(tipo.get())!=0 and len(tamano.get())!=0 and len(precio.get())!=0 and len(color.get())!=0 and len(estilo.get())!=0:
        try:
            documento = {"nombre":nombre.get(),"tipo":tipo.get(), "tamano":tamano.get(), "precio":precio.get(), "color":color.get(), "estilo":estilo.get(),}
            Colection_1.insert_one(documento)
            nombre.delete(0,END)
            tipo.delete(0,END)
            tamano.delete(0,END)
            precio.delete(0,END)
            color.delete(0,END)
            estilo.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
def dobleClickTabla(event):
    global ID_PRODUCTO
    ID_PRODUCTO = str(tabla.item(tabla.selection())["text"])
    documento = Colection_1.find({"_id":ObjectId(ID_PRODUCTO)})[0]
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    tipo.delete(0,END)
    tipo.insert(0,documento["tipo"])
    tamano.delete(0,END)
    tamano.insert(0,documento["tamano"])
    precio.delete(0,END)
    precio.insert(0,documento["precio"])
    color.delete(0,END)
    color.insert(0,documento["color"])
    estilo.delete(0,END)
    estilo.insert(0,documento["estilo"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    borrar["state"] = "normal"
def BorrarRegistro():
    global ID_PRODUCTO
    try:
        id_buscar = {"_id":ObjectId(ID_PRODUCTO)}
        Colection_1.delete_one(id_buscar)
        nombre.delete(0,END)
        tipo.delete(0,END)
        tamano.delete(0,END)
        precio.delete(0,END)
        color.delete(0,END)
        estilo.delete(0,END)    
    except pymongo.errors.ConnectionFailure as error:
        print (error)
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
    mostrar_datos()
def buscarRegistro():
    mostrar_datos(buscar_nombre.get(), buscar_tipo.get(), buscar_tamano.get(), buscar_precio.get(), buscar_color.get(), buscar_estilo.get())

ventana = Tk()
tabla = ttk.Treeview(ventana, columns=("col1", "col2", "col3", "col4","col5","col6"))
tabla.grid(row=1, column=0, columnspan=7)

# Encabezados de la tabla
tabla.heading("#0", text="ID")
tabla.heading("col1", text="Nombre")
tabla.heading("col2", text="Tipo")
tabla.heading("col3", text="Tamaño")
tabla.heading("col4", text="Precio")
tabla.heading("col5", text="Color")
tabla.heading("col6", text="Estilo")

# Ajustar columnas opcionalmente
tabla.column("#0", width=200) 
tabla.column("col1", width=100)
tabla.column("col2", width=100)
tabla.column("col3", width=100)
tabla.column("col4", width=100)
tabla.column("col5", width=100)
tabla.column("col6", width=100)

tabla.bind("<Double-Button-1>",dobleClickTabla)
#Nombre
Label(ventana, text="Nombre").grid(row=2,column=0,sticky=W+E)
nombre = Entry(ventana)
nombre.grid(row=2,column=1,sticky=W+E)
#Tipo
Label(ventana, text="Tipo").grid(row=3,column=0,sticky=W+E)
tipo = Entry(ventana)
tipo.grid(row=3,column=1,sticky=W+E)
#Tamaño
Label(ventana, text="Tamaño").grid(row=4,column=0,sticky=W+E)
tamano = Entry(ventana)
tamano.grid(row=4,column=1,sticky=W+E)
#Precio
Label(ventana, text="Precio").grid(row=5,column=0,sticky=W+E)
precio = Entry(ventana)
precio.grid(row=5,column=1,sticky=W+E)
#Color
Label(ventana, text="Color").grid(row=6,column=0,sticky=W+E)
color = Entry(ventana)
color.grid(row=6,column=1,sticky=W+E)
#Estilo
Label(ventana, text="Estilo").grid(row=7,column=0,sticky=W+E)
estilo = Entry(ventana)
estilo.grid(row=7,column=1,sticky=W+E)
#Boton crear
crear = Button(ventana, text="Agregar Producto", command=crearRegistro, bg="green", fg="white")
crear.grid(row=8,columnspan=2,sticky=W+E)
#Boton editar
editar = Button(ventana, text="Editar Producto", command=EditarRegistro, bg="yellow")
editar.grid(row=9,columnspan=2,sticky=W+E)
editar["state"] = "disabled"
#Boton borrar
borrar = Button(ventana, text="Borrar Producto", command=BorrarRegistro, bg="red",fg="white")
borrar.grid(row=10,columnspan=2,sticky=W+E)
borrar["state"] = "disabled"
#Buscar Tipo
Label(ventana, text="Buscar por Nombre").grid(row=11,column=0,sticky=W+E)
buscar_nombre = Entry(ventana)
buscar_nombre.grid(row=11,column=1,sticky=W+E)
buscar_nombre.focus()
#Buscar Tipo
Label(ventana, text="Buscar por Tipo").grid(row=12,column=0,sticky=W+E)
buscar_tipo = Entry(ventana)
buscar_tipo.grid(row=12,column=1,sticky=W+E)
#Buscar tamano
Label(ventana, text="Buscar por Tamaño").grid(row=13,column=0,sticky=W+E)
buscar_tamano = Entry(ventana)
buscar_tamano.grid(row=13,column=1,sticky=W+E)
#Buscar Precio
Label(ventana, text="Buscar por Precio").grid(row=14,column=0,sticky=W+E)
buscar_precio = Entry(ventana)
buscar_precio.grid(row=14,column=1,sticky=W+E)
#Buscar color
Label(ventana, text="Buscar por Color").grid(row=15,column=0,sticky=W+E)
buscar_color = Entry(ventana)
buscar_color.grid(row=15,column=1,sticky=W+E)
#Buscar Fabricante
Label(ventana, text="Buscar por Estilo").grid(row=16,column=0,sticky=W+E)
buscar_estilo = Entry(ventana)
buscar_estilo.grid(row=16,column=1,sticky=W+E)

#Boton buscar
buscar = Button(ventana, text="Buscar sensores", command=buscarRegistro, bg="blue", fg="white")
buscar.grid(row=17,columnspan=2,sticky=W+E)

mostrar_datos()
ventana.mainloop()