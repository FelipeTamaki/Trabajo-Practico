# En  este archivo habria que hacer que se tenga la informacion sobre la velocidad maxima, los costos, etc y los llamas cuando hagas lo de dijkstra 
from math import ceil
class Transporte():
    def __init__(self, modo, costo_fijo, velocidad, capacidad, costo_km, costo_kg):
        self.modo = modo
        self.costo_fijo = costo_fijo
        self.capacidad = capacidad
        self.velocidad = velocidad
        self.costo_km = costo_km
        self.costo_kg = costo_kg

class Aereo(Transporte):
    def __init__(self):
        super().__init__("Aerea", 750, [600,400], 5000, 40, 10)

    def calcular_costo(self,conexion, carga):
        cantidad= ceil(carga/self.capacidad)
        costo = cantidad *( self.costo_fijo+  self.costo_km*conexion.distancia_km)+ carga*self.costo_kg
        return costo
    
    def calcular_tiempo(self,conexion):
        if conexion.restriccion:
            tiempo=conexion.distancia_km(conexion.valor_restriccion*400+(1-conexion.valor_restriccion)*600)
        else:
            tiempo=conexion.distancia_km*600
        return tiempo

class Ferroviario(Transporte):
    def __init__(self):
        super().__init__("Ferroviario", 100, 100, 150000, None, 3)

    def calcular_costo(self, conexion, carga):
        if conexion.distancia_km>= 200: # Ver si la distancia es mayor a 200
            costo_km = 20
        else:
            costo_km = 15
        cantidad=ceil(carga/self.capacidad)
        costo=cantidad*(costo_km*conexion.distancia_km+self.costo_fijo)+self.costo_kg*carga  
        return costo
    
    def calcular_tiempo(self, conexion, velocidad):
        if conexion.restriccion:
            divisor=int(conexion.valor_restriccion)
            tiempo = conexion.distancia_km/divisor
        else:
            tiempo = conexion.distancia_km/velocidad
        return tiempo
        
class Automotor(Transporte):
    def __init__(self):
        super().__init__("Automotor", 30, 80, 30000, 5, None)
        
    def calcular_costo(self,conexion, carga):
        if conexion.restriccion:
            divisor = conexion.valor_restriccion
        else:
            divisor = self.capacidad
        divisor=int(divisor)
        if divisor >=15000:
            costo_kg = 2
        else:
            costo_kg = 1

        cantidad = carga//divisor
        costo=cantidad*(self.costo_km*conexion.distancia_km+self.costo_fijo+costo_kg*divisor)
        
        sobrante=carga%divisor
        if sobrante:
            if sobrante>=15000:
                costo_kg = 2
            else:
                costo_kg = 1    
            costo+=(self.costo_km*conexion.distancia_km+self.costo_km+costo_kg*sobrante)
        return costo
        
    def calcular_tiempo(self, conexion, velocidad):
        tiempo=conexion.distancia_k/self.velocidad
        return tiempo
        
class Fluvial(Transporte): 
    def __init__(self):
        super().__init__("Fluvial", None, 40, 100000, 15, 2)

    def calcular_costo(self,conexion, carga):
        if conexion.restriccion:
            costo_fijo=1500
        else:
            costo_fijo=500
        cantidad=ceil(carga/self.capacidad)
        costo=cantidad*(self.costo_km*conexion.distancia_km+costo_fijo)+self.costo_kg*carga
        return costo
    
    def calcular_tiempo(self,conexion, velocidad):
        tiempo = conexion.distancia_km/self.velocidad
        return tiempo