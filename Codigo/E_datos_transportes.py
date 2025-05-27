# En  este archivo habria que hacer que se tenga la informacion sobre la velocidad maxima, los costos, etc y los llamas cuando hagas lo de dijkstra 
class Transporte():
    def __init__(self, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg):
        self.modo=modo
        self.velocidad=velocidad
        self.capacidad=capacidad
        self.costo_fijo=costo_fijo
        self.costo_km=costo_km
        self.costo_kg=costo_kg
        ANDA AL DE GRAFOS 
class Aereo(Transporte):
    pass
class Ferroviario(Transporte):
    pass
class Automotor(Transporte):
    pass
class Fluvial(Transporte): # No estoy seguro si se divide en fluvial y maritimo o no
    pass
