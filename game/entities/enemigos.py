import pygame
from core.entidad_base import EntidadJuego #[cite: 6]

class EnemigoSlime(EntidadJuego):
    """Formas y animaciones por código de enemigos.""" #[cite: 2]
    def __init__(self, fila, columna, e, tam_celda):
        super().__init__(fila, columna, e, tam_celda) #[cite: 6]
        self.fase_animacion = 0

    def render(self, pantalla):
        """Dibuja al Slime usando primitivas gráficas.""" #[cite: 2]
        e = self.e #[cite: 6]
        lienzo = pygame.Surface((6 * e, 6 * e), pygame.SRCALPHA) #[cite: 6]
        
        VERDE_TOXICO = (50, 220, 50)
        VERDE_OSCURO = (20, 100, 20)
        
        # Cuerpo del slime (Elipse que se 'achata' según la fase)
        pygame.draw.ellipse(lienzo, VERDE_TOXICO, (1 * e, 3 * e, 4 * e, 2.5 * e))
        pygame.draw.ellipse(lienzo, VERDE_OSCURO, (1 * e, 3 * e, 4 * e, 2.5 * e), 2)
        
        # Ojos
        pygame.draw.circle(lienzo, (0, 0, 0), (int(2.5 * e), int(4 * e)), int(0.3 * e))
        pygame.draw.circle(lienzo, (0, 0, 0), (int(3.5 * e), int(4 * e)), int(0.3 * e))

        traslacion = lienzo.get_rect(topleft=(self.x, self.y)) #[cite: 6]
        pantalla.blit(lienzo, traslacion) #[cite: 6]

class VistaSectario(EntidadJuego):
    
    def __init__(self, fila, columna, e, tam_celda):
        super().__init__(fila, columna, e, tam_celda) #

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((6 * e, 6 * e), pygame.SRCALPHA)
        
        MORADO_OSCURO = (50, 10, 80)
        ROJO_SANGRE = (180, 20, 20)
        
        # Capucha (Primitiva de polígono)
        capucha = [(3*e, 1*e), (1.5*e, 5*e), (4.5*e, 5*e)]
        pygame.draw.polygon(lienzo, MORADO_OSCURO, capucha)
        
        # Ojos brillantes (Primitiva de círculo)
        pygame.draw.circle(lienzo, ROJO_SANGRE, (int(2.6*e), int(3*e)), int(0.2*e))
        pygame.draw.circle(lienzo, ROJO_SANGRE, (int(3.4*e), int(3*e)), int(0.2*e))
        
        pantalla.blit(lienzo, (self.x, self.y))

class VistaVagabundo(EntidadJuego):
    def __init__(self, fila, columna, e, tam_celda):
        super().__init__(fila, columna, e, tam_celda)

    def render(self, pantalla):
        e = self.e
        # Lienzo transparente de 6x6 unidades relativas
        lienzo = pygame.Surface((6 * e, 6 * e), pygame.SRCALPHA)
        
        VERDE_MUTANTE = (20, 50, 20)
        VERDE_OSCURO = (10, 30, 10)
        AMARILLO_OJO = (255, 215, 0)
        
        # 1. Protuberancias y bultos traseros
        pygame.draw.circle(lienzo, VERDE_OSCURO, (int(2.5*e), int(2*e)), int(1.5*e))
        pygame.draw.circle(lienzo, VERDE_OSCURO, (int(4*e), int(2.5*e)), int(1.2*e))
        
        # 2. Tentáculos asimétricos (Polígonos)
        tentaculo_izq = [(1.5*e, 3*e), (0.5*e, 5.5*e), (2*e, 4.5*e)]
        pygame.draw.polygon(lienzo, VERDE_OSCURO, tentaculo_izq)
        
        tentaculo_der = [(4.5*e, 3*e), (5.5*e, 5.5*e), (4*e, 4.5*e)]
        pygame.draw.polygon(lienzo, VERDE_OSCURO, tentaculo_der)
        
        # 3. Masa central del cuerpo
        pygame.draw.circle(lienzo, VERDE_MUTANTE, (int(3*e), int(3.5*e)), int(2*e))
        
        # 4. Ojo único rasgado y brillante
        # Globo ocular
        pygame.draw.ellipse(lienzo, AMARILLO_OJO, (int(2.2*e), int(2.2*e), int(1.6*e), int(0.8*e)))
        # Pupila vertical (reptiliana)
        pygame.draw.ellipse(lienzo, (0, 0, 0), (int(2.8*e), int(2.2*e), int(0.4*e), int(0.8*e)))
        
        pantalla.blit(lienzo, (self.x, self.y)) 