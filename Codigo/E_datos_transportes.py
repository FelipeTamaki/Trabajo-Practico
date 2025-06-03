# En  este archivo habria que hacer que se tenga la informacion sobre la velocidad maxima, los costos, etc y los llamas cuando hagas lo de dijkstra 
from math import ceil
class Transporte():
    def __init__(self,modo,costo_fijo,velocidad,capacidad,costo_km,costo_kg):
        self.modo = modo
        self.costo_fijo = costo_fijo
        self.velocidad = velocidad
        self.capacidad = capacidad
        self.costo_km = costo_km
        self.costo_kg = costo_kg
   

class Aereo(Transporte):
    def __init__(self, modo, costo_fijo, velocidad, capacidad, costo_km, costo_kg):
        super().__init__("Aerea", 750, [600,400], 5000, 40, 10)

    def calcular_costo(self,conexion, carga):
        cantidad= ceil(carga/self.capacidad)
        costo = cantidad *( self.costo_fijo+  self.costo_km*conexion.distancia_km)+ carga*self.costo_kg
        return costo

class Ferroviario(Transporte):
    def __init__(self, modo, costo_fijo, velocidad, capacidad, costo_km, costo_kg):
        super().__init__("Ferroviario", 100, 100, 150000, [15,20], 3)

    def calcular_costo(self, conexion, carga):
        if conexion.distancia >= 200: # Ver si la distancia es mayor a 200
            costo_km = self.costo_km[1]
        else:
            costo_km = self.costo_kg[0]
        cantidad=ceil(carga/self.capacidad)
        costo=cantidad*(costo_km*conexion.distancia_km+self.costo_fijo)+self.costo_kg*carga  
        return costo
        
class Automotor(Transporte):
    def __init__(self, modo, costo_fijo, velocidad, capacidad, costo_km, costo_kg):
        super().__init__("Automotor", 30, 80, 30000, 5, [1,2])

    def calcular_costo(self,conexion, carga):
        if conexion.restriccion:
            divisor = conexion.valor_restriccion
        else:
            divisor = self.capacidad

        if divisor >=15000:
            costo_kg = self.costo_kg[1]
        else:
            costo_kg = self.costo_kg[0]

        cantidad = carga//divisor
        costo=cantidad*(self.costo_km*conexion.distancia_km+self.costo_fijo+costo_kg*divisor)
        
        sobrante=carga%divisor
        if sobrante:
            if sobrante>=15000:
                costo_kg = self.costo_kg[1]
            else:
                costo_kg = self.costo_kg[0]
            costo+=(self.costo_km*conexion.distancia_km+self.costo_km+costo_kg*sobrante)
        return costo
        
class Fluvial(Transporte): 
    def __init__(self, modo, costo_fijo, velocidad, capacidad, costo_km, costo_kg):
        super().__init__("Fluvial", [500,1500], 40, 100000, 15, 2)

    def calcular_costo(self,conexion, carga):
        if conexion.restriccion:
            costo_fijo=self.costo_fijo[1]
        else:
            costo_fijo=self.costo_fijo[0]
        cantidad=ceil(carga/self.capacidad)
        costo=cantidad*(self.cos*conexion.distancia_km+costo_fijo)+self.costo_kg*carga
        return costo
