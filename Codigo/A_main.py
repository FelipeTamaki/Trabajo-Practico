from D_leer_csv import *
from F_grafos import *
from Z_validaciones import *
import tkinter as tk

def limpiar_ventana(): # Hace que se borren los widgets del menu para que cambie lo que ve el usuario en su seleccion
    for widget in menu.winfo_children():
        widget.destroy()

def volver_al_menu(): # Cuando termina la solicitud vuelve para comenzar nuevamente hasta que se cierre el mismo
    limpiar_ventana()
    tk.Button(menu, text="Solicitudes automáticas", command=solicitudes_automaticas,font=("Helvetica",14)).pack(pady=5)
    tk.Button(menu, text="Solicitud manual", command=solicitud_manual,font=("Helvetica",14)).pack(pady=5)

def solicitudes_automaticas(): # Realiza todas las solicitudes que encuentre dentro del archivo solicitudes
    solicitudes = leer_solicitudes("solicitudes.csv")
    KPI_solicitudes(solicitudes)

def solicitud_manual(): # Realiza la solicitud que ingrese el usuario 
    limpiar_ventana()
    tk.Label(menu, text="Ingrese la carga (número positivo):",font=("Helvetica",14)).pack(pady=5)
    entry_carga = tk.Entry(menu)
    entry_carga.pack()

    def siguiente_origen():
        try:
            carga = float(entry_carga.get())
            if carga <= 0:
                raise ValueError
        except:
            tk.Label(menu, text="Carga inválida. Ingrese un número válido.", fg="red",font=("Helvetica",14)).pack()
            return
        pedir_origen(carga)

    tk.Button(menu, text="Siguiente", command=siguiente_origen,font=("Helvetica",14)).pack(pady=5)

def pedir_origen(carga): # Pide el origen al usuario
    limpiar_ventana()
    tk.Label(menu, text="Seleccione el origen:",font=("Helvetica",14)).pack(pady=5)

    opciones_origen = list(Nodo.dict_nodos.keys())
    origen_var = tk.StringVar(menu)
    origen_var.set(opciones_origen[0]) 
    option_menu_origen = tk.OptionMenu(menu, origen_var, *opciones_origen)
    option_menu_origen.pack()

    def siguiente_destino():
        origen = origen_var.get()
        pedir_destino(carga, origen)

    tk.Button(menu, text="Siguiente", command=siguiente_destino,font=("Helvetica",14)).pack(pady=5)

def pedir_destino(carga, origen): # Pide el destino sabiendo el origen
    limpiar_ventana()
    tk.Label(menu, text=f"Seleccione el destino (desde {origen}):",font=("Helvetica",14)).pack(pady=5)

    # Lista de nodos excepto el origen
    opciones_destino = [n for n in Nodo.dict_nodos if n != origen]

    if not opciones_destino:
        tk.Label(menu, text="No hay destinos disponibles desde este origen", fg="red",font=("Helvetica",14)).pack()
        return

    destino_var = tk.StringVar(menu)
    destino_var.set(opciones_destino[0])  # valor por defecto
    option_menu_destino = tk.OptionMenu(menu, destino_var, *opciones_destino)
    option_menu_destino.pack()

    def calcularKPI(): # Calcula el KPI con los datos que proporciono el usuario
        destino = destino_var.get()
        limpiar_ventana()
        KPI(origen, destino, carga)
        tk.Label(menu, text="Solicitud procesada correctamente.",font=("Helvetica",14)).pack(pady=10)
        tk.Button(menu, text="Volver al menú principal", command=volver_al_menu,font=("Helvetica",14)).pack(pady=5)

    tk.Button(menu, text="Calcular KPIs", command=calcularKPI, font=("Helvetica",14)).pack(pady=5)

# ESTAS FUNCIONES SON LAS QUE SE UTILIZAN PARA CAMBIAR LOS DATOS QUE SE ANALIZAN
try:
    crear_nodos("nodos.csv")
    try:
        crear_conexiones("conexiones.csv")
    except FileNotFoundError:
        print("No se encontro el archivo de conexiones")
        raise
    except ValueError as e:
        print(e)
except FileNotFoundError:
    print("No se encontro el archivo de nodos")
    raise 
except ValueError as e:
    print(e)
else:
    menu = tk.Tk()
    menu.title("Menú interactivo")
    menu.geometry("300x140")

    # Menú principal
    try:
        tk.Button(menu, text="Solicitudes automáticas", command=solicitudes_automaticas,font=("Helvetica",14)).pack(pady=5)
        tk.Button(menu, text="Solicitud manual", command=solicitud_manual, font=("Helvetica",14)).pack(pady=5)

        menu.mainloop()
    except ValueError as e:
        print(e)

# VER COMO HACEMOS LO DE LOS GRAFICOS CUANDO TE LOS MUESTRA