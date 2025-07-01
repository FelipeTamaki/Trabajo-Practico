import tkinter as tk
from B_nodo import Nodo
from C_conexion import Conexion
from H_planificador import PlanificadorRutas
from D_leer_csv import crear_nodos, crear_conexiones, leer_solicitudes

class Menu:
    def __init__(self, m):
        self.menu = m
        self.menu.title("Menú interactivo")
        self.menu.geometry("352x145")
        self.origen_var = None
        self.destino_var = None
        self.carga = None
        self.planificador = PlanificadorRutas()
        self.inicializar_datos()
        self.volver_al_menu()

    def inicializar_datos(self):
        try:
            crear_nodos("nodos.csv")
            crear_conexiones("conexiones.csv")
        except FileNotFoundError as e:
            print(f"Error al cargar archivos: {e}")
            raise
        except ValueError as e:
            print(e)

    def limpiar_ventana(self): 
        for widget in self.menu.winfo_children():
            widget.destroy()

    def volver_al_menu(self): 
        self.limpiar_ventana()
        tk.Button(self.menu, text="Solicitudes automáticas", command=self.solicitudes_automaticas, font=("Helvetica",14)).pack(pady=5)
        tk.Button(self.menu, text="Solicitud manual", command=self.solicitud_manual, font=("Helvetica",14)).pack(pady=5)
        tk.Button(self.menu, text="Ver Estadistica", command=self.ver_estadistica_wrapper, font=("Helvetica",14)).pack(pady=5)

    def ver_estadistica_wrapper(self):
        self.limpiar_ventana()
        self.planificador.estadistica_eficiencia()
        self.volver_al_menu()

    def solicitudes_automaticas(self): 
        solicitudes = leer_solicitudes("solicitudes.csv")
        self.planificador.planificar_solicitudes(solicitudes)

    def solicitud_manual(self): 
        self.limpiar_ventana()
        tk.Label(self.menu, text="Ingrese la carga (número positivo):", font=("Helvetica",14)).pack(pady=5)
        self.carga = tk.Entry(self.menu)
        self.carga.pack()
        tk.Button(self.menu, text="Siguiente", command=self.siguiente_origen, font=("Helvetica",14)).pack(pady=5)

    def siguiente_origen(self):
        try:
            carga = float(self.carga.get())
            if carga <= 0:
                raise ValueError
        except:
            tk.Label(self.menu, text="Carga inválida. Ingrese un número válido.", fg="red", font=("Helvetica",14)).pack()
            return
        self.pedir_origen(carga)

    def pedir_origen(self, carga): 
        self.limpiar_ventana()
        tk.Label(self.menu, text="Seleccione el origen:", font=("Helvetica",14)).pack(pady=5)

        opciones_origen = list(Nodo.dict_nodos.keys())
        self.origen_var = tk.StringVar(self.menu)
        self.origen_var.set(opciones_origen[0]) 
        tk.OptionMenu(self.menu, self.origen_var, *opciones_origen).pack()
        tk.Button(self.menu, text="Siguiente", command=lambda: self.pedir_destino(carga, self.origen_var.get()), font=("Helvetica",14)).pack(pady=5)

    def pedir_destino(self, carga, origen): 
        self.limpiar_ventana()
        tk.Label(self.menu, text=f"Seleccione el destino (desde {origen}):", font=("Helvetica",14)).pack(pady=5)

        opciones_destino = [n for n in Nodo.dict_nodos if n != origen]
        if not opciones_destino:
            tk.Label(self.menu, text="No hay destinos disponibles desde este origen", fg="red", font=("Helvetica",14)).pack()
            return

        self.destino_var = tk.StringVar(self.menu)
        self.destino_var.set(opciones_destino[0]) 
        tk.OptionMenu(self.menu, self.destino_var, *opciones_destino).pack()
        tk.Button(self.menu, text="Calcular KPIs", command=lambda: self.calcularKPI(origen, self.destino_var.get(), carga), font=("Helvetica",14)).pack(pady=5)

    def calcularKPI(self, origen, destino, carga):
        self.limpiar_ventana()
        self.planificador.planificar_ruta(origen, destino, carga)
        tk.Label(self.menu, text="Solicitud procesada correctamente.", font=("Helvetica",14)).pack(pady=10)
        tk.Button(self.menu, text="Volver al menú principal", command=self.volver_al_menu, font=("Helvetica",14)).pack(pady=5)
        self.ultima_solicitud = (origen, destino, carga)
        self.volver_al_menu()