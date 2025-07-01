from datetime import timedelta
from B_nodo import Nodo
from C_conexion import Conexion
from E_datos_transportes import Transporte, Aereo, Ferroviario, Automotor, Fluvial
import matplotlib.pyplot as plt
import networkx as nx

class PlanificadorRutas:
    def __init__(self):
        """Inicializa los objetos de transporte y estructuras de datos para costos y tiempos."""
        self.transportes = {
            "Automotor": Automotor(),
            "Ferroviaria": Ferroviario(),
            "Fluvial": Fluvial(),
            "Aerea": Aereo()
        }
        self.valores_costo = {}
        self.valores_tiempo = {}

    def planificar_solicitudes(self, solicitudes):
        """Procesa múltiples solicitudes de planificación de rutas.

        Args:
            solicitudes (dict): Diccionario con datos de origen, destino y peso por pedido.
        """
        for pedido_id, datos in solicitudes.items():
            print(f"\nPedido {pedido_id}")
            self.planificar_ruta(datos["origen"], datos["destino"], datos["peso_kg"])


    def planificar_ruta(self, origen, destino, carga):
        """Planifica una ruta óptima por costo y tiempo entre dos puntos para una carga dada.

        Args:
            origen (str): Nodo origen.
            destino (str): Nodo destino.
            carga (float): Peso de la carga en kg.
        """
        self._generar_matrices(carga)
        print(f"\n Planificando ruta de {origen} a {destino} para una carga de {carga}kg\n")
        self._evaluar("costo", origen, destino, carga)
        self._evaluar("tiempo", origen, destino, carga)
        self._evaluar_poblacion_maxima(origen,destino,carga)

    def _generar_matrices(self, carga):
        """Calcula matrices de costos y tiempos para cada transporte, según la carga dada."""
        self.valores_costo = {k: {} for k in self.transportes}
        self.valores_tiempo = {k: {} for k in self.transportes}
        for nodo in Nodo.nodos:
            for tipo, conexiones in nodo.grafos.items():
                transporte = self.transportes.get(tipo)
                if transporte:
                    for conexion in conexiones:
                        key = f"{conexion.origen}-{conexion.destino}"
                        self.valores_costo[tipo][key] = transporte.calcular_costo_trayecto(conexion, carga)
                        self.valores_tiempo[tipo][key] = transporte.calcular_tiempo(conexion)

    def _evaluar(self, criterio, origen, destino, carga):
        """Evalúa y selecciona la mejor ruta según el criterio de costo o tiempo.

        Args:
            criterio (str): "costo" o "tiempo".
            origen (str): Nodo origen.
            destino (str): Nodo destino.
            carga (float): Peso de la carga.
        """
        matriz = self.valores_costo if criterio == "costo" else self.valores_tiempo
        mejor_valor = float("inf")
        mejor_camino = []
        mejor_tipo = ""
        mejor_costo_carga = 0
        mejor_tiempo = None

        for tipo in self.transportes:
            grafo = self._construir_grafo(matriz[tipo])
            valor, camino = self._dijkstra(grafo, origen, destino)
            if not camino:
                continue

            transporte = self.transportes[tipo]
            costo_carga = self._costo_carga_total(camino, carga, tipo, transporte)
            costo_total = self._calcular_costo_total(camino, tipo, self.valores_costo)
            tiempo_total = self._calcular_tiempo_total(camino, tipo, self.valores_tiempo)
            total = costo_total + costo_carga if criterio == "costo" else tiempo_total.total_seconds()

            if total < mejor_valor:
                mejor_valor = total
                mejor_camino = camino
                mejor_tipo = tipo
                mejor_costo_carga = costo_carga
                mejor_tiempo = tiempo_total

        if mejor_camino:
            distancias, tiempos, costos = self._obtener_datos_acumulados(mejor_camino, mejor_tipo, self.valores_costo, self.valores_tiempo, mejor_costo_carga)
            self._graficar(f"KPI {criterio} mínimo", tiempos, distancias, costos, matriz, mejor_camino, mejor_tipo, mejor_valor if criterio == 'costo' else costo_total + mejor_costo_carga, mejor_tiempo)

            print(f"{criterio.capitalize()} mínimo:")
            print(f"  - Medio de transporte: {mejor_tipo}")
            print(f"  - Itinerario: {' -> '.join(mejor_camino)}")
            print(f"  - Costo total: ${costo_total + mejor_costo_carga:.2f}")
            print(f"  - Tiempo total: {mejor_tiempo}\n")
        else:
            print(f" No se encontró ruta óptima por {criterio}.")

    def _construir_grafo(self, transporte):
        """Construye un grafo no dirigido a partir de los datos de transporte.

        Args:
            transporte (dict): Diccionario de trayectos con pesos.
        Returns:
            dict: Representación del grafo como lista de adyacencia.
        """
        grafo = {}
        for trayecto, costo in transporte.items():
            origen, destino = trayecto.split("-")
            grafo.setdefault(origen, []).append((destino, costo))
            grafo.setdefault(destino, []).append((origen, costo))
        return grafo

    def _dijkstra(self, grafo, inicio, fin):
        """Algoritmo de Dijkstra para encontrar el camino mínimo.

        Args:
            grafo (dict): Grafo de adyacencias.
            inicio (str): Nodo de inicio.
            fin (str): Nodo de destino.
        Returns:
            tuple: (costo mínimo, lista con el camino)
        """
        nodos = list(grafo.keys())
        costos = {nodo: float('inf') for nodo in grafo}
        anteriores = {}
        visitados = []
        costos[inicio] = 0

        while nodos:
            actual = min((n for n in nodos if n not in visitados), key=lambda n: costos[n], default=None)
            if actual is None:
                return 
            visitados.append(actual)
            nodos.remove(actual)
            for vecino, costo in grafo.get(actual, []):
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
        return costos.get(fin, float('inf')), camino

    def _calcular_tiempo_total(self, camino, tipo, tiempos):
        """Calcula el tiempo total en horas para una ruta.

        Args:
            camino (list): Lista de nodos en la ruta.
            tipo (str): Tipo de transporte.
            tiempos (dict): Diccionario de tiempos por trayecto.
        Returns:
            timedelta: Tiempo total del trayecto.
        """
        total = 0
        for i in range(len(camino) - 1):
            key = f"{camino[i]}-{camino[i + 1]}"
            key_inv = f"{camino[i + 1]}-{camino[i]}"
            tiempo = tiempos[tipo].get(key) or tiempos[tipo].get(key_inv)
            if tiempo:
                total += tiempo
        return timedelta(seconds=int(total * 3600))

    def _calcular_costo_total(self, camino, tipo, costos):
        """Suma el costo de los tramos que componen un camino.

        Args:
            camino (list): Nodos del camino.
            tipo (str): Tipo de transporte.
            costos (dict): Diccionario de costos.
        Returns:
            float: Costo total.
        """
        total = 0
        for i in range(len(camino) - 1):
            key = f"{camino[i]}-{camino[i + 1]}"
            key_inv = f"{camino[i + 1]}-{camino[i]}"
            costo = costos[tipo].get(key) or costos[tipo].get(key_inv)
            if costo:
                total += costo
        return total

    def _costo_carga_total(self, camino, carga, tipo, transporte):
        """Calcula el costo de la carga a transportar, considerando restricciones.

        Args:
            camino (list): Ruta.
            carga (float): Peso de la carga.
            tipo (str): Tipo de transporte.
            transporte (Transporte): Objeto de transporte correspondiente.
        Returns:
            float: Costo total por carga.
        """
        if tipo == "Automotor":
            capacidad = transporte.capacidad
            for i in range(len(camino) - 1):
                for conexion in Conexion.conexiones:
                    if ((conexion.origen.nombre == camino[i] and conexion.destino.nombre == camino[i + 1]) or
                        (conexion.destino.nombre == camino[i] and conexion.origen.nombre == camino[i + 1])) and conexion.tipo == tipo:
                        if conexion.restriccion:
                            capacidad = min(capacidad, int(conexion.valor_restriccion))
            return transporte.calcular_costo_total_carga(carga, capacidad)
        return transporte.calcular_costo_total_carga(carga)

    def _obtener_datos_acumulados(self, camino, tipo, costos, tiempos, costo_fijo):
        """Calcula acumulados de distancia, tiempo y costo para cada tramo de un camino.

        Returns:
            tuple: (distancias_acumuladas, tiempos_acumulados, costos_acumulados)
        """
        dist, time, cost = [0], [0], [costo_fijo]
        d_acum, t_acum, c_acum = 0, 0, costo_fijo

        for i in range(len(camino) - 1):
            origen, destino = camino[i], camino[i + 1]
            key = f"{origen}-{destino}"
            key_inv = f"{destino}-{origen}"
            distancia = next((c.distancia_km for c in Conexion.conexiones if (c.origen.nombre, c.destino.nombre) == (origen, destino) or (c.destino.nombre, c.origen.nombre) == (origen, destino)), 0)
            t = tiempos[tipo].get(key) or tiempos[tipo].get(key_inv) or 0
            c = costos[tipo].get(key) or costos[tipo].get(key_inv) or 0
            d_acum += distancia
            t_acum += t
            c_acum += c
            dist.append(d_acum)
            time.append(t_acum)
            cost.append(c_acum)

        return dist, time, cost

    def _graficar(self, titulo, tiempo_acum, distancia_acum, costo_acum, grafo_lista, camino_minimo, tipo_minimo, costo_minimo, tiempo_minimo):
        """Genera graficos de los KPIs: distancia-tiempo, distancia-costo, y ruta optima."""

        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f'{titulo}: {tipo_minimo}', fontsize=20, fontweight='bold')
        texto_info = f"Origen: {camino_minimo[0]}\nDestino: {camino_minimo[-1]}\nCosto total: {costo_minimo}\nTiempo total: {tiempo_minimo}"

        fig.text(0.02, 0.92, texto_info, fontsize=10, fontweight='bold',
        bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='square,pad=0.3'))

        # Gráfico: Tiempo acumulado vs Distancia
        axs[0].plot(distancia_acum, tiempo_acum, marker='o', color='teal')
        axs[0].set_title('Distancia vs Tiempo acumulado')
        axs[0].set_xlabel('Distancia (km)')
        axs[0].set_ylabel('Tiempo (h)')

        # Gráfico: Costo acumulado vs Distancia
        axs[1].plot(distancia_acum, costo_acum, marker='o', color='teal')
        if 'población' in titulo.lower():
            axs[1].set_title('Distancia vs Poblacion')
            axs[1].set_xlabel('Distancia (km)')
            axs[1].set_ylabel('Poblacion (Millones de person)')
        else:
            axs[1].set_title('Distancia vs Costo acumulado')
            axs[1].set_xlabel('Distancia (km)')
            axs[1].set_ylabel('Costo ($)')

        # Grafo de la ruta optima
        grafo = nx.Graph()
        agregados = set()
        for conexion in grafo_lista[tipo_minimo]:
            origen, destino = conexion.split("-")
            if (origen, destino) not in agregados and (destino, origen) not in agregados:
                grafo.add_edge(origen, destino, weight=grafo_lista[tipo_minimo][conexion])
                agregados.update([(origen, destino), (destino, origen)])

        layout = nx.spring_layout(grafo, weight='weight', seed=42)
        nodos = camino_minimo
        edges = [(nodos[i], nodos[i+1]) for i in range(len(nodos)-1)] + [(nodos[i+1], nodos[i]) for i in range(len(nodos)-1)]
        ax = axs[2]
        ax.set_title("Ruta optima")
        nx.draw_networkx_nodes(grafo, layout, ax=ax, node_color=['teal' if n in nodos else 'gray' for n in grafo.nodes()], node_size=800)
        nx.draw_networkx_edges(grafo, layout, ax=ax, edge_color=['teal' if e in edges else 'gray' for e in grafo.edges()], width=2)
        nx.draw_networkx_labels(grafo, layout, ax=ax, font_size=9)

        labels = nx.get_edge_attributes(grafo, 'weight')
        if 'tiempo' in titulo.lower() or 'población' in titulo.lower():
            etiquetas = {e: str(timedelta(hours=v)) for e, v in labels.items()}
        else:
            etiquetas = {e: f"{v}" for e, v in labels.items()}
        nx.draw_networkx_edge_labels(grafo, layout, edge_labels=etiquetas, ax=ax)
        ax.axis('off')

        plt.tight_layout()
        mng = plt.get_current_fig_manager()
        try:
            mng.window.state('zoomed')  # Windows
        except:
            try:
                mng.window.showMaximized()  # Linux
            except:
                pass
        plt.show()
        
    def _evaluar_poblacion_maxima(self, origen, destino, carga):
        """Busca rutas posibles y selecciona la que pase por mayor población intermedia."""
        mejor_ruta = []
        mejor_poblacion = -1
        mejor_tipo = ""
        mejor_tiempo = None
        mejor_costo_carga = 0
        for tipo in self.transportes:
            grafo = self._construir_grafo(self.valores_tiempo[tipo])
            rutas = self._encontrar_rutas_con_dfs(grafo, origen, destino, max_depth=6)
            for ruta in rutas:
                poblacion = sum(Nodo.dict_nodos[n].poblacion for n in ruta)
                if poblacion > mejor_poblacion:
                    mejor_poblacion = poblacion
                    mejor_ruta = ruta
                    mejor_tipo = tipo
        if mejor_ruta:
            poblacion=[]
            suma=0
            for ciudad in mejor_ruta:
                ciudad=Nodo.dict_nodos[ciudad]
                suma+= ciudad.poblacion
                poblacion.append(suma)

            transporte = self.transportes[mejor_tipo]
            mejor_costo_carga = self._costo_carga_total(mejor_ruta, carga, mejor_tipo, transporte)
            costo_total = self._calcular_costo_total(mejor_ruta, tipo, self.valores_costo)
            costo_total+=mejor_costo_carga
            mejor_tiempo = self._calcular_tiempo_total(mejor_ruta, mejor_tipo, self.valores_tiempo)
            distancias, tiempos, costos = self._obtener_datos_acumulados(mejor_ruta, mejor_tipo, self.valores_costo, self.valores_tiempo, mejor_costo_carga)
            self._graficar("KPI por población máxima", tiempos, distancias, poblacion, self.valores_tiempo, mejor_ruta, mejor_tipo, costo_total, mejor_tiempo)
            print(f" Ruta con mayor población intermedia:")
            print(f"  - Medio de transporte: {mejor_tipo}")
            print(f"  - Itinerario: {' -> '.join(mejor_ruta)}")
            print(f"  - Población total: {mejor_poblacion}")
            print(f'  - Costo total: {costo_total}')
            print(f"  - Tiempo total: {mejor_tiempo}\n")
        else:
            print(" No se encontró ruta con población intermedia significativa.")

    def _encontrar_rutas_con_dfs(self, grafo, inicio, fin, max_depth=5):
        """Encuentra rutas usando DFS con profundidad limitada."""
        rutas = []

        def dfs(visitados, actual):
            if len(visitados) > max_depth:
                return
            if actual == fin:
                rutas.append(visitados[:])
                return
            for vecino, _ in grafo.get(actual, []):
                if vecino not in visitados:
                    visitados.append(vecino)
                    dfs(visitados, vecino)
                    visitados.pop()

        dfs([inicio], inicio)
        return rutas
        
    def estadistica_eficiencia(self):
        carga = 30000
        resultados = []

        for conexion in Conexion.conexiones:
            tipo = conexion.getTipo()
            transporte = self.transportes[tipo]
            costo = self._costo_carga_total([conexion.origen, conexion.destino],carga,tipo,transporte) + transporte.calcular_costo_trayecto(conexion,carga)
            tiempo = transporte.calcular_tiempo(conexion)
            distancia = conexion.distancia_km
            if costo<100000:
                eficiencia_costo=1
            else:
                eficiencia_costo=costo/100000
            eficiencia = 0.55 / eficiencia_costo + 0.25 / tiempo + 0.2 / distancia
            resultados.append({"tipo": tipo,"costo": costo,"tiempo": tiempo,"distancia": distancia,"eficiencia": eficiencia})

        tipos = ["Aerea", "Ferroviaria", "Automotor", "Fluvial"]

        def obtener_valores_por_tipo(metric):
            return [[r[metric] for r in resultados if r["tipo"] == t] for t in tipos]
        
        # Colores distintos por boxplot
        colores = ['lightblue', 'lightgreen', 'lightcoral']
        metricas = ["costo", "tiempo", "distancia"]
        titulos = ["Costo Total", "Tiempo (horas)", "Distancia (km)"]
        plt.figure(figsize=(15, 5))
        plt.suptitle("Distribución de Métricas por Tipo de Transporte", fontsize=16, fontweight='bold')
        for i, (metric, titulo) in enumerate(zip(metricas, titulos)):
            valores = obtener_valores_por_tipo(metric)
            ax = plt.subplot(1, 3, i + 1)
            box = ax.boxplot(valores, patch_artist=True, labels=tipos)   
            # Aplicar color a cada box
            for patch in box['boxes']:
                patch.set_facecolor(colores[i])
            ax.set_title(titulo)
            ax.set_xlabel("Tipo de Transporte")
            ax.set_ylabel(metric.capitalize())
            ax.grid(True)
        plt.tight_layout()
        mng = plt.get_current_fig_manager()
        try:
            mng.window.state('zoomed')  # Windows
        except:
            try:
                mng.window.showMaximized()  # Linux
            except:
                pass
        plt.show()
        
        # Eficiencia promedio por tipo de transporte
        eficiencia_promedio = []
        for tipo in tipos:
            eficiencias = [r["eficiencia"] for r in resultados if r["tipo"] == tipo]
            promedio = sum(eficiencias) / len(eficiencias) if eficiencias else 0
            eficiencia_promedio.append(promedio)
            
        plt.figure(figsize=(8, 5))
        plt.bar(tipos, eficiencia_promedio, color='skyblue')
        plt.title("Eficiencia Promedio por Tipo de Transporte")
        plt.ylabel("Índice de Eficiencia")
        plt.xlabel("Tipo de Transporte")
        plt.grid(True)
        plt.tight_layout()
        mng = plt.get_current_fig_manager()
        try:
            mng.window.state('zoomed')  # Windows
        except:
            try:
                mng.window.showMaximized()  # Linux
            except:
                pass
        plt.show()
