from D_leer_csv import *
from F_grafos import *

crear_nodos("nodos.csv")
#print("Impresion de nodos para comprobar que se cargaron bien:")
#Nodo.imprimirNodos() # Prueba]
#print("")
#print("Impresion de conexiones para comprobar que se cargaron bien:")
crear_conexiones("conexiones.csv")
#Conexion.imprimirConexiones() # Prueba
#print("")
#print("Impresion de los nodos de vuelta para ver si se hizo bien la conexion (No se si esta bien hecha la conexion del objeto pero de las redes funciona):")
#Nodo.imprimirNodos()
KPIcosto("Junin","Buenos_Aires",50000)

# FALTA EL ARREGLAR EL COSTO FIJO