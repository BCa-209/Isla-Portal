class IAEnemigo:
    def __init__(self, es_jefe=False):
        if es_jefe:
            self.hp_maximo = 350
            self.hp_actual = 35
            self.patron = ["ataque_rapido", "ritual", "ataque_pesado"]
        else:
            self.hp_maximo = 150
            self.hp_actual = 15
            self.patron = ["embestida", "ataque_rapido", "embestida"]
            
        self.turno_actual = 0

    def elegir_accion(self):
        accion = self.patron[self.turno_actual]
        self.turno_actual = (self.turno_actual + 1) % len(self.patron)
        return accion
        
    def recibir_dano(self, cantidad):
        self.hp_actual -= cantidad
        if self.hp_actual < 0:
            self.hp_actual = 0