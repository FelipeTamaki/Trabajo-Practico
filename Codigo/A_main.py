# Este archivo es para probar el codigo y que todo funcione bien, si ponen codigo en otros archivos para probar pongan el if __name__ == "__main__":

from B_nodo import Nodo
from C_conexion import Conexion
from D_leer_csv import *

crear_nodos("nodos.csv")
Nodo.imprimir_nodos() # Prueba
crear_conexiones("conexiones.csv")
Conexion.imprimir_conexiones() 