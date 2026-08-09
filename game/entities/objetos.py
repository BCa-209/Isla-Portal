import pygame
from core.entidad_base import BaseGrafica

class Cristal(BaseGrafica):
    def __init__(self, x, y, e, tipo="cristal"):
        super().__init__(x, y, e)
        self.tipo = tipo

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((6 * e, 6 * e), pygame.SRCALPHA)

        AZUL = (0, 200, 255)
        BLANCO = (255, 255, 255)

        centro = (3 * e, 3 * e)

        for radio in range(3 * e, 0, -max(1, e // 2)):
            alpha = int(35 * (radio / (3 * e)))
            pygame.draw.circle(
                lienzo,
                (0, 220, 255, alpha),
                centro,
                radio
            )

        diamante = [
            (3 * e, 0.5 * e),
            (5 * e, 3 * e),
            (3 * e, 5.5 * e),
            (1 * e, 3 * e)
        ]

        pygame.draw.polygon(lienzo, AZUL, diamante)
        pygame.draw.polygon(lienzo, BLANCO, diamante, max(1, e // 3))

        reflejo = [
            (3 * e, 1 * e),
            (4 * e, 2.7 * e),
            (3 * e, 2.2 * e),
            (2.4 * e, 2.8 * e)
        ]

        pygame.draw.polygon(lienzo, (220, 250, 255), reflejo)

        pygame.draw.line(
            lienzo,
            BLANCO,
            (3 * e, 1 * e),
            (3 * e, 2 * e),
            max(1, e // 3)
        )

        pygame.draw.line(
            lienzo,
            BLANCO,
            (2.5 * e, 1.5 * e),
            (3.5 * e, 1.5 * e),
            max(1, e // 3)
        )

        pantalla.blit(lienzo, (self.x, self.y))
class Moneda(BaseGrafica):
    def __init__(self, x, y, e, tipo="moneda"):
        super().__init__(x, y, e)
        self.tipo = tipo

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((6 * e, 6 * e), pygame.SRCALPHA)

        ORO = (245, 200, 30)
        ORO_BRILLO = (255, 225, 70)
        BORDE = (160, 120, 0)
        NEGRO = (35, 25, 10)
        BLANCO = (255, 255, 220)

        centro = (3 * e, 3 * e)

        for radio in range(3 * e, 0, -max(1, e // 2)):
            alpha = int(30 * (radio / (3 * e)))
            pygame.draw.circle(
                lienzo,
                (255, 210, 40, alpha),
                centro,
                radio
            )

        pygame.draw.circle(
            lienzo,
            ORO,
            centro,
            2 * e
        )

        pygame.draw.circle(
            lienzo,
            BORDE,
            centro,
            2 * e,
            max(1, e // 3)
        )

        pygame.draw.arc(
            lienzo,
            ORO_BRILLO,
            (1.3 * e, 1.3 * e, 3.4 * e, 3.4 * e),
            0.5,
            2.5,
            max(1, e // 3)
        )

        pygame.draw.circle(
            lienzo,
            NEGRO,
            (3 * e, 2.7 * e),
            int(1.05 * e)
        )

        pygame.draw.circle(
            lienzo,
            ORO,
            (3 * e, 2.2 * e),
            int(0.75 * e)
        )

        pygame.draw.circle(
            lienzo,
            NEGRO,
            (2.65 * e, 2.65 * e),
            int(0.32 * e)
        )

        pygame.draw.circle(
            lienzo,
            NEGRO,
            (3.35 * e, 2.65 * e),
            int(0.32 * e)
        )

        pygame.draw.polygon(
            lienzo,
            NEGRO,
            [
                (2.4 * e, 3.2 * e),
                (2.6 * e, 3.8 * e),
                (3.4 * e, 3.8 * e),
                (3.6 * e, 3.2 * e)
            ]
        )

        pygame.draw.line(
            lienzo,
            ORO,
            (2.65 * e, 3.45 * e),
            (2.65 * e, 3.85 * e),
            max(1, e // 3)
        )

        pygame.draw.line(
            lienzo,
            ORO,
            (3 * e, 3.45 * e),
            (3 * e, 3.85 * e),
            max(1, e // 3)
        )

        pygame.draw.line(
            lienzo,
            ORO,
            (3.35 * e, 3.45 * e),
            (3.35 * e, 3.85 * e),
            max(1, e // 3)
        )

        pygame.draw.line(
            lienzo,
            BLANCO,
            (2.1 * e, 1.8 * e),
            (2.7 * e, 1.5 * e),
            max(1, e // 3)
        )

        pantalla.blit(lienzo, (self.x, self.y))

class Pocion(BaseGrafica):
    def __init__(self, x, y, e, tipo="pocion"):
        super().__init__(x, y, e)
        self.tipo = tipo

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((6 * e, 6 * e), pygame.SRCALPHA)

        VERDE = (40, 200, 80)
        VERDE_OSCURO = (20, 120, 50)
        GRIS = (160, 160, 160)
        BLANCO = (255, 255, 255)

        pygame.draw.rect(
            lienzo,
            GRIS,
            (2.5 * e, 1.2 * e, e, 0.8 * e)
        )

        pygame.draw.rect(
            lienzo,
            VERDE_OSCURO,
            (2.4 * e, 1.0 * e, 1.2 * e, 0.25 * e)
        )

        pygame.draw.ellipse(
            lienzo,
            VERDE,
            (1.5 * e, 2 * e, 3 * e, 3 * e)
        )

        pygame.draw.ellipse(
            lienzo,
            VERDE_OSCURO,
            (1.5 * e, 2 * e, 3 * e, 3 * e),
            max(1, int(0.3 * e))
        )

        pygame.draw.circle(
            lienzo,
            BLANCO,
            (2.2 * e, 2.7 * e),
            max(1, int(0.3 * e))
        )

        pantalla.blit(lienzo, (self.x, self.y))
#--------------

class InteractableItem(BaseGrafica):
    def __init__(self, x, y, e, tipo="cristal"):
        super().__init__(x, y, e)
        self.tipo = tipo
        
        # Instanciamos el objeto correcto pasando las coordenadas reales
        if self.tipo == "cristal":
            self.objeto_real = Cristal(x, y, e)
        elif self.tipo == "moneda":
            self.objeto_real = Moneda(x, y, e)
        elif self.tipo == "pocion":
            self.objeto_real = Pocion(x, y, e)
        else:
            self.objeto_real = None

    def render(self, pantalla):
        # Delegamos el renderizado al objeto instanciado para evitar dobles lienzos
        if self.objeto_real:
            self.objeto_real.render(pantalla)

#---------------------

class Llave(BaseGrafica):
    """
    tipo:
        "jungla"
        "desierto"
        "cofre"
    """

    def __init__(self, x, y, e, tipo="jungla"):
        super().__init__(x, y, e)
        self.tipo = tipo

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((8*e, 8*e), pygame.SRCALPHA)

        if self.tipo == "jungla":
            self._llave_jungla(lienzo, e)

        elif self.tipo == "desierto":
            self._llave_desierto(lienzo, e)

        else:
            self._llave_cofre(lienzo, e)

        pantalla.blit(lienzo, (self.x, self.y))

    # ----------------------------------------------------------

    def _llave_jungla(self, s, e):
        VERDE_MUSGO = (55, 115, 45)
        VERDE_OSCURO = (20, 65, 30)
        VERDE_PROFUNDO = (10, 45, 22)
        VERDE_BRILLO = (90, 150, 55)
        MARRON = (75, 55, 30)

        pygame.draw.circle(
            s,
            VERDE_PROFUNDO,
            (2 * e, 4 * e),
            int(1.15 * e)
        )

        pygame.draw.circle(
            s,
            VERDE_MUSGO,
            (2 * e, 4 * e),
            int(0.85 * e)
        )

        pygame.draw.circle(
            s,
            VERDE_PROFUNDO,
            (2 * e, 4 * e),
            int(0.42 * e)
        )

        pygame.draw.rect(
            s,
            VERDE_MUSGO,
            (2.5 * e, 3.65 * e, 3.0 * e, 0.7 * e)
        )

        pygame.draw.rect(
            s,
            VERDE_OSCURO,
            (2.5 * e, 4.15 * e, 3.0 * e, 0.2 * e)
        )

        pygame.draw.rect(
            s,
            VERDE_MUSGO,
            (5.0 * e, 3.65 * e, 0.55 * e, 1.4 * e)
        )

        pygame.draw.rect(
            s,
            VERDE_MUSGO,
            (4.2 * e, 3.65 * e, 0.55 * e, 0.9 * e)
        )

        pygame.draw.polygon(
            s,
            VERDE_OSCURO,
            [
                (2.7 * e, 3.1 * e),
                (3.6 * e, 2.0 * e),
                (4.4 * e, 2.9 * e),
                (3.7 * e, 3.3 * e)
            ]
        )

        pygame.draw.polygon(
            s,
            VERDE_PROFUNDO,
            [
                (3.5 * e, 2.8 * e),
                (4.1 * e, 2.1 * e),
                (4.7 * e, 2.7 * e),
                (4.0 * e, 3.0 * e)
            ]
        )

        pygame.draw.polygon(
            s,
            VERDE_OSCURO,
            [
                (3.4 * e, 4.7 * e),
                (4.3 * e, 5.65 * e),
                (4.9 * e, 4.7 * e),
                (4.1 * e, 4.5 * e)
            ]
        )

        pygame.draw.arc(
            s,
            VERDE_PROFUNDO,
            (1.0 * e, 2.4 * e, 2.8 * e, 3.4 * e),
            0.5,
            4.8,
            max(1, int(0.18 * e))
        )

        pygame.draw.polygon(
            s,
            VERDE_BRILLO,
            [
                (2.8 * e, 3.0 * e),
                (2.25 * e, 2.55 * e),
                (2.45 * e, 3.3 * e)
            ]
        )

        pygame.draw.line(
            s,
            MARRON,
            (2.7 * e, 3.9 * e),
            (4.8 * e, 3.9 * e),
            max(1, int(0.15 * e))
        )

    # ----------------------------------------------------------

    def _llave_desierto(self, s, e):
        PIEDRA = (155, 125, 75)
        PIEDRA_CLARA = (190, 155, 95)
        PIEDRA_OSCURA = (95, 75, 45)
        SOMBRA = (65, 55, 40)
        GEMA = (185, 95, 35)
        GEMA_OSCURA = (110, 50, 25)

        pygame.draw.polygon(
            s,
            PIEDRA_OSCURA,
            [
                (2 * e, 2.7 * e),
                (3.0 * e, 3.35 * e),
                (3.0 * e, 4.65 * e),
                (2 * e, 5.3 * e),
                (1 * e, 4.65 * e),
                (1 * e, 3.35 * e)
            ]
        )

        pygame.draw.polygon(
            s,
            PIEDRA,
            [
                (2 * e, 2.9 * e),
                (2.8 * e, 3.4 * e),
                (2.8 * e, 4.6 * e),
                (2 * e, 5.0 * e),
                (1.2 * e, 4.6 * e),
                (1.2 * e, 3.4 * e)
            ]
        )

        pygame.draw.polygon(
            s,
            SOMBRA,
            [
                (2 * e, 3.25 * e),
                (2.5 * e, 3.55 * e),
                (2.5 * e, 4.45 * e),
                (2 * e, 4.7 * e),
                (1.5 * e, 4.45 * e),
                (1.5 * e, 3.55 * e)
            ]
        )

        pygame.draw.rect(
            s,
            PIEDRA,
            (2.5 * e, 3.7 * e, 3.0 * e, 0.7 * e)
        )

        pygame.draw.rect(
            s,
            PIEDRA_OSCURA,
            (2.5 * e, 4.15 * e, 3.0 * e, 0.2 * e)
        )

        pygame.draw.rect(
            s,
            PIEDRA,
            (5.0 * e, 3.7 * e, 0.55 * e, 1.35 * e)
        )

        pygame.draw.rect(
            s,
            PIEDRA,
            (4.2 * e, 3.7 * e, 0.55 * e, 0.9 * e)
        )

        pygame.draw.polygon(
            s,
            GEMA_OSCURA,
            [
                (2 * e, 2.45 * e),
                (2.5 * e, 3 * e),
                (2 * e, 3.55 * e),
                (1.5 * e, 3 * e)
            ]
        )

        pygame.draw.polygon(
            s,
            GEMA,
            [
                (2 * e, 2.65 * e),
                (2.3 * e, 3 * e),
                (2 * e, 3.35 * e),
                (1.7 * e, 3 * e)
            ]
        )

        pygame.draw.line(
            s,
            PIEDRA_CLARA,
            (1.35 * e, 3.45 * e),
            (1.7 * e, 3.15 * e),
            max(1, int(0.18 * e))
        )

        pygame.draw.line(
            s,
            PIEDRA_OSCURA,
            (2.65 * e, 4.55 * e),
            (2.35 * e, 4.85 * e),
            max(1, int(0.18 * e))
        )

        pygame.draw.line(
            s,
            PIEDRA_OSCURA,
            (3.2 * e, 3.85 * e),
            (3.5 * e, 4.05 * e),
            max(1, int(0.15 * e))
        )

    # ----------------NO USADA-------------------------

    def _llave_cofre(self, s, e):
        MORADO = (170, 70, 255)
        DORADO = (255, 215, 0)
        BLANCO = (255,255,255)

        # aro con estrella
        pygame.draw.circle(s, DORADO, (2*e,4*e), e)
        pygame.draw.circle(s, (0,0,0,0), (2*e,4*e), int(0.5*e))

        estrella = [
            (2*e,2.7*e),
            (2.3*e,3.6*e),
            (3.2*e,3.6*e),
            (2.5*e,4.1*e),
            (2.8*e,5*e),
            (2*e,4.4*e),
            (1.2*e,5*e),
            (1.5*e,4.1*e),
            (0.8*e,3.6*e),
            (1.7*e,3.6*e)
        ]
        pygame.draw.polygon(s, MORADO, estrella)

        # mango
        pygame.draw.rect(s, DORADO, (2*e,3.7*e,4.8*e,0.6*e))

        # dientes elaborados
        pygame.draw.rect(s, DORADO, (5.3*e,3.7*e,0.5*e,1.6*e))
        pygame.draw.rect(s, DORADO, (6.1*e,3.7*e,0.5*e,e))
        pygame.draw.rect(s, DORADO, (4.5*e,3.7*e,0.5*e,0.8*e))

        # brillo
        pygame.draw.line(s, BLANCO, (5.8*e,2.5*e), (6.3*e,3*e), 1)
        pygame.draw.line(s, BLANCO, (6.3*e,2.5*e), (5.8*e,3*e), 1)