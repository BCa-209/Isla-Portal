import pygame
import sys
from core.escena_base import EscenaBase
from game.logic.finales_manager import EndingManager
import config

class EscenaJefe(EscenaBase):
    def __init__(self, inventario):
        pygame.font.init()
        self.fuente = pygame.font.SysFont("arial", 28, bold=True)
        
        # Recibimos el inventario actual para inyectarlo en el EndingManager
        self.inventario = inventario
        self.manager_finales = EndingManager(self.inventario)
        
        # Variables de estado del jefe
        self.resultado_final = None
        self.fase = "DECISION"  # Puede ser "DECISION" o "RESULTADO"

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Interacción de opciones solo si estamos en la fase de decisión
            if self.fase == "DECISION" and evento.type == pygame.KEYDOWN:
                decision = None
                
                if evento.key == pygame.K_1:
                    decision = "activar_portal"
                elif evento.key == pygame.K_2:
                    decision = "destruir_nucleo"
                elif evento.key == pygame.K_3:
                    decision = "huir"
                
                # Si se tomó una decisión válida, evaluamos el final y cambiamos de fase
                if decision:
                    self.resultado_final = self.manager_finales.evaluar_final(decision)
                    self.fase = "RESULTADO"

    def actualizar(self):
        # Aquí podría ir la lógica de ataque o animaciones del BossController
        pass

    def render(self, pantalla):
        # Fondo temático del monumento (rojo/oscuro)
        pantalla.fill((40, 10, 10))
        
        if self.fase == "DECISION":
            textos = [
                "¡Has llegado al núcleo del Monumento Antiguo!",
                "El Jefe Final aguarda tu decisión...",
                "",
                "[1] Usar llaves y activar el portal",
                "[2] Destruir el núcleo solar",
                "[3] Huir del archipiélago"
            ]
            
            # Dibujamos cada línea de texto centrada
            for i, linea in enumerate(textos):
                color = (255, 255, 255) if i < 3 else (200, 200, 200)
                superficie = self.fuente.render(linea, True, color)
                rect = superficie.get_rect(center=(config.ANCHO // 2, 150 + i * 45))
                pantalla.blit(superficie, rect)
                
        elif self.fase == "RESULTADO":
            # Mostramos el final desencadenado por el EndingManager
            texto_resultado = self.fuente.render(f"Has desencadenado el: {self.resultado_final}", True, (255, 215, 0))
            rect = texto_resultado.get_rect(center=(config.ANCHO // 2, config.ALTO // 2))
            pantalla.blit(texto_resultado, rect)