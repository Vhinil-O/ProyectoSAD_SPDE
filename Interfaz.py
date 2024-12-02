from tkinter import *
import subprocess  

def abrir_Empleados():
    try:
        subprocess.run(["python", "Empleados.py"])
    except FileNotFoundError:
        mensaje_error.config(text="Error: No se encuentra el archivo Empleados.py")

def abrir_Usuarios():
    try:
        subprocess.run(["python", "Usuarios.py"])
    except FileNotFoundError:
        mensaje_error.config(text="Error: No se encuentra el archivo Usuarios.py")

def abrir_Sensores():
    try:
        subprocess.run(["python", "Sensores.py"])
    except FileNotFoundError:
        mensaje_error.config(text="Error: No se encuentra el archivo Sensores.py")

def abrir_Productos():
    try:
        subprocess.run(["python", "Productos.py"])
    except FileNotFoundError:
        mensaje_error.config(text="Error: No se encuentra el archivo Sensores.py")

def abrir_Provedores():
    try:
        subprocess.run(["python", "Provedores.py"])
    except FileNotFoundError:
        mensaje_error.config(text="Error: No se encuentra el archivo Sensores.py")

def abrir_Ventas():
    try:
        subprocess.run(["python", "Ventas.py"])
    except FileNotFoundError:
        mensaje_error.config(text="Error: No se encuentra el archivo Sensores.py")

# Crear la ventana principal
ventana = Tk()
ventana.title("Menú Principal - Interfaz Gráfica")
ventana.geometry("300x350")

# Etiqueta de bienvenida
Label(ventana, text="Menú Principal", font=("Arial", 16)).pack(pady=10)

# Botón para abrir las tablas
Button(ventana, text="Abrir Gestión de Empleados", command=abrir_Empleados, bg="blue", fg="white", width=25).pack(pady=10)
Button(ventana, text="Abrir Gestión de Usuarios", command=abrir_Usuarios, bg="blue", fg="white", width=25).pack(pady=10)
Button(ventana, text="Abrir Gestión de Sensores", command=abrir_Sensores, bg="blue", fg="white", width=25).pack(pady=10)
Button(ventana, text="Abrir Gestión de Productos", command=abrir_Productos, bg="blue", fg="white", width=25).pack(pady=10)
Button(ventana, text="Abrir Gestión de Provedores", command=abrir_Provedores, bg="blue", fg="white", width=25).pack(pady=10)
Button(ventana, text="Abrir Gestión de Ventas", command=abrir_Ventas, bg="blue", fg="white", width=25).pack(pady=10)

# Mensaje de error si no se encuentra el archivo
mensaje_error = Label(ventana, text="", fg="red")
mensaje_error.pack()

# Ejecutar la interfaz
ventana.mainloop()
