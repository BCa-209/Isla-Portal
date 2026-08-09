import pygame
import math
from core.entidad_base import EntidadJuego #[cite: 6]

class Protagonista(EntidadJuego):
    def __init__(self, fila, columna, e, tam_celda):
        super().__init__(fila, columna, e, tam_celda) #

    def render(self, pantalla):
        e = self.e 
        lienzo = pygame.Surface((6 * e, 6 * e), pygame.SRCALPHA)
        
        AZUL_CAPA = (40, 80, 200)
        PIEL = (255, 220, 180)
        
        # Cabeza (Círculo primitivo)[cite: 2, 6]
        pygame.draw.circle(lienzo, PIEL, (int(3 * e), int(2 * e)), int(1.2 * e))
        
        # Cuerpo / Capa (Polígono primitivo)[cite: 2, 6]
        cuerpo = [
            (2 * e, 3 * e),
            (4 * e, 3 * e),
            (4.5 * e, 5 * e),
            (1.5 * e, 5 * e)
        ]
        pygame.draw.polygon(lienzo, AZUL_CAPA, cuerpo)
        pygame.draw.polygon(lienzo, (0, 0, 0), cuerpo, 2) # Borde[cite: 6]

        # Rotación y traslación heredada del motor base[cite: 6]
        rotacion = pygame.transform.rotate(lienzo, self.alfa) #[cite: 6]
        traslacion = rotacion.get_rect(topleft=(self.x, self.y)) #[cite: 6]
        pantalla.blit(rotacion, traslacion) #[cite: 6]