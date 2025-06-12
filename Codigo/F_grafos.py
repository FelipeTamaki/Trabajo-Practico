from math import ceil
from C_conexion import Conexion
from B_nodo import Nodo
from E_datos_transportes import Transporte, Aereo, Ferroviario, Automotor, Fluvial
from datetime import timedelta
import networkx as nx

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
        costo, camino= dijkstra(grafo, origen, destino)
        transporte = obtener_transporte(tipo)
        costo_carga=costo_carga_total(camino,carga,tipo,transporte)
        costo_total = costo + costo_carga
        tiempo=calcular_tiempo_total(camino,tipo, valores_tiempo)

        if costo_total < costo_minimo:
            costo_minimo = costo_total
            camino_minimo = camino
            tipo_minimo = tipo
            tiempo_minimo=tiempo
    
    print(obtener_datos_acumulados(camino_minimo,tipo,carga,valores_costo,valores_tiempo))
    camino_str = "-".join(camino_minimo)
    print(f"\nCosto mínimo:")
    print(f"Medio de transporte: {tipo_minimo}\nItinerario: {camino_str}\nCosto total: ${costo_minimo}\nTiempo esperado: {tiempo_minimo}")
    
    # Tiempo mínimo
    tiempo_minimo = float("inf")
    camino_minimo = []
    tipo_minimo = ""
    for tipo, conexiones in valores_tiempo.items():
        transporte = obtener_transporte(tipo)
        grafo = construir_grafo(valores_tiempo[tipo])
        tiempo, camino = dijkstra(grafo, origen, destino)
        costo=calcular_costo_total(camino,tipo,valores_costo)
        costo_carga=costo_carga_total(camino,carga,tipo,transporte)
        costo_total = costo + costo_carga
        if tiempo < tiempo_minimo:
            tiempo_minimo = tiempo
            camino_minimo = camino
            tipo_minimo = tipo
            costo_minimo=costo_total
    
    total_segundos = int(tiempo_minimo * 3600)
    duracion = timedelta(seconds=total_segundos)

    camino_str = "-".join(camino_minimo)
    print(f"\nTiempo mínimo:")
    print(f"Medio de transporte: {tipo_minimo}\nItinerario: {camino_str}\nTiempo total: {duracion}\nCosto total: ${costo_minimo}")

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

def calcular_tiempo_total(camino, tipo, valores_tiempo):
    tiempo_total = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]
        key = f"{origen}-{destino}"
        key_inv = f"{destino}-{origen}"
        tiempo = valores_tiempo[tipo].get(key) or valores_tiempo[tipo].get(key_inv)
        if tiempo:
            tiempo_total += tiempo
    return timedelta(seconds=int(tiempo_total * 3600))

def calcular_costo_total(camino, tipo, valores_costo):
    costo_total = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]
        key = f"{origen}-{destino}"
        key_inv = f"{destino}-{origen}"
        costo = valores_costo[tipo].get(key) or valores_costo[tipo].get(key_inv)
        if costo:
            costo_total += costo
    return costo_total

def costo_carga_total(camino,carga,tipo,transporte):
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
    return costo_carga_total

def obtener_datos_acumulados(camino, tipo, carga, valores_costo, valores_tiempo):
    distancias_acumuladas = [0]
    tiempos_acumulados = [0]
    costos_acumulados = [0]

    distancia_total = 0
    tiempo_total = 0
    costo_total = 0

    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]
        key = f"{origen}-{destino}"
        key_inv = f"{destino}-{origen}"
    
        for conexion in Conexion.conexiones:
            if (conexion.origen.nombre == origen and conexion.destino.nombre == destino) or (conexion.origen.nombre == destino and conexion.destino.nombre == origen) and conexion.tipo.nombre == tipo:
                distancia=conexion.distancia_km
        print(distancia)
        # Tiempo
        tiempo = valores_tiempo[tipo].get(key) or valores_tiempo[tipo].get(key_inv) or 0
        print(tiempo)
        # Costo
        costo = valores_costo[tipo].get(key) or valores_costo[tipo].get(key_inv) or 0
        print(costo)
        # Acumular
        distancia_total += distancia
        tiempo_total += tiempo
        costo_total += costo

        distancias_acumuladas.append(distancia_total)
        tiempos_acumulados.append(tiempo_total)
        costos_acumulados.append(costo_total)

    return distancias_acumuladas, tiempos_acumulados, costos_acumulados

def KPI_solicitudes(diccionario_solicitudes):
    for key in diccionario_solicitudes.keys(): # obtiene el id del pedido
        print(f'Posbles rutas para el pedido {key}')
        carga = diccionario_solicitudes[key]["peso_kg"]
        origen = diccionario_solicitudes[key]["origen"]
        destino = diccionario_solicitudes[key]["destino"]
        KPI(origen, destino, carga) # luego de extraer una solicitud del archivo csv, calcula su kpi de costo y tiempo