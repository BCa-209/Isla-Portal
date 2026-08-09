import pygame
import random

class TileManager:
    """Gestor visual para renderizar las baldosas del mapa utilizando primitivas gráficas."""
    
    def dibujar_casilla(self, superficie, tipo, x, y, tam, nivel):
        # Dibujar siempre el fondo por defecto (Tierra) para evitar huecos en objetos translúcidos
        if tipo not in [1, 2, 3, 5, 6, 10]:
            self._dibujar_tierra(superficie, x, y, tam, nivel)
            return

        # Dibujar elementos específicos del fondo
        if tipo == 1: # AGUA
            self._dibujar_agua(superficie, x, y, tam, nivel)
        elif tipo == 2: # ROCA
            self._dibujar_roca(superficie, x, y, tam, nivel)
        elif tipo == 3: # PORTAL PARA AVANZAR
            self._dibujar_tierra(superficie, x, y, tam, nivel)
            self._dibujar_portal(superficie, x, y, tam, (0, 150, 255))
        elif tipo == 6: # PORTAL PARA REGRESAR
            self._dibujar_tierra(superficie, x, y, tam, nivel)
            self._dibujar_portal(superficie, x, y, tam, (255, 50, 50))
        elif tipo == 10: # CUEVA
            self._dibujar_tierra(superficie, x, y, tam, nivel)
            self._dibujar_cueva(superficie, x, y, tam)
        elif tipo == 5: # JEFE
            self._dibujar_tierra(superficie, x, y, tam, nivel)
            self._dibujar_jefe(superficie, x, y, tam)

    def _dibujar_tierra(self, s, x, y, tam, nivel):
        if nivel == 4: # Cueva profunda
            color_base = (40, 30, 30)
            pygame.draw.rect(s, color_base, (x, y, tam, tam))
            # Textura de suelo lúgubre (puntos oscuros)
            pygame.draw.circle(s, (25, 15, 15), (x + int(tam*0.3), y + int(tam*0.7)), int(tam*0.1))
            pygame.draw.circle(s, (25, 15, 15), (x + int(tam*0.7), y + int(tam*0.3)), int(tam*0.15))
            
        elif nivel == 1: # Jungla
            color_base = (80, 160, 80)
            pygame.draw.rect(s, color_base, (x, y, tam, tam))
            # Hojas de pasto (pequeñas líneas en 'V')
            pygame.draw.line(s, (50, 120, 50), (x + tam*0.2, y + tam*0.8), (x + tam*0.3, y + tam*0.5), 2)
            pygame.draw.line(s, (50, 120, 50), (x + tam*0.4, y + tam*0.8), (x + tam*0.3, y + tam*0.5), 2)
            
        elif nivel == 2: # Desierto
            color_base = (210, 180, 140)
            pygame.draw.rect(s, color_base, (x, y, tam, tam))
            # Líneas onduladas para simular dunas de arena
            pygame.draw.arc(s, (180, 150, 110), (x, y + tam//4, tam, tam), 0, 3.14, 2)
            
        else: # Monumento
            color_base = (90, 90, 100)
            pygame.draw.rect(s, color_base, (x, y, tam, tam))
            # Baldosas antiguas (cuadrícula interna sutil)
            pygame.draw.rect(s, (70, 70, 80), (x + 2, y + 2, tam - 4, tam - 4), 1)
            
        # Borde general de grilla
        pygame.draw.rect(s, (0, 0, 0), (x, y, tam, tam), 1)

    def _dibujar_agua(self, s, x, y, tam, nivel):
        if nivel == 1:
            color_base = (28, 107, 160)
            color_brillo = (135, 206, 235)
        elif nivel == 2:
            color_base = (60, 200, 220) # Oasis más claro
            color_brillo = (200, 255, 255)
        else:
            color_base = (20, 20, 25) # Aguas oscuras/abismo
            color_brillo = (50, 50, 70)
            
        pygame.draw.rect(s, color_base, (x, y, tam, tam))
        
        # Olas horizontales con primitivas
        pygame.draw.line(s, color_brillo, (x + tam*0.2, y + tam*0.3), (x + tam*0.5, y + tam*0.3), max(1, tam//15))
        pygame.draw.line(s, color_brillo, (x + tam*0.5, y + tam*0.7), (x + tam*0.8, y + tam*0.7), max(1, tam//15))
        pygame.draw.rect(s, (0, 0, 0), (x, y, tam, tam), 1)

    def _dibujar_roca(self, s, x, y, tam, nivel):
        if nivel == 4:
            color_base = (15, 15, 15)
            color_relieve = (30, 30, 30)
        elif nivel == 1:
            color_base = (100, 100, 100)
            color_relieve = (130, 130, 130)
        elif nivel == 2:
            color_base = (180, 150, 110)
            color_relieve = (210, 180, 140)
        else:
            color_base = (60, 60, 70)
            color_relieve = (90, 90, 100)
            
        pygame.draw.rect(s, color_base, (x, y, tam, tam))
        
        # Polígono poligonal interno para dar efecto de volumen o bisel
        poligono = [
            (x + tam*0.1, y + tam*0.1),
            (x + tam*0.8, y + tam*0.2),
            (x + tam*0.9, y + tam*0.9),
            (x + tam*0.2, y + tam*0.8)
        ]
        pygame.draw.polygon(s, color_relieve, poligono)
        pygame.draw.polygon(s, (0,0,0), poligono, 1) # Borde de las fisuras
        pygame.draw.rect(s, (0, 0, 0), (x, y, tam, tam), 1)

    def _dibujar_portal(self, s, x, y, tam, color_brillo):
        centro = (x + tam//2, y + tam//2)
        # Anillos concéntricos
        pygame.draw.circle(s, color_brillo, centro, tam//2 - 2, 2)
        pygame.draw.circle(s, (255, 255, 255), centro, tam//3, 1)
        # Estrella central
        pygame.draw.line(s, color_brillo, (x+tam*0.2, y+tam//2), (x+tam*0.8, y+tam//2), 2)
        pygame.draw.line(s, color_brillo, (x+tam//2, y+tam*0.2), (x+tam//2, y+tam*0.8), 2)

    def _dibujar_cueva(self, s, x, y, tam):
        centro = (x + tam//2, y + tam//2)
        # Efecto de abismo profundo (Círculos oscuros hacia el centro)
        pygame.draw.circle(s, (20, 20, 20), centro, tam//2 - 2)
        pygame.draw.circle(s, (10, 10, 10), centro, tam//3)
        pygame.draw.circle(s, (0, 0, 0), centro, tam//4)

    def _dibujar_jefe(self, s, x, y, tam):
        # Alfombra o marca roja de combate
        pygame.draw.rect(s, (100, 20, 20), (x + 2, y + 2, tam - 4, tam - 4))
        # Rombos decorativos de amenaza
        rombo = [
            (x + tam//2, y + tam*0.1),
            (x + tam*0.9, y + tam//2),
            (x + tam//2, y + tam*0.9),
            (x + tam*0.1, y + tam//2)
        ]
        pygame.draw.polygon(s, (150, 0, 0), rombo, 2)