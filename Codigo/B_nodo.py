# Este archivo es para todo lo relacionado con la creacion de la clase nodo
from C_conexion import Conexion

class Nodo():
    dict_nodos = {}
    nodos = set()
    def __init__(self, nombre:str):
        self.nombre=nombre
        self.grafos= {"Automotor":set(),"Ferroviaria":set(),"Fluvial":set(),"Aerea":set()}
        Nodo.dict_nodos[self.nombre] = self
        Nodo.nodos.add(self)

    def __repr__(self):
        return f'{self.nombre}'
    
    def agregarConexion(self,conexion):
        if not isinstance(conexion, Conexion):
            raise TypeError (f'Error de tipo: se esperaba una clase de tipo Conexion y se dio uno {type(conexion)}')
        self.grafos[conexion.tipo].add(conexion)
    
    @classmethod
    def imprimirNodos(cls):
        for nodo in cls.nodos:
            print(f"{nodo.nombre}: ")
            for tipo, conexiones in nodo.grafos.items():
                print(f"{tipo}: ")
                for conexion in conexiones:
                    print(conexion)