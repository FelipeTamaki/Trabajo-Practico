from B_nodo import Nodo
from C_conexion import Conexion

def float_o_int(numero):
    try:
        numero = float(numero)
        return True
    except ValueError:
        print(f'Error de valor, se esperaba un float o int pero se introdujo un dato de tipo {type(numero)}')
        return False
    
def solo_float(numero):
    try:
        numero = float(numero)
        return True
    except ValueError:
        print(f'El numero ingresado no puede ser convertido a formato float')
        return False

def solo_nodo(nodo):
    if isinstance(nodo, Nodo):
        return True
    else:
        return False
    
def validar_restriccion(tipo, valor_restriccion):
    if tipo == "Ferroviaria" or tipo == "Automotor":
        if valor_restriccion == "":
            return True
        elif not float_o_int(valor_restriccion):
            raise ValueError('Se esperaba una restricción con valor float o int')
        return True

    elif tipo == "Fluvial":
        if str(valor_restriccion).strip().lower() not in ["fluvial", "maritimo"]:
            raise ValueError('Se esperaba una restricción "fluvial" o "maritimo" (str)')
        return True

    elif tipo == "Aerea":
        if not solo_float(valor_restriccion):
            raise ValueError('Se esperaba una restricción con valor float')
        return True

