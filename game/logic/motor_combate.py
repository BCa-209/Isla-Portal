class CombatManager:
    def __init__(self, inventario_jugador):
        self.inventario = inventario_jugador
        self.estado = "SELECCION" 
        
        self.acciones = {
            "ataque_rapido": {"dano": 15, "prep": 36, "tipo": "ataque"}, 
            "ataque_pesado": {"dano": 35, "prep": 108, "tipo": "ataque"}, 
            "pocion": {"curacion": 30, "prep": 30, "tipo": "curacion"}, 
            "observar": {"prep": 48, "tipo": "utilidad"}, 
            "ritual": {"dano": 50, "prep": 72, "tipo": "ataque"},
            "embestida": {"dano": 20, "prep": 45, "tipo": "ataque"}
        }
        
        self.resetear_turno()

    def resetear_turno(self):
        self.accion_jugador = None
        self.accion_enemigo = None
        self.timer_jugador = 0
        self.timer_enemigo = 0
        self.estado = "SELECCION"

    def fijar_acciones(self, id_accion_jugador, id_accion_enemigo):
        self.accion_jugador = self.acciones[id_accion_jugador]
        self.accion_enemigo = self.acciones[id_accion_enemigo]
        self.estado = "EJECUCION"

    def actualizar_timers(self):
        if self.estado != "EJECUCION":
            return None

        self.timer_jugador += 1
        self.timer_enemigo += 1

        jugador_listo = self.timer_jugador >= self.accion_jugador["prep"]
        enemigo_listo = self.timer_enemigo >= self.accion_enemigo["prep"]

        if jugador_listo and enemigo_listo:
            return "empate"
        elif jugador_listo:
            return "jugador_primero"
        elif enemigo_listo:
            return "enemigo_primero"
            
        return None

    def obtener_info_enemigo(self):
        if self.inventario.cordura < 60:
            return "???"
        else:
            return self.accion_enemigo