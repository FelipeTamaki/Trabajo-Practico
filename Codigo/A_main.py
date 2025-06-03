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
KPIcosto("Zarate","Mar_del_Plata",100000)
print("")
KPIcosto("Buenos_Aires","Azul",100000)