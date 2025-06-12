from D_leer_csv import *
from F_grafos import *
from Z_validaciones import *

crear_nodos("nodos.csv")
print("")
crear_conexiones("conexiones.csv")
decision = input("Si desea cargar una solicitud manualmente presione 'm', en caso contrario se realizara con el archivo 'solicitudes.csv': ")
if decision != "m":
    solicitudes = leer_solicitudes("solicitudes.csv") # lee las solicitudes ingresadas desde el archivo csv
    KPI_solicitudes(solicitudes)
else:
    carga = validar_carga()
    origen = validar_origen()
    destino = validar_destino()
    KPI(origen,destino,carga)

# Falta hacer los graficos