import pygame
import sys
from core.escena_base import EscenaBase
from game.entities.jugador import Protagonista
from game.entities.enemigos import EnemigoSlime, VistaSectario
from game.entities.objetos import Llave, InteractableItem
from game.logic.motor_juego import GameManager
import config

class EscenaIsla(EscenaBase):
    def __init__(self):
        self.motor = GameManager()
        self.e = config.ESCALA_BASE
        self.tam_celda = config.TAM_CELDA
        
        pygame.font.init()
        self.fuente_ui = pygame.font.SysFont("arial", 48, bold=True)
        self.fuente_dialogo = pygame.font.SysFont("arial", 22)
        
        self.jugador_grafico = Protagonista(
            config.POS_INI[0], config.POS_INI[1], self.e, self.tam_celda
        )
        self.temporizador_enemigos = 0
        self.temporizador_carga = 0
        self.cooldown_movimiento = 0  # Controla la velocidad del movimiento continuo
        #self.recalcular_escala()  # Inicializa la escala basada en la resolución actual

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if self.motor.estado == "CARGANDO":
                # Omitir pantalla de carga al presionar cualquier tecla tras 2 segundos (120 frames)
                if self.temporizador_carga >= 120 and evento.type == pygame.KEYDOWN:
                    self.motor.cargar_nivel(self.motor.nivel_objetivo)
                    self.temporizador_carga = 0
                return
                
            if self.motor.estado == "DERROTA":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    self.motor.reiniciar_tras_derrota()
                return 

            if self.motor.estado == "DIALOGO":
                if evento.type == pygame.KEYDOWN and evento.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    self.motor.cerrar_dialogo()
                return 

    def actualizar(self):
        if self.motor.estado == "CARGANDO":
            self.temporizador_carga += 1
            return

        if self.motor.estado == "EN_CURSO":
            # 1. Movimiento Continuo del Jugador
            if self.cooldown_movimiento > 0:
                self.cooldown_movimiento -= 1
                
            if self.cooldown_movimiento == 0:
                teclas = pygame.key.get_pressed()
                movido = False
                
                if teclas[pygame.K_UP]:
                    self.motor.intentar_mover_jugador(-1, 0)
                    movido = True
                elif teclas[pygame.K_DOWN]:
                    self.motor.intentar_mover_jugador(1, 0)
                    movido = True
                elif teclas[pygame.K_LEFT]:
                    self.motor.intentar_mover_jugador(0, -1)
                    movido = True
                elif teclas[pygame.K_RIGHT]:
                    self.motor.intentar_mover_jugador(0, 1)
                    movido = True
                    
                if movido:
                    # Pausa el movimiento por 10 frames (1/6 de segundo) para un control suave
                    self.cooldown_movimiento = 10 

            # 2. Movimiento de los enemigos
            self.temporizador_enemigos += 1
            if self.temporizador_enemigos >= 30:
                self.motor.actualizar_enemigos()
                self.temporizador_enemigos = 0

            # 3. Sincronización gráfica
            fila_logica, col_logica = self.motor.jugador_pos
            self.jugador_grafico.setFila(fila_logica)
            self.jugador_grafico.setColumna(col_logica)
            self.jugador_grafico.actualizar_coordenadas()

    def dibujar_pantalla_carga(self, pantalla):
        pantalla.fill((0, 0, 0))
        try:
            ruta_imagen = f"assets/images/carga_nivel_{self.motor.nivel_objetivo}.png"
            imagen = pygame.image.load(ruta_imagen)
            imagen = pygame.transform.scale(imagen, (config.ANCHO, config.ALTO))
            pantalla.blit(imagen, (0, 0))
        except FileNotFoundError:
            # Fallback si no encuentra la imagen
            texto = self.fuente_ui.render(f"Viajando al Nivel {self.motor.nivel_objetivo}...", True, (255, 255, 255))
            rect = texto.get_rect(center=(config.ANCHO // 2, config.ALTO // 2))
            pantalla.blit(texto, rect)

        # Panel de Historia a la derecha
        ancho_caja = 300
        rect_caja = (config.ANCHO - ancho_caja - 20, 20, ancho_caja, config.ALTO - 40)
        s_caja = pygame.Surface((rect_caja[2], rect_caja[3]), pygame.SRCALPHA)
        s_caja.fill((20, 20, 25, 230))
        pantalla.blit(s_caja, (rect_caja[0], rect_caja[1]))
        pygame.draw.rect(pantalla, (200, 200, 200), rect_caja, 2)
        
        # Renderizado multilínea del lore
        lineas = self.motor.texto_lore.split('\n')
        y_offset = 30
        for linea in lineas:
            texto_render = self.fuente_dialogo.render(linea, True, (255, 255, 255))
            pantalla.blit(texto_render, (rect_caja[0] + 20, rect_caja[1] + y_offset))
            y_offset += 32
            
        # Indicador para omitir tras 2 segundos
        if self.temporizador_carga >= 120:
            texto_skip = self.fuente_dialogo.render("Presiona cualquier tecla...", True, (255, 255, 0))
            pantalla.blit(texto_skip, (rect_caja[0] + 20, rect_caja[1] + rect_caja[3] - 40))

    def dibujar_overlay_derrota(self, pantalla):
        overlay = pygame.Surface((config.ANCHO, config.ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        pantalla.blit(overlay, (0, 0))

        texto = self.fuente_ui.render("¡ELIMINADO! - Reiniciar [R]", True, (255, 255, 255))
        sombra = self.fuente_ui.render("¡ELIMINADO! - Reiniciar [R]", True, (255, 0, 0))
        
        rect = texto.get_rect(center=(config.ANCHO // 2, config.ALTO // 2))
        rect_sombra = sombra.get_rect(center=(config.ANCHO // 2 + 2, config.ALTO // 2 + 2))
        
        pantalla.blit(sombra, rect_sombra) 
        pantalla.blit(texto, rect)

    def dibujar_dialogo(self, pantalla):
        margen = 20
        alto_caja = 120
        rect_caja = (margen, config.ALTO - alto_caja - margen, config.ANCHO - 2 * margen, alto_caja)
        
        s_caja = pygame.Surface((rect_caja[2], rect_caja[3]), pygame.SRCALPHA)
        s_caja.fill((10, 10, 30, 220))
        pantalla.blit(s_caja, (rect_caja[0], rect_caja[1]))
        pygame.draw.rect(pantalla, (255, 255, 255), rect_caja, 2) 
        
        texto_render = self.fuente_dialogo.render(self.motor.texto_dialogo, True, (255, 255, 255))
        pantalla.blit(texto_render, (rect_caja[0] + 25, rect_caja[1] + 25))
        
        instruccion = self.fuente_dialogo.render("Presiona ESPACIO o ENTER para continuar...", True, (150, 150, 150))
        pantalla.blit(instruccion, (rect_caja[0] + rect_caja[2] - 420, rect_caja[1] + rect_caja[3] - 35))

    def recalcular_escala(self):
        """Calcula dinámicamente el tamaño de la celda para llenar la pantalla."""
        # Calculamos cuánto espacio tiene cada celda en base a la resolución actual
        celda_x = config.ANCHO // self.motor.columnas
        celda_y = config.ALTO // self.motor.filas
        
        # Tomamos el valor mínimo para que las celdas sigan siendo cuadradas perfectas
        self.tam_celda = min(celda_x, celda_y)
        self.e = max(1, self.tam_celda // 6)
        
        # Actualizamos la escala de las entidades visuales
        self.jugador_grafico.setEscala(self.e)
        # Nota: Los enemigos y objetos se escalarán solos al instanciarse en el render()

    def render(self, pantalla):
        if self.motor.estado == "CARGANDO":
            self.dibujar_pantalla_carga(pantalla)
            return

        pantalla.fill((0, 0, 0))
        nivel = self.motor.nivel_actual
        
        colores = {
            self.motor.TIERRA: (80, 160, 80) if nivel == 1 else (210, 180, 140) if nivel == 2 else (90, 90, 100),
            self.motor.AGUA: (28, 107, 160) if nivel == 1 else (60, 200, 220) if nivel == 2 else (20, 20, 25),
            self.motor.ROCA: (100, 100, 100) if nivel == 1 else (180, 150, 110) if nivel == 2 else (60, 60, 70),
            
            self.motor.PORTAL: (0, 150, 255),
            self.motor.PORTAL_AZUL: (255, 50, 50), 
            self.motor.CUEVA: (30, 30, 30), 
            self.motor.JEFE: (150, 0, 0)
        }
        
        for fila in range(self.motor.filas):
            for col in range(self.motor.columnas):
                x = col * self.tam_celda
                y = fila * self.tam_celda
                tipo_casilla = self.motor.mapa[fila][col]
                
                if tipo_casilla in [self.motor.LLAVE, self.motor.CRISTAL, self.motor.MONEDA, self.motor.POCION]:
                    pygame.draw.rect(pantalla, colores[self.motor.TIERRA], (x, y, self.tam_celda, self.tam_celda))
                    pygame.draw.rect(pantalla, (0, 0, 0), (x, y, self.tam_celda, self.tam_celda), 1)
                    
                    if tipo_casilla == self.motor.LLAVE:
                        tipo_llave = "jungla" if nivel == 1 else "desierto"
                        obj_grafico = Llave(x, y, self.e, tipo=tipo_llave)
                    else:
                        if tipo_casilla == self.motor.CRISTAL:
                            tipo_obj = "cristal"
                        elif tipo_casilla == self.motor.MONEDA:
                            tipo_obj = "moneda"
                        elif tipo_casilla == self.motor.POCION:
                            tipo_obj = "pocion"
                            
                        obj_grafico = InteractableItem(x, y, self.e, tipo=tipo_obj)
                        
                    obj_grafico.render(pantalla)
                    
                else:
                    color = colores.get(tipo_casilla, (0,0,0))
                    pygame.draw.rect(pantalla, color, (x, y, self.tam_celda, self.tam_celda))
                    pygame.draw.rect(pantalla, (0, 0, 0), (x, y, self.tam_celda, self.tam_celda), 1)
                    
                    if tipo_casilla == self.motor.CUEVA:
                        pygame.draw.circle(pantalla, (10, 10, 10), (x + self.tam_celda//2, y + self.tam_celda//2), self.tam_celda//3)
                    elif tipo_casilla == self.motor.COFRE:
                        pygame.draw.rect(pantalla, (139, 69, 19), (x + 5, y + 10, self.tam_celda - 10, self.tam_celda - 20))
                        pygame.draw.rect(pantalla, (255, 215, 0), (x + self.tam_celda//2 - 5, y + self.tam_celda//2, 10, 5))
                    elif tipo_casilla == self.motor.PORTAL_MORADO:
                        pygame.draw.circle(pantalla, (128, 0, 128), (x + self.tam_celda//2, y + self.tam_celda//2), self.tam_celda//2 - 5)
                    elif tipo_casilla == self.motor.CADAVER:
                        pygame.draw.circle(pantalla, (150, 0, 0), (x + self.tam_celda//2, y + self.tam_celda//2), self.tam_celda//2 - 5) 
                        pygame.draw.rect(pantalla, (200, 200, 200), (x + self.tam_celda//2 - 10, y + self.tam_celda//2 - 15, 20, 30))
        
        for e_data in self.motor.enemigos:
            enemigo_grafico = VistaSectario(e_data["fila"], e_data["col"], self.e, self.tam_celda)
            enemigo_grafico.actualizar_coordenadas()
            enemigo_grafico.render(pantalla)
                
        self.jugador_grafico.render(pantalla)

        if self.motor.estado == "DERROTA":
            self.dibujar_overlay_derrota(pantalla)
        elif self.motor.estado == "DIALOGO":
            self.dibujar_dialogo(pantalla)