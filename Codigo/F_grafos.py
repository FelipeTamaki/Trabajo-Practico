# Este archivo es para que hagamos el algoritmo de Dijkstra de los de tipo fluvial (una vez que hacemos tel de todos los tipos vemos cual es el mejor)

from C_conexion import Conexion
from B_nodo import Nodo

# Costos y carateristicas de cada transporte
auto = {"Costo Fiijo":30,"Velocidad":80, "Capacidad":30000,"Costo km":5, }
tren = {"Costo Fijo":100, "Velocidad":100, "Capacidad":150000, "Costo km":20,
barco = {"Costo fijo": , ""}
avion = {}


def KPIcosto(origen,destino, carga):
    for nodo in Nodo.nodos: 
        if nodo.nombre==origen:
            for tipo, conexiones in nodo.grafos.items():
                
            
    

def KPItiempo(origen, destino, carga):
    