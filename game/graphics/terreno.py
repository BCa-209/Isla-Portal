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
            color_base = (60, 200, 220)
            color_brillo = (200, 255, 255)
        else:
            color_base = (20, 20, 25)
            color_brillo = (50, 50, 70)

        # Agua
        pygame.draw.rect(s, color_base, (x, y, tam, tam))

        # Olas
        grosor = max(1, tam // 15)

        pygame.draw.arc(
            s,
            color_brillo,
            (x + tam*0.1, y + tam*0.20,
            tam*0.45, tam*0.20),
            0,
            3.14,
            grosor
        )

        pygame.draw.arc(
            s,
            color_brillo,
            (x + tam*0.45, y + tam*0.50,
            tam*0.45, tam*0.20),
            0,
            3.14,
            grosor
        )

        pygame.draw.arc(
            s,
            color_brillo,
            (x + tam*0.15, y + tam*0.70,
            tam*0.40, tam*0.15),
            0,
            3.14,
            grosor
        )

        # Borde
        pygame.draw.rect(
            s,
            (0, 0, 0),
            (x, y, tam, tam),
            1
        )

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

    def _dibujar_cueva(self, s, x, y, tam):
        # Interior oscuro
        pygame.draw.rect(
            s,
            (15, 12, 10),
            (x + tam*0.2, y + tam*0.35, tam*0.6, tam*0.65)
        )

        # Marco antiguo de piedra
        piedra = (100, 85, 65)
        piedra_oscura = (65, 55, 45)

        # Laterales
        pygame.draw.rect(
            s,
            piedra_oscura,
            (x + tam*0.12, y + tam*0.35, tam*0.15, tam*0.6)
        )

        pygame.draw.rect(
            s,
            piedra_oscura,
            (x + tam*0.73, y + tam*0.35, tam*0.15, tam*0.6)
        )

        # Arco superior
        pygame.draw.arc(
            s,
            piedra,
            (x + tam*0.12, y + tam*0.08, tam*0.76, tam*0.65),
            3.14,
            6.28,
            max(2, tam//10)
        )

        # Piedra central decorativa
        pygame.draw.rect(
            s,
            piedra,
            (x + tam*0.43, y + tam*0.08, tam*0.14, tam*0.18)
        )

    def _dibujar_portal(self, s, x, y, tam, color_brillo):
        centro = (x + tam//2, y + tam*0.55)

        piedra = (90, 80, 65)
        piedra_clara = (120, 105, 85)

        # Fondo oscuro de la portada
        pygame.draw.rect(
            s,
            (15, 12, 15),
            (x + tam*0.18, y + tam*0.30,
            tam*0.64, tam*0.65)
        )

        # Orbe exterior
        pygame.draw.circle(
            s,
            color_brillo,
            centro,
            int(tam * 0.30)
        )

        # Orbe brillante
        color_claro = tuple(min(255, c + 70) for c in color_brillo)

        pygame.draw.circle(
            s,
            color_claro,
            centro,
            int(tam * 0.22)
        )

        # Núcleo de luz
        color_nucleo = tuple(min(255, c + 140) for c in color_brillo)

        pygame.draw.circle(
            s,
            color_nucleo,
            centro,
            int(tam * 0.12)
        )

        # Punto blanco de brillo
        pygame.draw.circle(
            s,
            (255, 255, 255),
            (
                int(x + tam * 0.45),
                int(y + tam * 0.45)
            ),
            max(1, int(tam * 0.045))
        )

        # Laterales de piedra
        pygame.draw.rect(
            s,
            piedra,
            (x + tam*0.08, y + tam*0.30,
            tam*0.15, tam*0.65)
        )

        pygame.draw.rect(
            s,
            piedra,
            (x + tam*0.77, y + tam*0.30,
            tam*0.15, tam*0.65)
        )

        # Arco de piedra
        pygame.draw.arc(
            s,
            piedra_clara,
            (x + tam*0.08, y + tam*0.05,
            tam*0.84, tam*0.65),
            3.14,
            6.28,
            max(2, tam//10)
        )
        
    def _dibujar_portal(self, s, x, y, tam, color_brillo):
        piedra = (90, 80, 65)
        piedra_clara = (120, 105, 85)

        # Centro oscuro
        pygame.draw.rect(
            s,
            (20, 15, 20),
            (x + tam*0.22, y + tam*0.30,
            tam*0.56, tam*0.65)
        )

        # Brillo exterior
        pygame.draw.rect(
            s,
            color_brillo,
            (x + tam*0.27, y + tam*0.35,
            tam*0.46, tam*0.55)
        )

        # Brillo interior
        color_claro = tuple(
            min(255, c + 80) for c in color_brillo
        )

        pygame.draw.rect(
            s,
            color_claro,
            (x + tam*0.34, y + tam*0.40,
            tam*0.32, tam*0.45)
        )

        # Núcleo muy brillante
        color_blanco = tuple(
            min(255, c + 150) for c in color_brillo
        )

        pygame.draw.rect(
            s,
            color_blanco,
            (x + tam*0.43, y + tam*0.45,
            tam*0.14, tam*0.35)
        )

        # Marco de piedra
        pygame.draw.rect(
            s,
            piedra,
            (x + tam*0.10, y + tam*0.30,
            tam*0.15, tam*0.65)
        )

        pygame.draw.rect(
            s,
            piedra,
            (x + tam*0.75, y + tam*0.30,
            tam*0.15, tam*0.65)
        )

        # Arco de piedra
        pygame.draw.arc(
            s,
            piedra_clara,
            (x + tam*0.10, y + tam*0.05,
            tam*0.80, tam*0.65),
            3.14,
            6.28,
            max(2, tam//10)
        )

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

    def _dibujar_arbol(self, s, x, y, tam):
        # Tronco
        pygame.draw.rect(
            s,
            (110, 65, 30),
            (x + tam*0.4, y + tam*0.45, tam*0.2, tam*0.45)
        )

        # Copa
        pygame.draw.circle(
            s,
            (35, 120, 35),
            (x + tam//2, y + tam*0.35),
            int(tam*0.35)
        )

        # Parte clara de la copa
        pygame.draw.circle(
            s,
            (55, 145, 45),
            (x + tam*0.4, y + tam*0.27),
            int(tam*0.18)
        )

    def _dibujar_ruinas(self, s, x, y, tam):
        piedra = (105, 95, 75)
        piedra_clara = (140, 125, 95)
        sombra = (65, 60, 50)

        # Suelo de las ruinas
        pygame.draw.rect(
            s,
            sombra,
            (x + tam*0.10, y + tam*0.75,
            tam*0.80, tam*0.15)
        )

        # Columna izquierda
        pygame.draw.rect(
            s,
            piedra,
            (x + tam*0.15, y + tam*0.30,
            tam*0.18, tam*0.50)
        )

        # Columna derecha rota
        pygame.draw.rect(
            s,
            piedra,
            (x + tam*0.67, y + tam*0.45,
            tam*0.18, tam*0.35)
        )

        # Parte superior de la columna izquierda
        pygame.draw.rect(
            s,
            piedra_clara,
            (x + tam*0.10, y + tam*0.25,
            tam*0.28, tam*0.10)
        )

        # Piedras caídas
        pygame.draw.rect(
            s,
            piedra_clara,
            (x + tam*0.38, y + tam*0.68,
            tam*0.18, tam*0.10)
        )

        pygame.draw.rect(
            s,
            piedra,
            (x + tam*0.55, y + tam*0.75,
            tam*0.12, tam*0.08)
        )

        # Grieta
        pygame.draw.line(
            s,
            sombra,
            (x + tam*0.45, y + tam*0.35),
            (x + tam*0.40, y + tam*0.60),
            max(1, tam//15)
        )

        # Borde
        pygame.draw.rect(
            s,
            (45, 40, 35),
            (x, y, tam, tam),
            1
        )