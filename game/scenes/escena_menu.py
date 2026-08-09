import pygame
import sys
from core.escena_base import EscenaBase
import config

class EscenaMenu(EscenaBase):
    def __init__(self):
        pygame.font.init()
        # Fuentes para el título y las instrucciones
        self.fuente_titulo = pygame.font.SysFont("arial", 64, bold=True)
        self.fuente_texto = pygame.font.SysFont("arial", 32)
        
        # Bandera para indicar al main.py cuándo cambiar de escena
        self.iniciar_juego = False

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Detectar si el jugador presiona ENTER para empezar
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    self.iniciar_juego = True

    def actualizar(self):
        # El menú no requiere actualizaciones matemáticas complejas en cada frame
        pass

    def render(self, pantalla):
        # Fondo oscuro para el menú
        pantalla.fill((20, 20, 30))
        
        # Renderizado del título
        titulo = self.fuente_titulo.render("ISLAS PORTAL", True, (0, 200, 255))
        rect_titulo = titulo.get_rect(center=(config.ANCHO // 2, config.ALTO // 3))
        
        # Renderizado de las instrucciones
        texto = self.fuente_texto.render("Presiona ENTER para iniciar", True, (255, 255, 255))
        rect_texto = texto.get_rect(center=(config.ANCHO // 2, config.ALTO // 2 + 50))
        
        pantalla.blit(titulo, rect_titulo)
        pantalla.blit(texto, rect_texto)