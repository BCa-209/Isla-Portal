class EndingManager:
    def __init__(self, inventario):
        self.inventario = inventario

    def evaluar_final(self, contexto, decision=None):
        """
        contexto: "muerte_comun", "muerte_jefe", "decision_monumento", "portal_morado"
        decision: "huir", "activar_portal"
        """
        
        # 1. Finales de Derrota
        if contexto == "muerte_comun":
            self.inventario.muertes_comunes += 1
            if self.inventario.muertes_comunes == 1:
                return "¿Primera vez?", "Has caído ante los horrores menores. La isla reclama tu cuerpo y tu mente se reinicia..."
            else:
                return "Consumido", "La oscuridad te ha devorado una vez más. Ya no hay esperanza."

        elif contexto == "muerte_jefe":
            return "El Sacrificio", "Tu luz se extinguió ante el Líder. Tu sangre ahora alimenta el ritual eterno del archipiélago."

        # 2. Final Verdadero (Ruta de la Locura)
        elif contexto == "portal_morado":
            if self.inventario.cordura <= 0:
                return "El Heraldo", "Has cruzado el velo mortal. Tu mente se ha apagado. Te unes a la Entidad Cósmica como su nuevo heraldo en la eternidad."
            else:
                # Opcional por si entra con cordura (aunque tu lógica la baja a 0 al entrar)
                return "La Mente Rota", "Viste lo que no debías. Sobreviviste, pero ya no eres de este mundo."

        # 3. Finales de Victoria (Ruta Clásica)
        elif contexto == "decision_monumento":
            if decision == "huir":
                return "El Retorno", "Derrotaste al líder y escapaste en una balsa. La isla sigue viva a tus espaldas... ¿Volverás a soñar con ella?"
                
            elif decision == "activar_portal":
                # Aquí evaluamos el esfuerzo del jugador explorando
                if self.inventario.fragmentos >= 5:
                    return "La Convergencia", "Canalizaste el poder de todos los cristales. El núcleo se purifica, sellando los portales. Ahora eres el guardián de estas tierras."
                else:
                    return "Fuga Incompleta", "Cruzaste el portal y salvaste tu vida, pero sientes un vacío. Los misterios de la isla quedaron sin resolver."