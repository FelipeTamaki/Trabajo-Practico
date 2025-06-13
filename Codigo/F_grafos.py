from math import ceil
from C_conexion import Conexion
from B_nodo import Nodo
from E_datos_transportes import Transporte, Aereo, Ferroviario, Automotor, Fluvial
from datetime import timedelta
import matplotlib.pyplot as plt
import networkx as nx

def KPI(origen, destino, carga): #Calcula ambas soluciones optimas (costo y tiempo), imprime el medio de transporte, el camino, el costo y el tiempo que tarda. 
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
             
    # Inicializamos variables para guardar los mejores resultados encontrados hasta el momento.
    # Vamos a buscar el camino con el menor costo total (trayecto + carga)
    costo_minimo = float("inf")
    camino_minimo = []
    tipo_minimo = ""
    tiempo_minimo=float("inf")
    costo_carga_minima=float("inf")

    for tipo, conexiones in valores_costo.items():
        grafo_costo = construir_grafo(valores_costo[tipo])
        costo, camino= dijkstra(grafo_costo, origen, destino)
        transporte = obtener_transporte(tipo)
        costo_carga=costo_carga_total(camino,carga,tipo,transporte)
        costo_total = costo + costo_carga
        tiempo=calcular_tiempo_total(camino,tipo, valores_tiempo)
        if costo_total < costo_minimo:
            costo_minimo = costo_total
            camino_minimo = camino
            tipo_minimo = tipo
            tiempo_minimo=tiempo
            costo_carga_minima=costo_carga
    if camino_minimo == []:
        print(f"No hay manera de llegar de {origen} a {destino}")
    else:
        distancia_acumulada, tiempo_acumulado,costo_acumulado = obtener_datos_acumulados(camino_minimo,tipo_minimo,valores_costo,valores_tiempo,costo_carga_minima)
        titulo = "Graficos del KPI costo mínimo"
        graficar(titulo,tiempo_acumulado,distancia_acumulada,costo_acumulado,valores_costo,camino_minimo,tipo_minimo,costo_minimo,tiempo_minimo)
        camino_str = "-".join(camino_minimo)
        print(f"\nCosto mínimo:")
        print(f"Medio de transporte: {tipo_minimo}\nItinerario: {camino_str}\nCosto total: ${costo_minimo}\nTiempo esperado: {tiempo_minimo}")
        # Inicializamos variables para guardar el mejor resultado posible según tiempo:
        # tiempo mínimo, camino correspondiente, tipo de transporte y costos asociados
        tiempo_minimo = float("inf")
        camino_minimo = []
        tipo_minimo = ""
        costo_minimo=float("inf")
        costo_carga_minima=float("inf")
        for tipo, conexiones in valores_tiempo.items():
            transporte = obtener_transporte(tipo)
            grafo_tiempo = construir_grafo(valores_tiempo[tipo])
            tiempo, camino = dijkstra(grafo_tiempo, origen, destino)
            costo=calcular_costo_total(camino,tipo,valores_costo)
            costo_carga=costo_carga_total(camino,carga,tipo,transporte)
            costo_total = costo + costo_carga
            if tiempo < tiempo_minimo and camino!=[]:
                tiempo_minimo = tiempo
                camino_minimo = camino
                tipo_minimo = tipo
                costo_minimo=costo_total
                costo_carga_minima=costo_carga
        
        total_segundos = int(tiempo_minimo * 3600)
        duracion = timedelta(seconds=total_segundos)
        distancia_acumulada, tiempo_acumulado,costo_acumulado = obtener_datos_acumulados(camino_minimo,tipo_minimo,valores_costo,valores_tiempo,costo_carga_minima)
        titulo = "Graficos del KPI tiempo mínimo"
        graficar(titulo, tiempo_acumulado,distancia_acumulada,costo_acumulado,valores_tiempo,camino_minimo,tipo_minimo,costo_minimo,duracion)
        camino_str = "-".join(camino_minimo)
        print(f"\nTiempo mínimo:")
        print(f"Medio de transporte: {tipo_minimo}\nItinerario: {camino_str}\nTiempo total: {duracion}\nCosto total: ${costo_minimo}")

def construir_grafo(transporte): # Construye el grafo para realizar Dijkstra
    grafo = {}
    for trayecto in transporte:
        origen, destino = trayecto.split("-")
        costo = transporte[trayecto]
        grafo.setdefault(origen, []).append((destino, costo))
        grafo.setdefault(destino, []).append((origen, costo))
    return grafo

def dijkstra(grafo, inicio, fin): # Algoritmo que obtiene el camino minimo desde un nodo hasta todo el resto de los nodos del grafo
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

def obtener_transporte(tipo): #se asocia cada tipo de transporte con un objeto de una clase
    if tipo == "Automotor":
        return Automotor()
    elif tipo == "Ferroviaria":
        return Ferroviario()
    elif tipo == "Fluvial":
        return Fluvial()
    elif tipo == "Aerea":
        return Aereo()

def calcular_tiempo_total(camino, tipo, valores_tiempo): #calcula tiempo total para cada tipo de transporte, extrayendo los datos del diccionario valores_tiempo
    tiempo_total = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]
        key = f"{origen}-{destino}"
        key_inv = f"{destino}-{origen}"
        tiempo = valores_tiempo[tipo].get(key) or valores_tiempo[tipo].get(key_inv)
        if tiempo:
            tiempo_total += tiempo
    return timedelta(seconds=int(tiempo_total * 3600)) #para devolver el tiempo total en hh:mm:ss

def calcular_costo_total(camino, tipo, valores_costo): # Calcula el costo total
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
                if ((conexion.origen.nombre == origen_conexion and conexion.destino.nombre == destino_conexion) or
                    (conexion.origen.nombre == destino_conexion and conexion.destino.nombre == origen_conexion)) and conexion.tipo == tipo:
                    if conexion.restriccion:
                        capacidad_efectiva = min(capacidad_efectiva, int(conexion.valor_restriccion))
        costo_carga_total = transporte.calcular_costo_total_carga(carga, capacidad_efectiva)
    else:
        costo_carga_total = transporte.calcular_costo_total_carga(carga)
    return costo_carga_total

def obtener_datos_acumulados(camino, tipo, valores_costo, valores_tiempo,costo_carga_minima): 
    #Define 3 listas con los valores acumulados, la de costos la arranca desde el costo de la carga (fijo)
    distancias_acumuladas = [0]
    tiempos_acumulados = [0]
    costos_acumulados = [costo_carga_minima]

    distancia_total = 0
    tiempo_total = 0
    costo_total = costo_carga_minima

    #Recorre el camino, y va separando de a pares (origen y destino)
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]
        key = f"{origen}-{destino}"
        key_inv = f"{destino}-{origen}" 
    
        for conexion in Conexion.conexiones:
            #Si el origen y el destino coincide con los de alguna conexion. Guarda esa distancia
            if (conexion.origen.nombre == origen and conexion.destino.nombre == destino) or (conexion.origen.nombre == destino and conexion.destino.nombre == origen) and conexion.tipo == tipo:
                distancia=conexion.distancia_km

        #Con el tipo y el key "origen-destino" busca el valor del tiempo y del costo
        tiempo = valores_tiempo[tipo].get(key) or valores_tiempo[tipo].get(key_inv)
        costo = valores_costo[tipo].get(key) or valores_costo[tipo].get(key_inv)

        #Suma los valores encontrados a los valores acumulados
        distancia_total += distancia
        tiempo_total += tiempo
        costo_total += costo

        #Los agrega a la lista 
        distancias_acumuladas.append(distancia_total)
        tiempos_acumulados.append(tiempo_total)
        costos_acumulados.append(costo_total)
    return distancias_acumuladas, tiempos_acumulados, costos_acumulados 

def graficar(titulo,tiempo_acumulado,distancia_acumulada,costo_acumulado, grafo_lista, camino_minimo, tipo_minimo,costo_minimo,tiempo_minimo):
    fig, axs = plt.subplots(1, 3, figsize=(12, 5))

    fig.suptitle(f'{titulo}: {tipo_minimo}',fontsize=20, fontweight = 'bold',color="black")

    texto_info = f"Origen: {camino_minimo[0]}\nDestino: {camino_minimo[-1]}\nCosto total: {costo_minimo}\nTiempo total: {tiempo_minimo}"
    fig.text(0.01, 0.92, texto_info,fontsize=10, fontweight='bold',bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='square,pad=0.3'),color='black')

    # Grafico tiempo vs distancia
    axs[0].plot(distancia_acumulada, tiempo_acumulado,marker='o',color='teal')
    axs[0].set_title('Distancia vs Tiempo acumulado',fontweight='bold')
    axs[0].set_xlabel('Distancia acumulada (km)')
    axs[0].set_ylabel('Tiempo acumulado (horas)')
    axs[0].grid(True)
    
    # Grafico costo vs distancia
    axs[1].plot(distancia_acumulada, costo_acumulado, marker='o', color='teal')
    axs[1].set_title('Costo vs Distancia acumulada',fontweight='bold')
    axs[1].set_xlabel('Distancia acumulada (km)')
    axs[1].set_ylabel('Costo acumulado ($)')
    axs[1].grid(True)


    # Grafo visual para representar la ruta óptima con networkx
    grafo = nx.Graph()  # Se crea un grafo vacio no dirigido
    agregados = set()   # Usamos un set para registrar conexiones ya agregadas y evitar duplicados
    for tipo, conexiones in grafo_lista.items():
        if tipo == tipo_minimo:
            for conexion in conexiones:
                origen, destino = conexion.split("-")
                key = f'{origen}-{destino}'            # Clave para registrar la conexion directa
                key_inv = f'{destino}-{origen}'        # Clave inversa para evitar duplicados (ida y vuelta)
                if key not in agregados and key_inv not in agregados:
                    peso = grafo_lista[tipo][conexion]
                    grafo.add_edge(origen, destino, weight=peso)
                    agregados.add(key)
                    agregados.add(key_inv)

    # Calculamos la posicion de cada nodo para el layout del gráfico
    ordenamiento = nx.spring_layout(grafo,weight='weight',seed = 42)
    nodos_resaltados = camino_minimo
    caminos_resaltados = []
    caminos_resaltados = []
    for i in range(len(camino_minimo) - 1):
        origen = camino_minimo[i]
        destino = camino_minimo[i + 1]
        caminos_resaltados.append((origen, destino))
        caminos_resaltados.append((destino, origen))

    ax = axs[2]
    ax.set_title("Ruta óptima (Se muestran costos por tramo)",fontweight='bold')
    node_colors = ['teal' if nodo in nodos_resaltados else 'gray' for nodo in grafo.nodes()]
    edge_colors = ['teal' if (origen, destino) in caminos_resaltados else 'gray' for (origen, destino) in grafo.edges()] # aca tiene que usar (origen,destino) porque el grafo te devuelve las aristas en forma de tuplas

    nx.draw_networkx_nodes(grafo, ordenamiento, ax=ax, node_color=node_colors, node_size=1000)
    nx.draw_networkx_edges(grafo, ordenamiento, ax=ax, edge_color=edge_colors, width=2)
    nx.draw_networkx_labels(grafo, ordenamiento, ax=ax, font_size=9)

    conexiones = nx.get_edge_attributes(grafo, 'weight')
    if 'tiempo' in titulo.lower(): # Se fija si el titulo tiene tiempo en el nombre para saber cuando convertir los datos
        # Convertimos los valores en horas a formato hh:mm:ss
        conexiones_etiquetas = {c: str(timedelta(hours=tiempo)) for c, tiempo in conexiones.items()}
    else: # Si no tiene tiempo en el titulo entonces lo dejo como está al ser un costo, este costo esta dado unicamente por tramo, no incluye el costo por carga
        conexiones_etiquetas = {c: f"{costo}" for c, costo in conexiones.items()}
    nx.draw_networkx_edge_labels(grafo, ordenamiento, edge_labels=conexiones_etiquetas, ax=ax, font_color='black')

    ax.axis('off')

    # ajusta espaciado
    plt.tight_layout()
    plt.show()

def KPI_solicitudes(diccionario_solicitudes):
    for key in diccionario_solicitudes.keys(): # obtiene el id del pedido
        print(f'Posbles rutas para el pedido {key}')
        carga = diccionario_solicitudes[key]["peso_kg"]
        origen = diccionario_solicitudes[key]["origen"]
        destino = diccionario_solicitudes[key]["destino"]
        KPI(origen, destino, carga) # luego de extraer una solicitud del archivo csv, calcula su kpi de costo y tiempo