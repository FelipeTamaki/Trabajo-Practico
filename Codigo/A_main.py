# Este archivo es para probar el codigo y que todo funcione bien, si ponen codigo en otros archivos para probar pongan el if __name__ == "__main__":
from B_nodo import Nodo
from C_conexion import Conexion
from D_leer_csv import *

crear_nodos("nodos.csv")
print("Impresion de nodos para comprobar que se cargaron bien:")
Nodo.imprimirNodos() # Prueba
print("")
print("Impresion de conexiones para comprobar que se cargaron bien:")
crear_conexiones("conexiones.csv")
Conexion.imprimirConexiones() # Prueba
print("")
print("Impresion de los nodos de vuelta para ver si se hizo bien la conexion (No se si esta bien hecha la conexion del objeto pero de las redes funciona):")
Nodo.imprimirNodos()
