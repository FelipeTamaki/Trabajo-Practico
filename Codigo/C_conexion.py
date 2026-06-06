# Este archivo se encaga de todo lo relacionado a la creación de conexiones
class Conexion():
    conexiones = set()
    def __init__(self,origen:str,destino:str,tipo:str,distancia_km:int,restriccion,valor_restriccion):
        self.origen=origen
        self.destino=destino
        self.tipo=tipo
        self.distancia_km=distancia_km
        self.restriccion=restriccion
        self.valor_restriccion=valor_restriccion
        Conexion.conexiones.add(self)
        self.conectar()

    def __repr__(self):
        if self.restriccion == "":
            return f" Origen:{self.origen}, Destino:{self.destino}, Tipo:{self.tipo}, Distancia_km:{self.distancia_km}, Restriccion: Ninguna"
        else:           
            return f" Origen:{self.origen}, Destino:{self.destino}, Tipo:{self.tipo}, Distancia_km:{self.distancia_km}, Restriccion:{self.restriccion}, Valor_restriccion:{self.valor_restriccion}"
        
    def conectar(self): 
        """
        Conecta ambos nodos (origen y destino) a la conexion
        """
        
        self.origen.agregarConexion(self)
        self.destino.agregarConexion(self)
    
    def getOrigen(self):
        return self.origen

    def getDestino(self):
        return self.destino

    def getTipo(self):
        return self.tipo
    @classmethod
    def imprimirConexiones(cls):
        for conex in Conexion.conexiones:
            print(conex)
            