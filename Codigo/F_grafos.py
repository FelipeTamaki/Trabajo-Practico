# Este archivo es para que hagamos el algoritmo de Dijkstra de los de tipo fluvial (una vez que hacemos tel de todos los tipos vemos cual es el mejor)
from math import ceil
from C_conexion import Conexion
from B_nodo import Nodo

# Costos y carateristicas de cada transporte
automotor = {"Modo":"Automotor", "Costo Fijo":30,"Velocidad":80, "Capacidad":30000,"Costo km":5, "Costo kg": [1,2]}
tren = {"Modo":"Ferroviario","Costo Fijo":100, "Velocidad":100, "Capacidad":150000, "Costo km":[15,20],"Costo kg":3}
barco = {"Modo":"Fluvial","Costo Fijo": [500,1500], "Velocidad": 40, "Capacidad":100000, "Costo km":15, "Costo kg":2}
avion = {"Modo":"Aerea", "Costo Fijo":750,"Velocidad":[600,400], "Capacidad":5000,"Costo km":40, "Costo kg": 10}
    
def KPIcosto(origen,destino, carga):
    for nodo in Nodo.nodos: 
        if nodo.nombre==origen:
            for tipo, conexiones in nodo.grafos.items():
                valores={}
                for conexion in conexiones:
                    costo = 0
                    if tipo == "Automotor":
                        if carga >= 15000: #Ver si el costo por km es 1 o 2
                            costo_kg=automotor["Costo kg"][1]
                        else:
                            costo_kg=automotor["Costo kg"][0]

                        if conexion.restriccion:
                            divisor = conexion.valor_restriccion
                        else:
                            divisor = automotor["Capacidad"]
                        cantidad=ceil(carga/divisor)
                        costo=cantidad*(automotor["Costo km"]*conexion.distancia+automotor["Costo Fijo"])+costo_kg*carga
                        
                    elif tipo == "Ferroviario":
                        if conexion.distancia >= 200: # Ver si la distancia es mayor a 200
                            costo_km = tren["Costo km"][1]
                        else:
                            costo_km = tren ["Costo km"][0]
                        cantidad=ceil(carga/tren["Capacidad"])
                        costo=cantidad*(costo_km*conexion.distancia+tren["Costo Fijo"])+tren["Costo kg"]*carga            
                    
                    elif tipo == "Fluvial":
                        if conexion.restriccion:
                            costo_fijo=barco["Costo Fijo"][1]
                        else:
                            costo_fijo=barco["Costo Fijo"][0]
                        cantidad=ceil(carga/barco["Capacidad"])
                        costo=cantidad*(barco["Costo km"]*conexion.distancia+costo_fijo)+barco["Costo kg"]*carga

                    elif tipo == "Aerea":
                        cantidad= ceil(carga/avion["Capacidad"])
                        costo = cantidad *( avion["Costo Fijo"]+  avion["Costo km"]*conexion.distancia)+ carga*avion["Costo kg"]
                    valores[f"{conexion.origen}-{conexion.destino}"]=costo
                    print(valores)