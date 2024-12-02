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
MONGO_COLECTION_1 = "Sensors"
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
BaseDatos = client[MONGO_BASEDATOS]
Colection_1 = BaseDatos[MONGO_COLECTION_1]
ID_SENSOR = ""

def EditarRegistro ():
    global ID_SENSOR
    if (tipo.get())!=0 and len(producto.get())!=0 and len(parametro.get())!=0 and len(fabricante.get())!=0:
        try:
            id_buscar = {"_id":ObjectId(ID_SENSOR)}
            nuevosValores = {"$set":{"tipo":tipo.get(), "producto":producto.get(), "parametro":parametro.get(), "fabricante":fabricante.get()}}
            Colection_1.update_one(id_buscar,nuevosValores)
            tipo.delete(0,END)
            producto.delete(0,END)
            parametro.delete(0,END)
            fabricante.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else :
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
def mostrar_datos(tipo="", producto="", parametro="", fabricante=""):
    Objeto_Buscar = {}
    if len(tipo) != 0:
        Objeto_Buscar["tipo"] = tipo
    if len(producto) != 0:
        Objeto_Buscar["producto"] = producto
    if len(parametro) != 0:
        Objeto_Buscar["parametro"] = parametro
    if len(fabricante) != 0:
        Objeto_Buscar["fabricante"] = fabricante
    
    try:
        # Limpiar la tabla antes de llenarla
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)

        # Insertar los datos de MongoDB en la tabla
        for documento in Colection_1.find(Objeto_Buscar):
            tabla.insert('', 0, text=str(documento["_id"]),
                         values=(documento["tipo"], documento["producto"], documento["parametro"], 
                                 documento["fabricante"],))
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print(f"Error: Tiempo excedido - {errorTiempo}")
    except pymongo.errors.ConnectionFailure as errorConexion:
        print(f"Error: Fallo al conectarse a MongoDB - {errorConexion}")
def crearRegistro():
    if (tipo.get())!=0 and len(producto.get())!=0 and len(parametro.get())!=0 and len(fabricante.get())!=0:
        try:
            documento = {"tipo":tipo.get(), "producto":producto.get(), "parametro":parametro.get(), "fabricante":fabricante.get()}
            Colection_1.insert_one(documento)
            tipo.delete(0,END)
            producto.delete(0,END)
            parametro.delete(0,END)
            fabricante.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
def dobleClickTabla(event):
    global ID_SENSOR
    ID_SENSOR = str(tabla.item(tabla.selection())["text"])
    documento = Colection_1.find({"_id":ObjectId(ID_SENSOR)})[0]
    tipo.delete(0,END)
    tipo.insert(0,documento["tipo"])
    producto.delete(0,END)
    producto.insert(0,documento["producto"])
    parametro.delete(0,END)
    parametro.insert(0,documento["parametro"])
    fabricante.delete(0,END)
    fabricante.insert(0,documento["fabricante"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    borrar["state"] = "normal"
def BorrarRegistro():
    global ID_SENSOR
    try:
        id_buscar = {"_id":ObjectId(ID_SENSOR)}
        Colection_1.delete_one(id_buscar)
        tipo.delete(0,END)
        producto.delete(0,END)
        parametro.delete(0,END)
        fabricante.delete(0,END)    
    except pymongo.errors.ConnectionFailure as error:
        print (error)
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
    mostrar_datos()
def buscarRegistro():
    mostrar_datos(buscar_tipo.get(), buscar_producto.get(), buscar_parametro.get(), buscar_fabricante.get())

ventana = Tk()
tabla = ttk.Treeview(ventana, columns=("col1", "col2", "col3", "col4"))
tabla.grid(row=1, column=0, columnspan=7)

# Encabezados de la tabla
tabla.heading("#0", text="ID")
tabla.heading("col1", text="Tipo")
tabla.heading("col2", text="Producto")
tabla.heading("col3", text="Parametro")
tabla.heading("col4", text="Fabricante")
# Ajustar columnas opcionalmente
tabla.column("#0", width=200)  # Ajustar la anchura del ID
tabla.column("col1", width=100)
tabla.column("col2", width=100)
tabla.column("col3", width=100)
tabla.column("col4", width=150)

tabla.bind("<Double-Button-1>",dobleClickTabla)
#Nombre
Label(ventana, text="Tipo").grid(row=2,column=0,sticky=W+E)
tipo = Entry(ventana)
tipo.grid(row=2,column=1,sticky=W+E)
#Producto
Label(ventana, text="Producto").grid(row=3,column=0,sticky=W+E)
producto = Entry(ventana)
producto.grid(row=3,column=1,sticky=W+E)
#Valor Recomendado
Label(ventana, text="Valor Recomendado").grid(row=4,column=0,sticky=W+E)
parametro = Entry(ventana)
parametro.grid(row=4,column=1,sticky=W+E)
#Fabricante
Label(ventana, text="Fabricante").grid(row=5,column=0,sticky=W+E)
fabricante = Entry(ventana)
fabricante.grid(row=5,column=1,sticky=W+E)
#Boton crear
crear = Button(ventana, text="Agregar Sensor", command=crearRegistro, bg="green", fg="white")
crear.grid(row=9,columnspan=2,sticky=W+E)
#Boton editar
editar = Button(ventana, text="Editar Sensor", command=EditarRegistro, bg="yellow")
editar.grid(row=10,columnspan=2,sticky=W+E)
editar["state"] = "disabled"
#Boton borrar
borrar = Button(ventana, text="Borrar Sensor", command=BorrarRegistro, bg="red",fg="white")
borrar.grid(row=11,columnspan=2,sticky=W+E)
borrar["state"] = "disabled"
#Buscar Tipo
Label(ventana, text="Buscar por Tipo").grid(row=12,column=0,sticky=W+E)
buscar_tipo = Entry(ventana)
buscar_tipo.grid(row=12,column=1,sticky=W+E)
buscar_tipo.focus()
#Buscar Producto
Label(ventana, text="Buscar por Producto").grid(row=13,column=0,sticky=W+E)
buscar_producto = Entry(ventana)
buscar_producto.grid(row=13,column=1,sticky=W+E)
#Buscar Telefono
Label(ventana, text="Buscar por Parametro Minimo").grid(row=14,column=0,sticky=W+E)
buscar_parametro = Entry(ventana)
buscar_parametro.grid(row=14,column=1,sticky=W+E)
#Buscar Fabricante
Label(ventana, text="Buscar por Fabrincante").grid(row=15,column=0,sticky=W+E)
buscar_fabricante = Entry(ventana)
buscar_fabricante.grid(row=15,column=1,sticky=W+E)
#Boton buscar
buscar = Button(ventana, text="Buscar sensores", command=buscarRegistro, bg="blue", fg="white")
buscar.grid(row=19,columnspan=2,sticky=W+E)

mostrar_datos()
ventana.mainloop()