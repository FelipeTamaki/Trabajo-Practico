#FALTA HACER LO DEL COSTO X CAMION --> Restriccion cargas
#CORREGIR SINTAXIS

# Este archivo es para que hagamos el algoritmo de Dijkstra de los de tipo fluvial (una vez que hacemos tel de todos los tipos vemos cual es el mejor)
from math import ceil
from C_conexion import Conexion 
from B_nodo import Nodo
from E_datos_transportes import Transporte, Aereo, Ferroviario, Automotor, Fluvial
    
def KPIcosto(origen,destino, carga):
    camion=Automotor()
    tren=Ferroviaria()
    
    for nodo in Nodo.nodos: 
        if nodo.nombre==origen:
            for tipo, conexiones in nodo.grafos.items():
                valores={}
                for conexion in conexiones:
                    costo = 0
                    if tipo == "Automotor":
                        camion.calcular_costo(conexion,carga)
                        
                        
                    elif tipo == "Ferroviario":
                        tren.calcular_costo(co)
                        
                    elif tipo == "Fluvial":
                        .

                    elif tipo == "Aerea":
                        

                    valores[f"{conexion.origen}-{conexion.destino}"]=costo
                    print(valores)
