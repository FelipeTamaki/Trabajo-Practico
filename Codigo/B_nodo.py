# Este archivo es para todo lo relacionado con la creacion de la clase nodo

class Nodo:
    NODOS = set()  # Hace que no se repitan nodos
    DICT_NODOS = {} # Se usa para buscarlos cuando se "crean" las conexiones

    IMPRIMIR = set() # esta es solo de prueba para imprimir los nodos

    def __init__(self, nombre: str): # Crea el nodo/ciudad y al principio no tiene conexiones
        if not isinstance(nombre, str):
            raise TypeError(f"Error de tipo: se esperaba un objeto de tipo str y se proporciono uno de tipo {type(nombre)} para la variable nombre")
        if nombre in Nodo.NODOS:
            raise ValueError(f"Ya existe un nodo con el nombre '{nombre}'")
        self.nombre = nombre
        self.conexiones = []  # Lista de las vias conectadas al nodo
        self.tipos = set()  # Redes que pueden llegar al nodo
        Nodo.NODOS.add(nombre)
        Nodo.DICT_NODOS[nombre] = self
        Nodo.IMPRIMIR.add(self)

    def agregar_conexion(self, conexion): # Se crea una conexion con otro nodo mediante un objeto via
        self.conexiones.append(conexion)
        self.tipos.add(conexion.tipo)

    def __str__(self):
        return f"Nombre: {self.nombre} Redes: {(self.tipos)}"

    @classmethod
    def imprimir_nodos(cls): # Prueba
        for nodo in cls.IMPRIMIR:
            print(nodo)

