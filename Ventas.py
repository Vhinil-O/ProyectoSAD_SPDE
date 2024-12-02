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
MONGO_COLECTION_1 = "Ventas"
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OUT)
BaseDatos = client[MONGO_BASEDATOS]
Colection_1 = BaseDatos[MONGO_COLECTION_1]
ID_VENTA = ""

def EditarRegistro ():
    global ID_VENTA
    if (cliente.get())!=0 and len(producto.get())!=0 and len(cantidad.get())!=0 and len(fecha.get())!=0:
        try:
            id_buscar = {"_id":ObjectId(ID_VENTA)}
            nuevosValores = {"$set":{"cliente":cliente.get(),"producto":producto.get(), "cantidad":cantidad.get(), "fecha":fecha.get()}}
            Colection_1.update_one(id_buscar,nuevosValores)
            cliente.delete(0,END)
            producto.delete(0,END)
            cantidad.delete(0,END)
            fecha.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else :
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
def mostrar_datos(cliente="", producto="", cantidad="", fecha=""):
    Objeto_Buscar = {}
    if len(cliente) != 0:
        Objeto_Buscar["cliente"] = cliente
    if len(producto) != 0:
        Objeto_Buscar["producto"] = producto
    if len(cantidad) != 0:
        Objeto_Buscar["cantidad"] = cantidad
    if len(fecha) != 0:
        Objeto_Buscar["fecha"] = fecha
    
    try:
        # Limpiar la tabla antes de llenarla
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)

        # Insertar los datos de MongoDB en la tabla
        for documento in Colection_1.find(Objeto_Buscar):
            tabla.insert('', 0, text=str(documento["_id"]),
                         values=(documento["cliente"], documento["producto"], documento["cantidad"], documento["fecha"]))
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print(f"Error: Tiempo excedido - {errorTiempo}")
    except pymongo.errors.ConnectionFailure as errorConexion:
        print(f"Error: Fallo al conectarse a MongoDB - {errorConexion}")
def crearRegistro():
    if (cliente.get())!=0 and len(producto.get())!=0 and len(cantidad.get())!=0 and len(fecha.get())!=0:
        try:
            documento = {"cliente":cliente.get(),"producto":producto.get(), "cantidad":cantidad.get(), "fecha":fecha.get()}
            Colection_1.insert_one(documento)
            cliente.delete(0,END)
            producto.delete(0,END)
            cantidad.delete(0,END)
            fecha.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print (error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrar_datos()
def dobleClickTabla(event):
    global ID_VENTA
    ID_VENTA = str(tabla.item(tabla.selection())["text"])
    documento = Colection_1.find({"_id":ObjectId(ID_VENTA)})[0]
    cliente.delete(0,END)
    cliente.insert(0,documento["cliente"])
    producto.delete(0,END)
    producto.insert(0,documento["producto"])
    cantidad.delete(0,END)
    cantidad.insert(0,documento["cantidad"])
    fecha.delete(0,END)
    fecha.insert(0,documento["fecha"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    borrar["state"] = "normal"
def BorrarRegistro():
    global ID_VENTA
    try:
        id_buscar = {"_id":ObjectId(ID_VENTA)}
        Colection_1.delete_one(id_buscar)
        cliente.delete(0,END)
        producto.delete(0,END)
        cantidad.delete(0,END)
        fecha.delete(0,END)    
    except pymongo.errors.ConnectionFailure as error:
        print (error)
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"
    mostrar_datos()
def buscarRegistro():
    mostrar_datos(buscar_cliente.get(), buscar_producto.get(), buscar_cantidad.get(), buscar_fecha.get())

ventana = Tk()
tabla = ttk.Treeview(ventana, columns=("col1", "col2", "col3", "col4"))
tabla.grid(row=1, column=0, columnspan=7)

# Encabezados de la tabla
tabla.heading("#0", text="ID")
tabla.heading("col1", text="Cliente")
tabla.heading("col2", text="Producto")
tabla.heading("col3", text="Cantidad")
tabla.heading("col4", text="Fecha")

# Ajustar columnas opcionalmente
tabla.column("#0", width=200) 
tabla.column("col1", width=100)
tabla.column("col2", width=100)
tabla.column("col3", width=100)
tabla.column("col4", width=100)

tabla.bind("<Double-Button-1>",dobleClickTabla)
#Cliente
Label(ventana, text="Cliente").grid(row=2,column=0,sticky=W+E)
cliente = Entry(ventana)
cliente.grid(row=2,column=1,sticky=W+E)
#Producto
Label(ventana, text="Producto").grid(row=3,column=0,sticky=W+E)
producto = Entry(ventana)
producto.grid(row=3,column=1,sticky=W+E)
#Cantidad
Label(ventana, text="Cantidad").grid(row=4,column=0,sticky=W+E)
cantidad = Entry(ventana)
cantidad.grid(row=4,column=1,sticky=W+E)
#Fecha
Label(ventana, text="Fecha").grid(row=5,column=0,sticky=W+E)
fecha = Entry(ventana)
fecha.grid(row=5,column=1,sticky=W+E)
#Boton crear
crear = Button(ventana, text="Agregar Producto", command=crearRegistro, bg="green", fg="white")
crear.grid(row=6,columnspan=2,sticky=W+E)
#Boton editar
editar = Button(ventana, text="Editar Producto", command=EditarRegistro, bg="yellow")
editar.grid(row=7,columnspan=2,sticky=W+E)
editar["state"] = "disabled"
#Boton borrar
borrar = Button(ventana, text="Borrar Producto", command=BorrarRegistro, bg="red",fg="white")
borrar.grid(row=8,columnspan=2,sticky=W+E)
borrar["state"] = "disabled"
#Buscar cliente
Label(ventana, text="Buscar por cliente").grid(row=9,column=0,sticky=W+E)
buscar_cliente = Entry(ventana)
buscar_cliente.grid(row=9,column=1,sticky=W+E)
buscar_cliente.focus()
#Buscar producto
Label(ventana, text="Buscar por producto").grid(row=10,column=0,sticky=W+E)
buscar_producto = Entry(ventana)
buscar_producto.grid(row=10,column=1,sticky=W+E)
#Buscar cantidad
Label(ventana, text="Buscar por cantidad").grid(row=11,column=0,sticky=W+E)
buscar_cantidad = Entry(ventana)
buscar_cantidad.grid(row=11,column=1,sticky=W+E)
#Buscar fecha
Label(ventana, text="Buscar por fecha").grid(row=12,column=0,sticky=W+E)
buscar_fecha = Entry(ventana)
buscar_fecha.grid(row=12,column=1,sticky=W+E)

#Boton buscar
buscar = Button(ventana, text="Buscar sensores", command=buscarRegistro, bg="blue", fg="white")
buscar.grid(row=13,columnspan=2,sticky=W+E)

mostrar_datos()
ventana.mainloop()