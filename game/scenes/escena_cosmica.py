import pygame
import sys
import json
import os
from core.escena_base import EscenaBase
from game.logic.finales_manager import EndingManager
from game.logic.inventario import PlayerInventory
import config

class EscenaCosmica(EscenaBase):
    def __init__(self):
        pygame.font.init()
        self.fuente_dialogo = pygame.font.SysFont("arial", 22)
        self.timer = 0
        inventario = PlayerInventory.inventario
        manager = EndingManager(inventario)
        self.titulo_final, self.texto = manager.evaluar_final("portal_morado")
        
        try:
            with open(os.path.join("data", "lore.json"), "r", encoding="utf-8") as archivo:
                data = json.load(archivo)
                self.texto = data.get("final_cosmico", "Te encuentras con la Entidad Cósmica...")
        except FileNotFoundError:
            self.texto = "Te encuentras con la Entidad Cósmica..."

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
        pantalla.fill((5, 5, 15)) # Fondo espacio oscuro
        
        # Geometría abstracta de la Entidad Cósmica
        centro_x = config.ANCHO // 2
        centro_y = config.ALTO // 2 - 50
        
        # Efecto de pulsación basado en el tiempo
        radio_pulso = 100 + (self.timer % 20)
        pygame.draw.circle(pantalla, (255, 255, 255), (centro_x, centro_y), radio_pulso, 1)
        pygame.draw.circle(pantalla, (148, 0, 211), (centro_x, centro_y), 40)
        
        # Caja de diálogo final (Estilo RPG)
        margen = 20
        alto_caja = 120
        rect_caja = (margen, config.ALTO - alto_caja - margen, config.ANCHO - 2 * margen, alto_caja)
        
        s_caja = pygame.Surface((rect_caja[2], rect_caja[3]), pygame.SRCALPHA)
        s_caja.fill((10, 10, 30, 220))
        pantalla.blit(s_caja, (rect_caja[0], rect_caja[1]))
        pygame.draw.rect(pantalla, (255, 255, 255), rect_caja, 2) 
        
        # Mostrar mensaje
        texto_render = self.fuente_dialogo.render(self.texto, True, (200, 200, 255))
        pantalla.blit(texto_render, (rect_caja[0] + 25, rect_caja[1] + 25))
        
        # Mostrar instrucción de cierre
        if self.timer > 60:
            instruccion = self.fuente_dialogo.render("Presiona cualquier tecla para terminar...", True, (150, 150, 150))
            pantalla.blit(instruccion, (rect_caja[0] + rect_caja[2] - 420, rect_caja[1] + rect_caja[3] - 35))
        self