class IAEnemigo:
    def __init__(self, tipo_enemigo):
        self.tipo = tipo_enemigo
        self.turno_actual = 0
        
        # Configuramos estadísticas y patrones según el tipo
        if tipo_enemigo == "jefe":
            self.hp_maximo = 150
            self.hp_actual = 150
            self.patron = ["ataque_rapido", "ritual", "ataque_pesado"]
            
        elif tipo_enemigo == "vagabundo":
            self.hp_maximo = 120
            self.hp_actual = 120
            self.patron = ["ataque_pesado", "embestida", "ataque_rapido", "embestida"]
            
        elif tipo_enemigo == "estatico": # Sectario normal
            self.hp_maximo = 60
            self.hp_actual = 60
            self.patron = ["ataque_rapido", "ritual", "ataque_rapido"]
            
        else: # "circulo" (Slimes o Bestias Oscuras)
            self.hp_maximo = 40
            self.hp_actual = 40
            self.patron = ["embestida", "ataque_rapido"]

    def elegir_accion(self):
        accion = self.patron[self.turno_actual]
        self.turno_actual = (self.turno_actual + 1) % len(self.patron)
        return accion
        
    def recibir_dano(self, cantidad):
        self.hp_actual -= cantidad
        if self.hp_actual < 0:
            self.hp_actual = 0