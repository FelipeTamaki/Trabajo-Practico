from math import ceil
from C_conexion import Conexion
from B_nodo import Nodo

class Transporte():
    def __init__(self, modo, costo_fijo, velocidad, capacidad, costo_km, costo_kg):
        self.modo = modo
        self.costo_fijo = costo_fijo
        self.capacidad = capacidad
        self.velocidad = velocidad
        self.costo_km = costo_km
        self.costo_kg = costo_kg


    def calcular_costo_total_carga(self,carga):
        return self.costo_kg*carga
        
class Aereo(Transporte):
    def __init__(self):
        super().__init__("Aerea", 750, [600, 400], 5000, 40, 10)

    def calcular_costo_trayecto(self, conexion, carga):
        cantidad = ceil(carga / self.capacidad)
        costo = cantidad * (self.costo_km * conexion.distancia_km+self.costo_fijo) 
        return costo

    def calcular_tiempo(self,conexion): # Calcula el tiempo del Aereo
        if conexion.restriccion:
            tiempo=conexion.distancia_km*(float(conexion.valor_restriccion)*400+(1-float(conexion.valor_restriccion))*600)
        else:
            tiempo=conexion.distancia_km*600 
        return tiempo

class Ferroviario(Transporte):
    def __init__(self):
        super().__init__("Ferroviario", 100, 100, 150000, None, 3)

    def calcular_costo_trayecto(self, conexion, carga):
        if conexion.distancia_km < 200:
            costo_km = 20 
        else:
            costo_km=15
        cantidad = ceil(carga / self.capacidad)
        costo = (costo_km * conexion.distancia_km+self.costo_fijo)*cantidad 
        return costo

    def calcular_tiempo(self, conexion):
        if conexion.restriccion:
            divisor = int(conexion.valor_restriccion)
            tiempo = conexion.distancia_km / divisor
        else:
            tiempo = conexion.distancia_km / self.velocidad
        return tiempo

class Automotor(Transporte):
    def __init__(self):
        super().__init__("Automotor", 30, 80, 30000, 5, None)

    def calcular_costo_trayecto(self, conexion, carga):
        cantidad = ceil(carga / self.capacidad)
        costo_tramo = (self.costo_fijo + self.costo_km * conexion.distancia_km) * cantidad
        return costo_tramo

    def calcular_costo_carga(self, carga, conexion):
        capacidad_efectiva = int(conexion.valor_restriccion) if conexion.restriccion else self.capacidad
        return self.calcular_costo_total_carga(carga, capacidad_efectiva)

    def calcular_costo_total_carga(self, carga, capacidad_efectiva):
        if capacidad_efectiva >= 15000:
            costo_kg = 2
        else:
            costo_kg = 1

        cantidad = carga // capacidad_efectiva
        costo_carga = cantidad * costo_kg * capacidad_efectiva

        sobrante = carga - cantidad * capacidad_efectiva
        if sobrante:
            costo_kg = 2 if sobrante >= 15000 else 1
            costo_carga += costo_kg * sobrante

        return costo_carga

    def calcular_tiempo(self, conexion):
        return conexion.distancia_km / self.velocidad


class Fluvial(Transporte):
    def __init__(self):
        super().__init__("Fluvial", None, 40, 100000, 15, 2)

    def calcular_costo_trayecto(self, conexion, carga):
        if conexion.valor_restriccion == "maritimo":
            costo_fijo = 1500 
        elif conexion.valor_restriccion == "fluvial":
            costo_fijo = 500
        cantidad = ceil(carga / self.capacidad)
        costo = cantidad * (self.costo_km * conexion.distancia_km + costo_fijo) 
        return costo

    def calcular_tiempo(self, conexion):
        return conexion.distancia_km / self.velocidad