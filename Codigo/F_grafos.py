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
    costo_minimo=float("inf") 
    camino_minimo=[]  
    tipo_minimo = ""       
    for tipo, conexiones in valores.items():
        grafo=construir_grafo(valores[tipo])
        costo, camino=dijkstra(grafo,origen,destino)
        print(costo,camino,tipo)
        if costo_minimo>costo:
            costo_minimo=costo
            camino_minimo=camino
            tipo_minimo=tipo

    camino=""
    for ciudad in camino_minimo:
        camino+=ciudad +"-"
         
    print(f"Modo: {tipo_minimo}\nItinerario: {camino}\nCosto total: {costo_minimo}")
    
def KPItiempo(origen, destino, carga):
    pass


def construir_grafo(transporte):
    grafo = {} 
    for trayecto in transporte:
        origen, destino = trayecto.split("-")
        costo = transporte[trayecto]

        if origen not in grafo:
            grafo[origen] = []
        if destino not in grafo:
            grafo[destino] = []

        grafo[origen].append((destino, costo))
        grafo[destino].append((origen, costo)) 
    return grafo

def dijkstra(grafo, inicio, fin):
    nodos = list(grafo.keys())
    costos = {n: float('inf') for n in nodos}
    if fin not in nodos:
        return float('inf'),"No se puede llegar con ese modo de transporte"
    anteriores = {}
    visitados = []

    costos[inicio] = 0

    while nodos:
        actual = None
        for nodo in nodos:
            if nodo not in visitados and (actual is None or costos[nodo] < costos[actual]):
                actual = nodo

        if actual is None:
            return 

        visitados.append(actual)
        nodos.remove(actual)

        for vecino, costo in grafo[actual]:
            nuevo_costo = costos[actual] + costo
            if nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                anteriores[vecino] = actual
    camino = []
    actual = fin
    while actual in anteriores:
        camino.insert(0, actual)
        actual = anteriores[actual]
    if camino:
        camino.insert(0, inicio)

    return costos[fin], camino

# inicio = "A"
# fin = "D"
# mejor_costo = float('inf')
# mejor_transporte = None
# mejor_camino = []

# for medio, trayectos in valores.items():
#     grafo = construir_grafo(trayectos)
#     costo, camino = dijkstra(grafo, inicio, fin)

#     print(f"{medio}: costo = {costo}, camino = {camino}")

#     if costo < mejor_costo:
#         mejor_costo = costo
#         mejor_transporte = medio
#         mejor_camino = camino


# print(f"Mejor medio de transporte: {mejor_transporte}: costo = {mejor_costo}, camino = {mejor_camino}")
