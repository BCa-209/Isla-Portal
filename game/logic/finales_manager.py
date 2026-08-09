class EndingManager:
    """Evaluación de condiciones para los finales.""" #[cite: 2]
    
    def __init__(self, inventario):
        self.inventario = inventario
        
    def evaluar_final(self, decision_jugador):
        """
        Dispara uno de los 5 finales (Normal, Bueno, Malo, Alternativo, Secreto)
        en base a la decisión del jugador y el estado del inventario.
        """ #[cite: 2]
        
        # Sistema basado en la obtención de los 5 Fragmentos Perdidos[cite: 2]
        if self.inventario.fragmentos == 5 and decision_jugador == "activar_portal":
            return "Final Bueno" #[cite: 2]
        elif self.inventario.fragmentos == 5 and decision_jugador == "destruir_nucleo":
            return "Final Secreto" #[cite: 2]
        elif self.inventario.fragmentos > 0 and decision_jugador == "activar_portal":
            return "Final Normal" #[cite: 2]
        elif self.inventario.fragmentos > 0 and decision_jugador == "huir":
            return "Final Alternativo" #[cite: 2]
        else:
            return "Final Malo" #[cite: 2]