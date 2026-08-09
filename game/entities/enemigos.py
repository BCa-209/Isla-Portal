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
        super().__init__(fila, columna, e, tam_celda)

    def render(self, pantalla):
        e = self.e

        lienzo = pygame.Surface(
            (6 * e, 6 * e),
            pygame.SRCALPHA
        )

        TUNICA = (48, 35, 55)
        TUNICA_LUZ = (68, 52, 75)
        TUNICA_SOMBRA = (27, 21, 32)

        CAPUCHA = (38, 27, 45)
        CAPUCHA_LUZ = (58, 42, 64)

        PIEL = (170, 135, 115)
        PIEL_SOMBRA = (105, 78, 67)

        OJOS = (170, 25, 35)

        NEGRO = (10, 8, 12)


        tunica = [
            (2.0 * e, 3.0 * e),       # hombro izquierdo
            (4.0 * e, 3.0 * e),       # hombro derecho
            (4.55 * e, 5.8 * e),      # extremo inferior derecho
            (1.45 * e, 5.8 * e)       # extremo inferior izquierdo
        ]

        pygame.draw.polygon(
            lienzo,
            TUNICA,
            tunica
        )

        # Borde oscuro
        pygame.draw.polygon(
            lienzo,
            TUNICA_SOMBRA,
            tunica,
            max(1, int(0.12 * e))
        )

        # PLIEGUES DE LA TÚNICA

        # Pliegue izquierdo
        pygame.draw.polygon(lienzo, TUNICA_LUZ, [
            (2.0 * e, 3.15 * e),
            (2.45 * e, 3.25 * e),
            (2.25 * e, 5.7 * e),
            (1.7 * e, 5.7 * e)
        ])

        # Pliegue central
        pygame.draw.polygon(lienzo, TUNICA_SOMBRA, [
            (2.8 * e, 3.15 * e),
            (3.15 * e, 3.15 * e),
            (3.35 * e, 5.7 * e),
            (2.8 * e, 5.7 * e)
        ])

        # Pliegue derecho
        pygame.draw.polygon(lienzo, TUNICA_LUZ, [
            (3.55 * e, 3.2 * e),
            (4.0 * e, 3.15 * e),
            (4.3 * e, 5.7 * e),
            (3.7 * e, 5.7 * e)
        ])

        # BRAZO IZQUIERDO

        brazo_izq = [
            (2.05 * e, 3.05 * e),
            (1.6 * e, 3.35 * e),
            (1.35 * e, 4.75 * e),
            (1.8 * e, 4.85 * e),
            (2.35 * e, 3.55 * e)
        ]

        pygame.draw.polygon(
            lienzo,
            TUNICA_SOMBRA,
            brazo_izq
        )

        # BRAZO DERECHO

        brazo_der = [
            (3.95 * e, 3.05 * e),
            (4.4 * e, 3.35 * e),
            (4.65 * e, 4.75 * e),
            (4.2 * e, 4.85 * e),
            (3.65 * e, 3.55 * e)
        ]

        pygame.draw.polygon(
            lienzo,
            TUNICA_SOMBRA,
            brazo_der
        )

        # MANOS

        pygame.draw.circle(
            lienzo,
            PIEL_SOMBRA,
            (int(1.55 * e), int(4.8 * e)),
            int(0.28 * e)
        )

        pygame.draw.circle(
            lienzo,
            PIEL_SOMBRA,
            (int(4.45 * e), int(4.8 * e)),
            int(0.28 * e)
        )

        # CUELLO

        pygame.draw.rect(
            lienzo,
            PIEL_SOMBRA,
            pygame.Rect(
                int(2.55 * e),
                int(2.55 * e),
                int(0.9 * e),
                int(0.7 * e)
            )
        )

        # CABEZA

        pygame.draw.circle(
            lienzo,
            PIEL,
            (int(3.0 * e), int(2.25 * e)),
            int(0.85 * e)
        )

        # CAPUCHA PUNTIAGUDA

        # Forma exterior de la capucha.
        # La punta elevada hace que la silueta sea claramente
        # diferente de una persona normal.
        capucha = [
            (3.0 * e, 0.35 * e),      # punta
            (2.35 * e, 1.0 * e),
            (1.8 * e, 1.65 * e),
            (1.65 * e, 2.55 * e),

            (2.1 * e, 3.0 * e),
            (3.0 * e, 3.2 * e),

            (3.9 * e, 3.0 * e),
            (4.35 * e, 2.55 * e),
            (4.2 * e, 1.65 * e),
            (3.65 * e, 1.0 * e)
        ]

        pygame.draw.polygon(
            lienzo,
            CAPUCHA,
            capucha
        )

        # PARTE INTERIOR DE LA CAPUCHA

        interior = [
            (3.0 * e, 1.05 * e),
            (2.25 * e, 1.75 * e),
            (2.15 * e, 2.55 * e),
            (2.55 * e, 2.95 * e),
            (3.0 * e, 3.05 * e),
            (3.45 * e, 2.95 * e),
            (3.85 * e, 2.55 * e),
            (3.75 * e, 1.75 * e)
        ]

        pygame.draw.polygon(
            lienzo,
            NEGRO,
            interior
        )

        # ROSTRO EN SOMBRA

        # Parte visible de la cara
        pygame.draw.polygon(lienzo, PIEL_SOMBRA, [
            (2.45 * e, 2.1 * e),
            (3.55 * e, 2.1 * e),
            (3.45 * e, 2.7 * e),
            (3.0 * e, 2.95 * e),
            (2.55 * e, 2.7 * e)
        ])

        # OJOS BAJO LA CAPUCHA

        pygame.draw.circle(
            lienzo,
            OJOS,
            (int(2.65 * e), int(2.25 * e)),
            max(1, int(0.12 * e))
        )

        pygame.draw.circle(
            lienzo,
            OJOS,
            (int(3.35 * e), int(2.25 * e)),
            max(1, int(0.12 * e))
        )

        # BORDE INTERIOR DE LA CAPUCHA

        pygame.draw.line(
            lienzo,
            CAPUCHA_LUZ,
            (int(2.1 * e), int(2.65 * e)),
            (int(3.0 * e), int(3.05 * e)),
            max(1, int(0.12 * e))
        )

        pygame.draw.line(
            lienzo,
            CAPUCHA_LUZ,
            (int(3.0 * e), int(3.05 * e)),
            (int(3.9 * e), int(2.65 * e)),
            max(1, int(0.12 * e))
        )

        # SÍMBOLO DEL CULT0

        # Pequeño símbolo en el pecho.
        # No se hace demasiado grande para mantener la lectura
        # de la silueta.
        pygame.draw.circle(
            lienzo,
            CAPUCHA_LUZ,
            (int(3.0 * e), int(3.8 * e)),
            max(1, int(0.22 * e)),
            max(1, int(0.1 * e))
        )

        pygame.draw.line(
            lienzo,
            CAPUCHA_LUZ,
            (int(3.0 * e), int(3.55 * e)),
            (int(3.0 * e), int(4.05 * e)),
            max(1, int(0.1 * e))
        )

        # DIBUJAR EN PANTALLA

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

class VistaVagabundo(EntidadJuego):

    def __init__(self, fila, columna, e, tam_celda):
        super().__init__(fila, columna, e, tam_celda)

    def render(self, pantalla):
        e = self.e

        # LIENZO 6x6
        lienzo = pygame.Surface(
            (6 * e, 6 * e),
            pygame.SRCALPHA
        )

        # PALETA

        CUERPO = (45, 52, 43)
        CUERPO_LUZ = (65, 72, 58)
        CUERPO_SOMBRA = (25, 31, 25)

        OJO = (215, 190, 55)
        OJO_LUZ = (255, 225, 95)
        PUPILA = (15, 12, 10)

        GARRAS = (82, 77, 60)

        DIMENSIONAL = (75, 91, 72)

        NEGRO = (8, 8, 8)

        # 1. PATAS TRASERAS

        # Pata trasera izquierda
        pygame.draw.polygon(lienzo, CUERPO_SOMBRA, [
            (1.55 * e, 3.55 * e),
            (1.15 * e, 4.1 * e),
            (0.9 * e, 5.15 * e),
            (1.3 * e, 5.4 * e),
            (1.75 * e, 4.55 * e),
            (2.2 * e, 3.9 * e)
        ])

        # Pata trasera derecha
        pygame.draw.polygon(lienzo, CUERPO_SOMBRA, [
            (4.45 * e, 3.55 * e),
            (4.85 * e, 4.1 * e),
            (5.1 * e, 5.15 * e),
            (4.7 * e, 5.4 * e),
            (4.25 * e, 4.55 * e),
            (3.8 * e, 3.9 * e)
        ])

        # 2. PATAS DELANTERAS

        # Pata delantera izquierda
        pygame.draw.polygon(lienzo, CUERPO, [
            (2.0 * e, 3.4 * e),
            (1.55 * e, 3.85 * e),
            (1.35 * e, 5.05 * e),
            (1.7 * e, 5.4 * e),
            (2.15 * e, 4.45 * e),
            (2.5 * e, 3.7 * e)
        ])

        # Pata delantera derecha
        pygame.draw.polygon(lienzo, CUERPO, [
            (4.0 * e, 3.4 * e),
            (4.45 * e, 3.85 * e),
            (4.65 * e, 5.05 * e),
            (4.3 * e, 5.4 * e),
            (3.85 * e, 4.45 * e),
            (3.5 * e, 3.7 * e)
        ])

        # 3. GARRAS

        pygame.draw.polygon(lienzo, GARRAS, [
            (1.25 * e, 5.15 * e),
            (0.85 * e, 5.6 * e),
            (1.3 * e, 5.45 * e),
            (1.55 * e, 5.7 * e),
            (1.7 * e, 5.25 * e)
        ])

        pygame.draw.polygon(lienzo, GARRAS, [
            (4.3 * e, 5.25 * e),
            (4.45 * e, 5.7 * e),
            (4.7 * e, 5.45 * e),
            (5.15 * e, 5.6 * e),
            (4.75 * e, 5.15 * e)
        ])

        # 4. MASA AMORFA PRINCIPAL

        # Forma irregular pero redondeada.
        cuerpo = [
            (1.25 * e, 2.8 * e),
            (1.4 * e, 2.15 * e),
            (1.85 * e, 1.65 * e),
            (2.45 * e, 1.35 * e),
            (3.15 * e, 1.3 * e),
            (3.85 * e, 1.55 * e),
            (4.35 * e, 2.05 * e),
            (4.7 * e, 2.7 * e),
            (4.6 * e, 3.45 * e),
            (4.15 * e, 4.0 * e),
            (3.45 * e, 4.35 * e),
            (2.65 * e, 4.4 * e),
            (1.9 * e, 4.1 * e),
            (1.4 * e, 3.55 * e)
        ]

        pygame.draw.polygon(
            lienzo,
            CUERPO,
            cuerpo
        )

        # 5. BULTOS DE LA MASA

        # Joroba superior izquierda
        pygame.draw.circle(
            lienzo,
            CUERPO_LUZ,
            (int(2.15 * e), int(2.0 * e)),
            int(0.8 * e)
        )

        # Masa superior derecha
        pygame.draw.circle(
            lienzo,
            CUERPO_SOMBRA,
            (int(3.75 * e), int(2.15 * e)),
            int(0.9 * e)
        )

        # Masa inferior
        pygame.draw.circle(
            lienzo,
            CUERPO_SOMBRA,
            (int(3.15 * e), int(3.65 * e)),
            int(0.8 * e)
        )

        # 6. OJO ÚNICO

        # Cuenca oscura alrededor del ojo
        pygame.draw.ellipse(
            lienzo,
            NEGRO,
            pygame.Rect(
                int(1.75 * e),
                int(1.8 * e),
                int(2.5 * e),
                int(1.35 * e)
            )
        )

        # Globo ocular
        pygame.draw.ellipse(
            lienzo,
            OJO,
            pygame.Rect(
                int(1.95 * e),
                int(1.95 * e),
                int(2.1 * e),
                int(0.95 * e)
            )
        )

        # Brillo del ojo
        pygame.draw.circle(
            lienzo,
            OJO_LUZ,
            (int(2.45 * e), int(2.15 * e)),
            max(1, int(0.18 * e))
        )

        # Pupila vertical
        pygame.draw.ellipse(
            lienzo,
            PUPILA,
            pygame.Rect(
                int(2.85 * e),
                int(1.95 * e),
                int(0.35 * e),
                int(0.95 * e)
            )
        )

        # 7. TENTÁCULOS / EXTENSIONES

        # Extensión izquierda
        pygame.draw.polygon(lienzo, DIMENSIONAL, [
            (1.65 * e, 2.8 * e),
            (1.05 * e, 3.0 * e),
            (0.55 * e, 3.5 * e),
            (1.25 * e, 3.25 * e),
            (1.85 * e, 3.05 * e)
        ])

        # Extensión derecha
        pygame.draw.polygon(lienzo, DIMENSIONAL, [
            (4.25 * e, 2.75 * e),
            (4.85 * e, 2.9 * e),
            (5.35 * e, 3.35 * e),
            (4.65 * e, 3.2 * e),
            (4.05 * e, 3.0 * e)
        ])

        # 8. PEQUEÑAS PROTUBERANCIAS

        pygame.draw.circle(
            lienzo,
            DIMENSIONAL,
            (int(1.35 * e), int(2.05 * e)),
            max(1, int(0.2 * e))
        )

        pygame.draw.circle(
            lienzo,
            DIMENSIONAL,
            (int(4.4 * e), int(2.0 * e)),
            max(1, int(0.18 * e))
        )

        pygame.draw.circle(
            lienzo,
            CUERPO_LUZ,
            (int(3.9 * e), int(3.65 * e)),
            max(1, int(0.15 * e))
        )

        # 9. BOCA PEQUEÑA

        # Una abertura debajo del ojo.
        pygame.draw.ellipse(
            lienzo,
            NEGRO,
            pygame.Rect(
                int(2.45 * e),
                int(3.0 * e),
                int(1.1 * e),
                int(0.45 * e)
            )
        )

        # 10. ROTACIÓN Y TRASLACIÓN

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

class LiderSectario(EntidadJuego):

    def __init__(self, fila, columna, e, tam_celda):
        super().__init__(fila, columna, e, tam_celda)

    def render(self, pantalla):
        e = self.e

        # LIENZO 6x6
        lienzo = pygame.Surface(
            (6 * e, 6 * e),
            pygame.SRCALPHA
        )

        # PALETA

        TUNICA = (38, 32, 42)
        TUNICA_LUZ = (60, 51, 65)
        TUNICA_SOMBRA = (22, 19, 25)

        MASCARA = (215, 212, 198)
        MASCARA_SOMBRA = (165, 162, 150)

        PELO = (25, 22, 24)
        PELO_LUZ = (43, 38, 41)

        NEGRO = (8, 7, 9)

        OJOS = (105, 18, 25)

        # 1. TÚNICA PRINCIPAL

        tunica = [
            (2.0 * e, 2.8 * e),
            (4.0 * e, 2.8 * e),

            # hombro derecho
            (4.45 * e, 3.35 * e),

            # borde irregular
            (4.55 * e, 4.3 * e),
            (4.35 * e, 5.75 * e),
            (3.55 * e, 5.6 * e),
            (3.0 * e, 5.8 * e),
            (2.45 * e, 5.6 * e),
            (1.65 * e, 5.75 * e),

            (1.45 * e, 4.3 * e),
            (1.55 * e, 3.35 * e)
        ]

        pygame.draw.polygon(
            lienzo,
            TUNICA,
            tunica
        )

        # Borde exterior
        pygame.draw.polygon(
            lienzo,
            TUNICA_SOMBRA,
            tunica,
            max(1, int(0.1 * e))
        )

        # 2. PLIEGUES DE LA TÚNICA

        # Pliegue izquierdo
        pygame.draw.polygon(lienzo, TUNICA_LUZ, [
            (1.7 * e, 3.25 * e),
            (2.35 * e, 3.45 * e),
            (2.15 * e, 5.65 * e),
            (1.65 * e, 5.7 * e)
        ])

        # Pliegue central oscuro
        pygame.draw.polygon(lienzo, TUNICA_SOMBRA, [
            (2.7 * e, 3.2 * e),
            (3.2 * e, 3.2 * e),
            (3.35 * e, 5.7 * e),
            (2.75 * e, 5.75 * e)
        ])

        # Pliegue derecho
        pygame.draw.polygon(lienzo, TUNICA_LUZ, [
            (3.55 * e, 3.3 * e),
            (4.15 * e, 3.2 * e),
            (4.4 * e, 5.65 * e),
            (3.75 * e, 5.55 * e)
        ])

        # 3. BRAZOS

        # Brazo izquierdo
        pygame.draw.polygon(lienzo, TUNICA_SOMBRA, [
            (1.85 * e, 3.0 * e),
            (1.35 * e, 3.4 * e),
            (1.05 * e, 4.45 * e),
            (1.45 * e, 4.65 * e),
            (2.15 * e, 3.65 * e)
        ])

        # Brazo derecho
        pygame.draw.polygon(lienzo, TUNICA_SOMBRA, [
            (4.15 * e, 3.0 * e),
            (4.65 * e, 3.4 * e),
            (4.95 * e, 4.45 * e),
            (4.55 * e, 4.65 * e),
            (3.85 * e, 3.65 * e)
        ])

        # 4. MANOS

        # Manos parcialmente ocultas por las mangas
        pygame.draw.circle(
            lienzo,
            MASCARA_SOMBRA,
            (int(1.3 * e), int(4.55 * e)),
            max(1, int(0.22 * e))
        )

        pygame.draw.circle(
            lienzo,
            MASCARA_SOMBRA,
            (int(4.7 * e), int(4.55 * e)),
            max(1, int(0.22 * e))
        )

        # 5. CUELLO / SOMBRA

        pygame.draw.rect(
            lienzo,
            NEGRO,
            pygame.Rect(
                int(2.35 * e),
                int(2.35 * e),
                int(1.3 * e),
                int(0.8 * e)
            )
        )

        # 6. CABELLO MUY LARGO
        #
        # Se dibuja antes de la máscara para que caiga detrás
        # y alrededor del rostro.
        #

        cabello = [
            (1.75 * e, 1.2 * e),
            (2.1 * e, 0.75 * e),
            (2.75 * e, 0.6 * e),
            (3.35 * e, 0.65 * e),
            (3.9 * e, 1.0 * e),

            # lado derecho
            (4.2 * e, 1.75 * e),
            (4.3 * e, 2.65 * e),
            (4.15 * e, 3.55 * e),
            (4.25 * e, 4.35 * e),
            (3.8 * e, 4.85 * e),

            # lado izquierdo
            (3.6 * e, 4.25 * e),
            (3.45 * e, 3.3 * e),
            (2.55 * e, 3.3 * e),
            (2.4 * e, 4.35 * e),
            (2.15 * e, 4.9 * e),
            (1.75 * e, 4.25 * e),
            (1.85 * e, 3.4 * e),
            (1.55 * e, 2.55 * e)
        ]

        pygame.draw.polygon(
            lienzo,
            PELO,
            cabello
        )

        # 7. MECHONES DESALIÑADOS

        # Mechón izquierdo largo
        pygame.draw.polygon(lienzo, PELO_LUZ, [
            (1.85 * e, 1.35 * e),
            (2.2 * e, 1.0 * e),
            (2.25 * e, 2.1 * e),
            (2.0 * e, 3.5 * e),
            (2.15 * e, 4.7 * e),
            (1.75 * e, 4.25 * e),
            (1.8 * e, 3.0 * e)
        ])

        # Mechón derecho largo
        pygame.draw.polygon(lienzo, PELO_LUZ, [
            (3.65 * e, 1.1 * e),
            (4.0 * e, 1.5 * e),
            (4.05 * e, 2.8 * e),
            (3.9 * e, 3.8 * e),
            (4.0 * e, 4.65 * e),
            (3.65 * e, 4.25 * e),
            (3.5 * e, 3.2 * e)
        ])

        # Mechón central irregular
        pygame.draw.polygon(lienzo, PELO, [
            (2.65 * e, 0.7 * e),
            (3.0 * e, 0.55 * e),
            (3.35 * e, 0.75 * e),
            (3.15 * e, 1.5 * e),
            (2.8 * e, 1.75 * e),
            (2.55 * e, 1.3 * e)
        ])

        # 8. MÁSCARA BLANCA

        # Máscara ovalada ligeramente alargada
        mascara = [
            (2.35 * e, 1.15 * e),
            (2.75 * e, 0.95 * e),
            (3.25 * e, 1.0 * e),
            (3.65 * e, 1.3 * e),
            (3.75 * e, 2.0 * e),
            (3.55 * e, 2.7 * e),
            (3.0 * e, 2.95 * e),
            (2.45 * e, 2.7 * e),
            (2.25 * e, 2.0 * e)
        ]

        pygame.draw.polygon(
            lienzo,
            MASCARA,
            mascara
        )

        # Sombra inferior de la máscara
        pygame.draw.polygon(lienzo, MASCARA_SOMBRA, [
            (2.35 * e, 2.35 * e),
            (2.55 * e, 2.7 * e),
            (3.0 * e, 2.9 * e),
            (3.5 * e, 2.6 * e),
            (3.65 * e, 2.25 * e),
            (3.0 * e, 2.5 * e)
        ])

        # 9. OJOS DE LA MÁSCARA

        # Pequeñas aberturas oscuras.
        pygame.draw.ellipse(
            lienzo,
            NEGRO,
            pygame.Rect(
                int(2.5 * e),
                int(1.75 * e),
                int(0.45 * e),
                int(0.22 * e)
            )
        )

        pygame.draw.ellipse(
            lienzo,
            NEGRO,
            pygame.Rect(
                int(3.05 * e),
                int(1.75 * e),
                int(0.45 * e),
                int(0.22 * e)
            )
        )

        # 10. PEQUEÑO DETALLE ROJO

        # No son ojos brillantes; es una pequeña marca ritual.
        pygame.draw.circle(
            lienzo,
            OJOS,
            (int(3.0 * e), int(2.35 * e)),
            max(1, int(0.08 * e))
        )

        # 11. ROTACIÓN Y TRASLACIÓN

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
