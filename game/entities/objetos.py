import pygame
from core.entidad_base import BaseGrafica

class Cristal(BaseGrafica):
    def __init__(self, x, y, e, tipo="cristal"):
        super().__init__(x, y, e)
        self.tipo = tipo

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((6*e, 6*e), pygame.SRCALPHA)

        AZUL = (0, 200, 255)
        BLANCO = (255, 255, 255)

        diamante = [
            (3*e, 0.5*e),
            (5*e, 3*e),
            (3*e, 5.5*e),
            (1*e, 3*e)
        ]

        pygame.draw.polygon(lienzo, AZUL, diamante)
        pygame.draw.polygon(lienzo, BLANCO, diamante, 1)

        # Descomentado para que el objeto realmente se dibuje
        pantalla.blit(lienzo, (self.x, self.y))


class Moneda(BaseGrafica):
    def __init__(self, x, y, e, tipo="moneda"):
        super().__init__(x, y, e)
        self.tipo = tipo

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((6*e, 6*e), pygame.SRCALPHA)

        ORO = (245, 200, 30)
        BORDE = (160, 120, 0)

        pygame.draw.circle(lienzo, ORO, (3*e, 3*e), 2*e)
        pygame.draw.circle(lienzo, BORDE, (3*e, 3*e), 2*e, 1)

        pygame.draw.line(lienzo, BORDE, (3*e, 1.7*e), (3*e, 4.3*e), 2)
        pygame.draw.line(lienzo, BORDE, (2*e, 3*e), (4*e, 3*e), 2)

        pantalla.blit(lienzo, (self.x, self.y))


class Pocion(BaseGrafica):
    def __init__(self, x, y, e, tipo="pocion"):
        super().__init__(x, y, e)
        self.tipo = tipo

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((6*e, 6*e), pygame.SRCALPHA)

        ROJO = (220, 40, 60)
        GRIS = (180, 180, 180)
        BLANCO = (255, 255, 255)

        # Cuello
        pygame.draw.rect(lienzo, GRIS, (2.5*e, 0.8*e, e, e))

        # Frasco
        pygame.draw.ellipse(lienzo, ROJO, (1*e, 1.5*e, 4*e, 4*e))
        pygame.draw.ellipse(lienzo, BLANCO, (1*e, 1.5*e, 4*e, 4*e), 1)

        # Brillo
        pygame.draw.circle(lienzo, (255,255,255), (2*e, 2.5*e), int(0.4*e))

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
        VERDE = (40, 170, 70)
        OSCURO = (20, 100, 40)

        # aro
        pygame.draw.circle(s, VERDE, (2*e, 4*e), e)
        pygame.draw.circle(s, (0,0,0,0), (2*e,4*e), int(0.55*e))

        # tallo
        pygame.draw.rect(s, VERDE, (2*e,3.7*e,4*e,0.6*e))

        # dientes
        pygame.draw.rect(s, VERDE, (5.2*e,3.7*e,0.5*e,1.5*e))
        pygame.draw.rect(s, VERDE, (4.2*e,3.7*e,0.5*e,e))

        # hojas
        pygame.draw.polygon(s, OSCURO,
            [(3*e,3*e),(4*e,2.2*e),(4.5*e,3*e)])
        pygame.draw.polygon(s, OSCURO,
            [(3.8*e,5*e),(4.8*e,5.8*e),(4.5*e,4.8*e)])

    # ----------------------------------------------------------

    def _llave_desierto(self, s, e):
        ORO = (228, 185, 60)
        MARRON = (160, 110, 30)

        # aro hexagonal
        pygame.draw.polygon(s, ORO, [
            (2*e,2.8*e),
            (3*e,3.4*e),
            (3*e,4.6*e),
            (2*e,5.2*e),
            (1*e,4.6*e),
            (1*e,3.4*e)
        ], 0)

        pygame.draw.circle(s, (0,0,0,0), (2*e,4*e), int(0.45*e))

        # mango
        pygame.draw.rect(s, ORO, (2*e,3.7*e,4.5*e,0.6*e))

        # dientes
        pygame.draw.rect(s, ORO, (5.5*e,3.7*e,0.5*e,1.2*e))
        pygame.draw.rect(s, ORO, (4.6*e,3.7*e,0.5*e,0.8*e))

        # gema
        pygame.draw.polygon(s, MARRON, [
            (2*e,2.5*e),
            (2.4*e,3*e),
            (2*e,3.5*e),
            (1.6*e,3*e)
        ])

    # ----------------------------------------------------------

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