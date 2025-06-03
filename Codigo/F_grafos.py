#FALTA HACER LO DEL COSTO X CAMION --> Restriccion cargas
#CORREGIR SINTAXIS

# Este archivo es para que hagamos el algoritmo de Dijkstra de los de tipo fluvial (una vez que hacemos tel de todos los tipos vemos cual es el mejor)
from math import ceil
from C_conexion import Conexion 
from B_nodo import Nodo
from E_datos_transportes import Transporte, Aereo, Ferroviario, Automotor, Fluvial
    
def KPIcosto(origen,destino, carga):
    
    camion=Automotor()
    tren=Ferroviario()
    barco=Fluvial()
    avion=Aereo()
    
    valores={"Automotor":{},"Ferroviaria":{},"Fluvial":{}, "Aerea":{}}
    for nodo in Nodo.nodos: 
        for tipo, conexiones in nodo.grafos.items():
            for conexion in conexiones:
                costo = 0
                if tipo == "Automotor":
                    costo = camion.calcular_costo(conexion,carga)
                if tipo == "Ferroviaria":
                    costo = tren.calcular_costo(conexion, carga)
                if tipo == "Fluvial":
                    costo=barco.calcular_costo(conexion,carga)
                if tipo == "Aerea":
                    costo=avion.calcular_costo(conexion,carga) 
                valores[tipo][f"{conexion.origen}-{conexion.destino}"]=costo
                
    for tipo, conexiones in valores.items():
        print(tipo)
        print(conexiones)
def KPItiempo(origen, destino, carga):
    pass
def dijkstra():
    pass