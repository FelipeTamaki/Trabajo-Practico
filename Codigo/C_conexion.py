# Este archivo se encaga de todo lo relacionado a la creación de conexiones

from B_nodo import Nodo

class Conexion:
    CONEXIONES = set()
    TIPOS = {"Aerea", "Ferroviaria", "Fluvial", "Automotor"}

    def __init__(self, origen, destino, tipo:str, distancia_km: float, restriccion, valor_restriccion): # FALTA VERIFICACION DE TIPOS DE RESTRICCIONES
        if not isinstance(origen, Nodo):
            raise TypeError(f'Error de tipo: se esperaba un Nodo para origen y se recibió {type(origen)}')
        if not isinstance(destino, Nodo):
            raise TypeError(f'Error de tipo: se esperaba un Nodo para destino y se recibió {type(destino)}')
        if not isinstance(distancia_km, float) or distancia_km <= 0:
            raise ValueError(f'La distancia_km debe ser un número float positivo, no {distancia_km}')
        if tipo not in Conexion.TIPOS:
            raise ValueError(f'Tipo de transporte inválido. Debe ser uno de: {Conexion.TIPOS}')

        self.origen = origen # Validado
        self.destino = destino # Validado
        self.distancia_km = distancia_km # Validado
        self.tipo = tipo # Validado
        self.restriccion = restriccion 
        self.valor_restriccion = valor_restriccion # esto esta validado en leer_csv antes de crear cada conexion
        origen.agregar_conexion(self)
        destino.agregar_conexion(self)
        Conexion.CONEXIONES.add(self)

    def __str__(self):
        if self.restriccion == "":
            return f'Via {self.tipo} de {self.origen.nombre} a {self.destino.nombre}, {self.distancia_km} km. Restriccion: Ninguna'
        else:
            return f'Via {self.tipo} de {self.origen.nombre} a {self.destino.nombre}, {self.distancia_km} km. Restriccion: {self.restriccion} {self.valor_restriccion}'
    
    @classmethod
    def imprimir_conexiones(cls): #Prueba
        for conexion in Conexion.CONEXIONES:
            print(conexion)