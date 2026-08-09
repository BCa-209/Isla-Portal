import pygame
import math
from core.entidad_base import EntidadJuego #[cite: 6]

class Protagonista(EntidadJuego):
    def __init__(self, fila, columna, e, tam_celda):
        super().__init__(fila, columna, e, tam_celda)

    def render(self, pantalla):
        e = self.e

        lienzo = pygame.Surface((6 * e, 6 * e), pygame.SRCALPHA)

        # Piel
        PIEL = (205, 165, 135)
        PIEL_SOMBRA = (155, 115, 92)

        # Cabello
        PELO = (38, 34, 32)
        PELO_LUZ = (58, 51, 47)

        # Gabardina envejecida
        GABARDINA = (52, 52, 49)
        GABARDINA_LUZ = (70, 69, 63)
        GABARDINA_SOMBRA = (30, 31, 30)
        GABARDINA_DESGASTE = (82, 80, 71)

        # Camisa vieja
        CAMISA = (181, 178, 164)
        CAMISA_SOMBRA = (145, 142, 130)

        # Corbata
        CORBATA = (35, 34, 32)
        CORBATA_LUZ = (53, 51, 47)

        ZAPATO = (24, 23, 22)
        NEGRO = (10, 10, 10)

        pygame.draw.polygon(lienzo, GABARDINA_SOMBRA, [
            (2.0 * e, 4.6 * e),
            (2.8 * e, 4.6 * e),
            (2.7 * e, 5.7 * e),
            (1.9 * e, 5.7 * e)
        ])

        pygame.draw.polygon(lienzo, GABARDINA_SOMBRA, [
            (3.2 * e, 4.6 * e),
            (4.0 * e, 4.6 * e),
            (4.1 * e, 5.7 * e),
            (3.3 * e, 5.7 * e)
        ])

        # Zapatos desgastados
        pygame.draw.rect(
            lienzo,
            ZAPATO,
            pygame.Rect(
                int(1.65 * e),
                int(5.55 * e),
                int(1.2 * e),
                int(0.35 * e)
            )
        )

        pygame.draw.rect(
            lienzo,
            ZAPATO,
            pygame.Rect(
                int(3.2 * e),
                int(5.55 * e),
                int(1.2 * e),
                int(0.35 * e)
            )
        )

        cuerpo = [
            (1.55 * e, 3.0 * e),
            (4.45 * e, 3.0 * e),
            (4.65 * e, 3.55 * e),

            # borde inferior irregular
            (4.45 * e, 4.75 * e),
            (4.3 * e, 5.25 * e),
            (3.65 * e, 5.18 * e),
            (3.1 * e, 5.28 * e),
            (2.55 * e, 5.18 * e),
            (1.65 * e, 5.25 * e),
            (1.35 * e, 3.55 * e)
        ]

        pygame.draw.polygon(
            lienzo,
            GABARDINA,
            cuerpo
        )

        # Borde
        pygame.draw.polygon(
            lienzo,
            NEGRO,
            cuerpo,
            max(1, int(0.10 * e))
        )

        # Zona gastada izquierda
        pygame.draw.polygon(lienzo, GABARDINA_DESGASTE, [
            (1.55 * e, 3.55 * e),
            (1.85 * e, 3.45 * e),
            (2.05 * e, 4.35 * e),
            (1.75 * e, 4.7 * e)
        ])

        # Zona gastada derecha
        pygame.draw.polygon(lienzo, GABARDINA_SOMBRA, [
            (3.85 * e, 3.55 * e),
            (4.4 * e, 3.4 * e),
            (4.25 * e, 4.55 * e),
            (3.95 * e, 4.75 * e)
        ])

        # Pequeño desgaste inferior
        pygame.draw.polygon(lienzo, GABARDINA_DESGASTE, [
            (2.0 * e, 4.8 * e),
            (2.5 * e, 4.7 * e),
            (2.65 * e, 5.2 * e),
            (2.15 * e, 5.18 * e)
        ])

        pygame.draw.polygon(lienzo, GABARDINA_LUZ, [
            (1.7 * e, 3.1 * e),
            (2.75 * e, 3.25 * e),
            (2.35 * e, 4.0 * e),
            (1.75 * e, 3.65 * e)
        ])

        pygame.draw.polygon(lienzo, GABARDINA_SOMBRA, [
            (4.3 * e, 3.1 * e),
            (3.25 * e, 3.25 * e),
            (3.65 * e, 4.0 * e),
            (4.25 * e, 3.65 * e)
        ])

        pygame.draw.polygon(lienzo, CAMISA, [
            (2.35 * e, 3.05 * e),
            (3.65 * e, 3.05 * e),
            (3.35 * e, 3.75 * e),
            (2.65 * e, 3.75 * e)
        ])

        # Sombra / suciedad de la camisa
        pygame.draw.polygon(lienzo, CAMISA_SOMBRA, [
            (2.4 * e, 3.15 * e),
            (2.7 * e, 3.35 * e),
            (2.55 * e, 3.7 * e),
            (2.4 * e, 3.6 * e)
        ])

        pygame.draw.polygon(lienzo, CORBATA, [
            (2.82 * e, 3.12 * e),
            (3.15 * e, 3.15 * e),
            (3.25 * e, 3.65 * e),
            (3.0 * e, 4.0 * e),
            (2.78 * e, 3.65 * e)
        ])

        # Pequeño brillo/desgaste
        pygame.draw.line(
            lienzo,
            CORBATA_LUZ,
            (int(3.02 * e), int(3.45 * e)),
            (int(3.08 * e), int(3.75 * e)),
            max(1, int(0.08 * e))
        )

        pygame.draw.polygon(lienzo, CAMISA, [
            (2.35 * e, 2.85 * e),
            (2.75 * e, 3.25 * e),
            (3.0 * e, 3.05 * e),
            (3.25 * e, 3.25 * e),
            (3.65 * e, 2.85 * e)
        ])

        # Cuello de piel
        pygame.draw.rect(
            lienzo,
            PIEL_SOMBRA,
            pygame.Rect(
                int(2.55 * e),
                int(2.55 * e),
                int(0.9 * e),
                int(0.65 * e)
            )
        )

        # Masa principal
        pygame.draw.polygon(lienzo, PELO, [
            (1.85 * e, 1.45 * e),
            (2.15 * e, 0.95 * e),
            (2.7 * e, 0.75 * e),
            (3.3 * e, 0.75 * e),
            (3.85 * e, 0.95 * e),
            (4.15 * e, 1.45 * e),

            # lado derecho irregular
            (4.05 * e, 2.15 * e),
            (4.15 * e, 2.65 * e),
            (3.8 * e, 2.9 * e),

            # lado izquierdo irregular
            (3.55 * e, 2.35 * e),
            (2.45 * e, 2.35 * e),
            (2.3 * e, 2.85 * e),
            (1.9 * e, 2.7 * e)
        ])

        # Mechón izquierdo
        pygame.draw.polygon(lienzo, PELO_LUZ, [
            (1.9 * e, 1.35 * e),
            (2.2 * e, 1.0 * e),
            (2.35 * e, 1.75 * e),
            (2.15 * e, 2.75 * e),
            (1.9 * e, 2.55 * e)
        ])

        # Mechón derecho
        pygame.draw.polygon(lienzo, PELO, [
            (3.75 * e, 1.05 * e),
            (4.1 * e, 1.45 * e),
            (4.15 * e, 2.65 * e),
            (3.8 * e, 2.85 * e),
            (3.65 * e, 1.8 * e)
        ])

        pygame.draw.circle(
            lienzo,
            PIEL,
            (int(3 * e), int(1.95 * e)),
            int(1.05 * e)
        )

        # Sombra bajo el cabello
        pygame.draw.polygon(lienzo, PIEL_SOMBRA, [
            (2.2 * e, 2.25 * e),
            (2.45 * e, 2.65 * e),
            (3.55 * e, 2.65 * e),
            (3.8 * e, 2.25 * e),
            (3.65 * e, 2.55 * e),
            (2.35 * e, 2.55 * e)
        ])


        pygame.draw.polygon(lienzo, PELO, [
            (2.05 * e, 1.4 * e),
            (2.35 * e, 0.95 * e),
            (2.7 * e, 0.85 * e),
            (2.6 * e, 1.45 * e),
            (2.35 * e, 1.7 * e)
        ])

        pygame.draw.polygon(lienzo, PELO, [
            (2.65 * e, 0.85 * e),
            (3.05 * e, 0.75 * e),
            (3.5 * e, 0.95 * e),
            (3.2 * e, 1.45 * e),
            (2.85 * e, 1.3 * e)
        ])

        pygame.draw.rect(
            lienzo,
            NEGRO,
            pygame.Rect(
                int(2.35 * e),
                int(1.95 * e),
                max(1, int(0.25 * e)),
                max(1, int(0.15 * e))
            )
        )

        pygame.draw.rect(
            lienzo,
            NEGRO,
            pygame.Rect(
                int(3.4 * e),
                int(1.95 * e),
                max(1, int(0.25 * e)),
                max(1, int(0.15 * e))
            )
        )

        pygame.draw.line(
            lienzo,
            PIEL_SOMBRA,
            (int(3.0 * e), int(2.05 * e)),
            (int(2.9 * e), int(2.35 * e)),
            max(1, int(0.1 * e))
        )

        rotacion = pygame.transform.rotate(
            lienzo,
            self.alfa
        )

        traslacion = rotacion.get_rect(
            topleft=(self.x, self.y)
        )

        pantalla.blit(
            rotacion,
            traslacion
        )
