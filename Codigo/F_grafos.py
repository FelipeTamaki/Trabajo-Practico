from math import ceil
from C_conexion import Conexion
from B_nodo import Nodo
from E_datos_transportes import Transporte, Aereo, Ferroviario, Automotor, Fluvial

def KPI(origen, destino, carga):
    camion = Automotor()
    tren = Ferroviario()
    barco = Fluvial()
    avion = Aereo()

    valores_costo = {"Automotor": {}, "Ferroviaria": {}, "Fluvial": {}, "Aerea": {}}
    valores_tiempo = {"Automotor": {}, "Ferroviaria": {}, "Fluvial": {}, "Aerea": {}}

    for nodo in Nodo.nodos:
        for tipo, conexiones in nodo.grafos.items():
            for conexion in conexiones:
                if tipo == "Automotor":
                    costo = camion.calcular_costo_trayecto(conexion, carga)
                    tiempo = camion.calcular_tiempo(conexion)
                elif tipo == "Ferroviaria":
                    costo = tren.calcular_costo_trayecto(conexion, carga)
                    tiempo = tren.calcular_tiempo(conexion)
                elif tipo == "Fluvial":
                    costo = barco.calcular_costo_trayecto(conexion, carga)
                    tiempo = barco.calcular_tiempo(conexion)
                elif tipo == "Aerea":
                    costo = avion.calcular_costo_trayecto(conexion, carga)
                    tiempo = avion.calcular_tiempo(conexion)
                else:
                    continue
                valores_costo[tipo][f"{conexion.origen}-{conexion.destino}"] = costo
                valores_tiempo[tipo][f"{conexion.origen}-{conexion.destino}"] = tiempo

    # Costo mínimo
    costo_minimo = float("inf")
    camino_minimo = []
    tipo_minimo = ""

    for tipo, conexiones in valores_costo.items():
        grafo = construir_grafo(valores_costo[tipo])
        costo, camino = dijkstra(grafo, origen, destino)
        transporte = obtener_transporte(tipo)

        if not isinstance(camino, list):
            continue
        print(costo)
        if tipo == "Automotor":
            capacidad_efectiva = transporte.capacidad
            for i in range(len(camino) - 1):
                origen_conexion, destino_conexion = camino[i], camino[i + 1]
                for conexion in Conexion.conexiones:
                    if ((conexion.origen == origen_conexion and conexion.destino == destino_conexion) or
                        (conexion.origen == destino_conexion and conexion.destino == origen_conexion)) and conexion.tipo == tipo:
                        if conexion.restriccion:
                            capacidad_efectiva = min(capacidad_efectiva, int(conexion.valor_restriccion))
            costo_carga_total = transporte.calcular_costo_total_carga(carga, capacidad_efectiva)
        else:
            costo_carga_total = transporte.calcular_costo_total_carga(carga)
    
        costo_total = costo + costo_carga_total
        print(costo_total)

        if costo_total < costo_minimo:
            costo_minimo = costo_total
            camino_minimo = camino
            tipo_minimo = tipo

    camino_str = "-".join(camino_minimo)
    print(f"\nCosto mínimo:")
    print(f"Modo: {tipo_minimo}\nItinerario: {camino_str}\nCosto total: {costo_minimo}")

    # Tiempo mínimo
    tiempo_minimo = float("inf")
    camino_minimo = []
    tipo_minimo = ""
    for tipo, conexiones in valores_tiempo.items():
        grafo = construir_grafo(valores_tiempo[tipo])
        tiempo, camino = dijkstra(grafo, origen, destino)
        if not isinstance(camino, list):
            continue
        if tiempo < tiempo_minimo:
            tiempo_minimo = tiempo
            camino_minimo = camino
            tipo_minimo = tipo

    camino_str = "-".join(camino_minimo)
    print(f"\nTiempo mínimo:")
    print(f"Modo: {tipo_minimo}\nItinerario: {camino_str}\nTiempo total: {tiempo_minimo}")

def construir_grafo(transporte):
    grafo = {}
    for trayecto in transporte:
        origen, destino = trayecto.split("-")
        costo = transporte[trayecto]
        grafo.setdefault(origen, []).append((destino, costo))
        grafo.setdefault(destino, []).append((origen, costo))
    return grafo

def dijkstra(grafo, inicio, fin):
    nodos = list(grafo.keys())
    costos = {nodo: float('inf') for nodo in grafo} # Hace que inicialmente todos esten en infinito
    anteriores = {} 
    visitados = [] # Una vez que visitemos cada nodo se va a agregar aca para saber que ya sabemos como llegar a ese nodo de la forma minima
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
        for vecino, costo_conexion in grafo.get(actual, []):
            nuevo_costo = costos[actual] + costo_conexion
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

    return costos.get(fin, float('inf')), camino

def obtener_transporte(tipo):
    if tipo == "Automotor":
        return Automotor()
    elif tipo == "Ferroviaria":
        return Ferroviario()
    elif tipo == "Fluvial":
        return Fluvial()
    elif tipo == "Aerea":
        return Aereo()
