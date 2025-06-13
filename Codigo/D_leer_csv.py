# Este archivo se encarga de leer los diferentes csv y ya crear los nodos y conexiones directamente cuando se usan sus funciones 
import csv
from B_nodo import Nodo
from C_conexion import Conexion
from Z_validaciones import *

def crear_nodos(archivo_nodos: str): # Esta funcion va leyendo y creando los nodos que esten presentes en el archivo de nodos. La validacion se hace dentro de la funcion nodo
    if isinstance(archivo_nodos,str):
        with open(archivo_nodos, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            archivo.readline()
            for fila in lector:
                if fila == []:
                    continue
                else:
                    nodo = Nodo(fila[0])   

    else:
        return TypeError (f'Error de tipo: se esperaba un objeto de tipo string y se proporciono un objeto de tipo {type(archivo_nodos)} para la variable archivo_nodos')

def crear_conexiones(archivo_conexiones: str): # Esta funcion va leyendo y creando las conexiones que esten presentes en el archivo de conexiones.
    diccionario_de_nodos = Nodo.dict_nodos
    with open(archivo_conexiones, newline='', encoding='utf-8') as archivo: # abre el archivo y se asegura de que no ocurra un error al dejarlo abierto
        lector = csv.reader(archivo)
        archivo.readline() # se saltea la primera fila de enunciados
        for fila in lector:
            if fila == []:
                continue
            else:
                origen = fila[0]
                if not origen:
                     raise ValueError (f'Error en el origen de una de las conexiones, el valor no puede ser None')
                destino = fila[1]
                if not destino:
                     raise ValueError (f'Error en el destino de una de las conexiones, el valor no puede ser None')
                tipo = fila[2]
                if not tipo:
                     raise ValueError (f'Error en el tipo de una de las conexiones, el valor no puede ser None')
                distancia_km = fila[3]
                if not distancia_km and not float_o_int(distancia_km): 
                     raise ValueError (f'No se cargo una distancia o distancia_km no es de tipo float. Su tipo es {type(distancia_km)}')
                restriccion = fila[4]
                valor_restriccion = fila[5]
                if not validar_restriccion(tipo,valor_restriccion):
                    raise ValueError (f'No se cargo un valor de restriccion valido. Un valor de restriccion valido tiene que ser de clase Float o  Int. Se cargo un tipo {type(valor_restriccion)}') # falta la validacion aca
                
                # al conseguir todos los datos necesarios para la conexion la crea, lo que la guarda como instancia para tomar luego
                conexion = Conexion(diccionario_de_nodos[origen],diccionario_de_nodos[destino], tipo, float(distancia_km), restriccion, valor_restriccion)

def leer_solicitudes(archivo_solicitudes:str):
    solicitudes = {}
    with open(archivo_solicitudes, newline='', encoding='utf-8') as archivo: # abre el archivo y se asegura de que no ocurra un error al dejarlo abierto
        lector = csv.reader(archivo)
        archivo.readline() # se saltea la primera fila de enunciados
        for fila in lector: # Se va guardando por fila las solicitudes y se ingresan dentro de un diccionario para despues usar los datos en la funcion KPI
            if fila == []:
                continue
            else:
                id_carga = fila[0] 
                if not id_carga:
                    raise ValueError (f'Error en el id de carga, debe tener un id de carga asociado')
                peso_kg = int(fila[1])
                if not peso_kg:
                        raise ValueError (f'Error en el peso_kg')
                origen = fila[2]
                if not origen:
                        raise ValueError (f'Error en el origen')
                destino = fila[3]
                if not destino:
                        raise ValueError (f'Error en el destino')
                solicitudes[id_carga] = {"peso_kg":peso_kg,"origen":origen,"destino":destino}
        return solicitudes
