import pygame
import sys
import json
import math
import os
from core.escena_base import EscenaBase
from game.logic.finales_manager import EndingManager
from game.logic.inventario import PlayerInventory
from game.sounds.gestor_audio import SoundManager
import config

class EscenaCosmica(EscenaBase):
    def __init__(self):
        pygame.font.init()
        self.fuente_dialogo = pygame.font.SysFont("arial", 22)
        self.timer = 0
        inventario = PlayerInventory()
        manager = EndingManager(inventario)
        self.titulo_final, self.texto = manager.evaluar_final("portal_morado")

        self.audio = SoundManager()
        self.audio.detener_todos() # Silenciamos el ambiente anterior
        self.audio.ajustar_volumen('final', 0.5) # Ajusta este valor de 0.0 a 1.0 según lo fuerte que sea el mp3
        self.audio.reproducir('final')

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Permitir terminar el juego presionando cualquier tecla tras una leve pausa
            if evento.type == pygame.KEYDOWN and self.timer > 60:

                pygame.quit()
                sys.exit()

    def actualizar(self):
        self.timer += 1

    def render(self, pantalla):
        pantalla.fill((3, 3, 12))

        # CENTRO Y TIEMPO

        centro_x = config.ANCHO // 2
        centro_y = config.ALTO // 2 - 90

        tiempo = pygame.time.get_ticks() / 1000.0

        # Pulsación lenta y orgánica
        pulso = (math.sin(tiempo * 2.0) + 1) / 2

        # AURA CÓSMICA

        aura = pygame.Surface(
            (config.ANCHO, config.ALTO),
            pygame.SRCALPHA
        )

        radio_base = 280 + int(pulso * 35)

        # Grandes ondas alrededor de la entidad
        for i in range(8):
            radio = radio_base - i * 28

            alpha = max(8, 45 - i * 4)

            pygame.draw.circle(
                aura,
                (105, 0, 170, alpha),
                (centro_x, centro_y),
                radio,
                5
            )

        # Segunda capa de distorsión
        for i in range(4):
            radio = 180 + i * 35 + int(pulso * 15)

            pygame.draw.circle(
                aura,
                (170, 20, 220, 35),
                (centro_x, centro_y),
                radio,
                2
            )

        pantalla.blit(aura, (0, 0))

        # SUPERFICIE DE LA ENTIDAD

        tam = 700

        entidad = pygame.Surface(
            (tam, tam),
            pygame.SRCALPHA
        )

        cx = tam // 2
        cy = tam // 2 - 10

        # COLORES

        TENTACULO_OSCURO = (30, 8, 43, 245)
        TENTACULO = (52, 12, 68, 250)
        TENTACULO_LUZ = (78, 18, 92, 240)

        MASA = (42, 10, 57, 250)
        MASA_LUZ = (63, 15, 77, 245)
        MASA_OSCURA = (24, 6, 33, 250)

        OJO = (225, 218, 175)
        IRIS = (115, 15, 145)
        PUPILA = (5, 2, 8)

        # TENTÁCULOS TRASEROS

        # Cada tentáculo tiene varios segmentos para que no parezca
        # una simple línea.

        tentaculos = [

            # Arriba izquierda
            [
                (cx - 70, cy - 100),
                (cx - 180, cy - 180),
                (cx - 270, cy - 230),
                (cx - 330, cy - 300)
            ],

            # Arriba derecha
            [
                (cx + 70, cy - 100),
                (cx + 180, cy - 185),
                (cx + 275, cy - 220),
                (cx + 335, cy - 285)
            ],

            # Izquierda superior
            [
                (cx - 100, cy - 45),
                (cx - 220, cy - 75),
                (cx - 315, cy - 45),
                (cx - 350, cy - 105)
            ],

            # Derecha superior
            [
                (cx + 100, cy - 45),
                (cx + 220, cy - 70),
                (cx + 315, cy - 40),
                (cx + 350, cy - 100)
            ],

            # Izquierda
            [
                (cx - 110, cy),
                (cx - 225, cy + 20),
                (cx - 320, cy + 80),
                (cx - 350, cy + 150)
            ],

            # Derecha
            [
                (cx + 110, cy),
                (cx + 225, cy + 25),
                (cx + 320, cy + 85),
                (cx + 350, cy + 155)
            ],

            # Abajo izquierda
            [
                (cx - 80, cy + 90),
                (cx - 170, cy + 170),
                (cx - 240, cy + 260),
                (cx - 300, cy + 315)
            ],

            # Abajo derecha
            [
                (cx + 80, cy + 90),
                (cx + 175, cy + 170),
                (cx + 245, cy + 260),
                (cx + 305, cy + 315)
            ],

            # Tentáculo inferior central izquierdo
            [
                (cx - 40, cy + 100),
                (cx - 75, cy + 210),
                (cx - 100, cy + 290),
                (cx - 70, cy + 345)
            ],

            # Tentáculo inferior central derecho
            [
                (cx + 40, cy + 100),
                (cx + 75, cy + 210),
                (cx + 105, cy + 290),
                (cx + 75, cy + 345)
            ]
        ]

        # DIBUJAR TENTÁCULOS

        for i, puntos in enumerate(tentaculos):

            # Movimiento independiente de cada tentáculo
            desplazamiento = math.sin(
                tiempo * 1.5 + i * 0.7
            ) * 12

            puntos_animados = []

            for j, (x, y) in enumerate(puntos):

                # Los extremos se mueven más
                factor = j / len(puntos)

                x += desplazamiento * factor

                puntos_animados.append((x, y))

            # Tentáculo principal
            pygame.draw.lines(
                entidad,
                TENTACULO_OSCURO,
                False,
                puntos_animados,
                42
            )

            pygame.draw.lines(
                entidad,
                TENTACULO,
                False,
                puntos_animados,
                28
            )

            # Línea de luz interior
            pygame.draw.lines(
                entidad,
                TENTACULO_LUZ,
                False,
                puntos_animados,
                7
            )

        # PEQUEÑOS TENTÁCULOS SECUNDARIOS

        secundarios = [

            (-250, -140),
            (-290, 10),
            (-240, 180),

            (250, -140),
            (290, 20),
            (240, 190),

            (-140, 280),
            (140, 280)
        ]

        for i, (dx, dy) in enumerate(secundarios):

            x1 = cx + dx * 0.55
            y1 = cy + dy * 0.55

            x2 = cx + dx
            y2 = cy + dy

            curva = math.sin(tiempo * 2 + i) * 15

            pygame.draw.line(
                entidad,
                TENTACULO_OSCURO,
                (x1, y1),
                (x2 + curva, y2),
                18
            )

        # MASA CENTRAL

        # Masa principal
        pygame.draw.circle(
            entidad,
            MASA_OSCURA,
            (cx, cy),
            170 + int(pulso * 8)
        )

        # Bultos orgánicos
        bultos = [
            (-95, -70, 90),
            (90, -75, 100),
            (-110, 40, 80),
            (105, 45, 95),
            (-55, 105, 85),
            (70, 110, 90)
        ]

        for i, (dx, dy, radio) in enumerate(bultos):

            movimiento = math.sin(
                tiempo * 1.5 + i
            ) * 4

            pygame.draw.circle(
                entidad,
                MASA,
                (
                    int(cx + dx + movimiento),
                    int(cy + dy)
                ),
                radio
            )

        # PROTUBERANCIAS

        for i in range(12):

            angulo = tiempo * 0.2 + i * 0.52

            radio = 160 + math.sin(
                tiempo * 1.5 + i
            ) * 15

            x = cx + math.cos(angulo) * radio
            y = cy + math.sin(angulo) * radio

            pygame.draw.circle(
                entidad,
                TENTACULO_LUZ,
                (int(x), int(y)),
                18
            )

        # OJO CENTRAL

        ojo_pulso = 1 + pulso * 0.12

        ancho_ojo = int(150 * ojo_pulso)
        alto_ojo = int(95 * ojo_pulso)

        # Aura del ojo
        pygame.draw.circle(
            entidad,
            (190, 30, 220, 70),
            (cx, cy),
            105 + int(pulso * 15)
        )

        # Cuenca
        pygame.draw.ellipse(
            entidad,
            (8, 3, 10, 255),
            (
                cx - ancho_ojo // 2 - 12,
                cy - alto_ojo // 2 - 12,
                ancho_ojo + 24,
                alto_ojo + 24
            )
        )

        # Globo ocular
        pygame.draw.ellipse(
            entidad,
            OJO,
            (
                cx - ancho_ojo // 2,
                cy - alto_ojo // 2,
                ancho_ojo,
                alto_ojo
            )
        )

        # Iris
        iris_radio = int(42 + pulso * 5)

        pygame.draw.circle(
            entidad,
            IRIS,
            (cx, cy),
            iris_radio
        )

        # Pupila vertical
        pygame.draw.ellipse(
            entidad,
            PUPILA,
            (
                cx - 11,
                cy - 40,
                22,
                80
            )
        )

        # Reflejo
        pygame.draw.circle(
            entidad,
            (255, 255, 255),
            (
                cx - 25,
                cy - 18
            ),
            9
        )

        # ANILLOS ALREDEDOR DEL OJO

        for i in range(4):

            radio = 110 + i * 20 + int(pulso * 10)

            pygame.draw.arc(
                entidad,
                (160, 35, 190, 100),
                (
                    cx - radio,
                    cy - radio // 2,
                    radio * 2,
                    radio
                ),
                math.radians(195),
                math.radians(345),
                3
            )

        # PARTÍCULAS

        for i in range(25):

            angulo = tiempo * 0.15 + i * 0.7

            radio = 210 + (i % 5) * 30

            x = cx + math.cos(angulo) * radio
            y = cy + math.sin(angulo) * radio

            pygame.draw.circle(
                entidad,
                (170, 50, 220, 130),
                (int(x), int(y)),
                3 + (i % 3)
            )

        # COLOCAR ENTIDAD EN PANTALLA

        pantalla.blit(
            entidad,
            (
                centro_x - cx,
                centro_y - cy
            )
        )

        # CAJA DE DIÁLOGO

        margen = 20
        alto_caja = 120

        rect_caja = (
            margen,
            config.ALTO - alto_caja - margen,
            config.ANCHO - 2 * margen,
            alto_caja
        )

        s_caja = pygame.Surface(
            (rect_caja[2], rect_caja[3]),
            pygame.SRCALPHA
        )

        s_caja.fill(
            (10, 10, 30, 220)
        )

        pantalla.blit(
            s_caja,
            (rect_caja[0], rect_caja[1])
        )

        pygame.draw.rect(
            pantalla,
            (255, 255, 255),
            rect_caja,
            2
        )

        texto_render = self.fuente_dialogo.render(
            self.texto,
            True,
            (200, 200, 255)
        )

        pantalla.blit(
            texto_render,
            (
                rect_caja[0] + 25,
                rect_caja[1] + 25
            )
        )

        if self.timer > 60:

            instruccion = self.fuente_dialogo.render(
                "Presiona cualquier tecla para terminar...",
                True,
                (150, 150, 150)
            )

            pantalla.blit(
                instruccion,
                (
                    rect_caja[0] + rect_caja[2] - 420,
                    rect_caja[1] + rect_caja[3] - 35
                )
            )