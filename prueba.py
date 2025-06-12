import networkx as nx
import matplotlib.pyplot as plt

# Crear grafo no dirigido
G = nx.Graph()

# Agregar nodos con nombres reales
lista = ["Buenos Aires", "La Plata", "Zárate", "Rosario"]
G.add_nodes_from(lista)

# Agregar aristas con pesos
conexiones = [("Buenos Aires", "La Plata", 60),
              ("Buenos Aires", "Zárate", 90), 
              ("La Plata", "Zárate", 130), 
              ("Zárate", "Rosario", 200), 
              ("Rosario", "Buenos Aires", 300)]
for origen, destino, peso in conexiones:
    G.add_edge(origen, destino, weight=peso)

# Posiciones fijas para que el grafo sea estable
pos = nx.spring_layout(G, seed=42)

# --- ✅ Parámetros para resaltar un camino --- Camino que consigue Dijkstra
nodos_resaltados = ["Buenos Aires", "Zárate", "Rosario"]
aristas_resaltadas = [("Buenos Aires", "Zárate"), ("Zárate", "Rosario")]

# Dibujar nodos (resaltados en naranja, el resto en celeste)
node_colors = ['orange' if node in nodos_resaltados else 'lightblue' for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1200)

# Dibujar etiquetas de los nodos
nx.draw_networkx_labels(G, pos, font_size=10)

# Dibujar aristas (resaltadas en rojo, el resto en gris)
aristas_todas = list(G.edges())
edge_colors = ['red' if edge in aristas_resaltadas or (edge[1], edge[0]) in aristas_resaltadas else 'gray' for edge in aristas_todas]
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)

# Dibujar etiquetas de los pesos
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

plt.title("Camino a tomar")
plt.axis('off')
plt.show()


