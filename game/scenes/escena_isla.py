import pygame
import sys
from core.escena_base import EscenaBase
from game.entities.jugador import Protagonista
from game.entities.enemigos import EnemigoSlime, VistaSectario, VistaVagabundo
from game.entities.objetos import Llave, InteractableItem
from game.logic.motor_juego import GameManager
from game.graphics.terreno import TileManager
import config

class EscenaIsla(EscenaBase):
    def __init__(self):
        self.motor = GameManager()

        # graficoss
        self.tam_celda = config.TAM_CELDA
        self.e = config.ESCALA_BASE
        self.gestor_terreno = TileManager()

        pygame.font.init()
        self.fuente_ui = pygame.font.SysFont("arial", 48, bold=True)
        self.fuente_dialogo = pygame.font.SysFont("arial", 22)
        
        self.jugador_grafico = Protagonista(
            config.POS_INI[0], config.POS_INI[1], self.e, self.tam_celda
        )
        self.temporizador_enemigos = 0
        self.temporizador_carga = 0
        self.cooldown_movimiento = 0  # Controla la velocidad del movimiento continuo

        self.camera_x = 0
        self.camera_y = 0
        self.recalcular_escala()

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if self.motor.estado == "CARGANDO":
                if self.temporizador_carga >= 120 and evento.type == pygame.KEYDOWN:
                    self.motor.cargar_nivel(self.motor.nivel_objetivo)
                    self.temporizador_carga = 0
                    
                    # Reposicionamos la cámara instantáneamente al cambiar de mapa
                    fila, col = self.motor.jugador_pos
                    self.jugador_grafico.x = col * self.tam_celda
                    self.jugador_grafico.y = fila * self.tam_celda
                    self.camera_x = self.jugador_grafico.x - (config.ANCHO // 2) + (self.tam_celda // 2)
                    self.camera_y = self.jugador_grafico.y - (config.ALTO // 2) + (self.tam_celda // 2)
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
            self.motor.evaluar_locura_espontanea()
            # --- 1. Lógica de Inputs y Cooldown ---
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
                    self.cooldown_movimiento = 10 

            # --- 2. Lógica del Motor de Enemigos ---
            self.temporizador_enemigos += 1
            if self.temporizador_enemigos >= 30:
                self.motor.actualizar_enemigos()
                self.temporizador_enemigos = 0

            # --- 3. ANIMACIÓN FLUIDA DEL JUGADOR (LERP) ---
            fila_logica, col_logica = self.motor.jugador_pos
            target_x = col_logica * self.tam_celda
            target_y = fila_logica * self.tam_celda
            
            velocidad_suavizado = 0.3 
            self.jugador_grafico.x += (target_x - self.jugador_grafico.x) * velocidad_suavizado
            self.jugador_grafico.y += (target_y - self.jugador_grafico.y) * velocidad_suavizado

            # --- 4. CÁMARA FLUIDA (Seguimiento) ---
            # El objetivo de la cámara es el centro visual del jugador menos la mitad de la pantalla
            target_cam_x = self.jugador_grafico.x - (config.ANCHO // 2) + (self.tam_celda // 2)
            target_cam_y = self.jugador_grafico.y - (config.ALTO // 2) + (self.tam_celda // 2)
            
            # Deslizamiento suave de la cámara
            self.camera_x += (target_cam_x - self.camera_x) * 0.1
            self.camera_y += (target_cam_y - self.camera_y) * 0.1

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
        # Fondo oscuro semitransparente
        overlay = pygame.Surface((config.ANCHO, config.ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210)) # Un poco más oscuro para que el texto resalte
        pantalla.blit(overlay, (0, 0))

        # Extraemos los textos (usamos getattr por seguridad con valores por defecto)
        titulo = getattr(self.motor, "titulo_derrota", "¡ELIMINADO!")
        texto = getattr(self.motor, "texto_derrota", "Has caído ante la oscuridad.")

        # 1. Renderizar el Título del Final (En rojo)
        render_titulo = self.fuente_ui.render(titulo, True, (255, 50, 50))
        rect_titulo = render_titulo.get_rect(center=(config.ANCHO // 2, config.ALTO // 2 - 60))
        pantalla.blit(render_titulo, rect_titulo)

        # 2. Renderizar la narrativa del final (En blanco/gris)
        render_texto = self.fuente_dialogo.render(texto, True, (200, 200, 200))
        rect_texto = render_texto.get_rect(center=(config.ANCHO // 2, config.ALTO // 2))
        pantalla.blit(render_texto, rect_texto)

        # 3. Instrucción para continuar (En amarillo)
        render_instruccion = self.fuente_dialogo.render("Presiona [R] para reiniciar el ciclo...", True, (255, 255, 0))
        rect_instruccion = render_instruccion.get_rect(center=(config.ANCHO // 2, config.ALTO // 2 + 80))
        pantalla.blit(render_instruccion, rect_instruccion)

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

        # Color base para el espacio "vacío" si la cámara enfoca fuera del mapa
        pantalla.fill((0, 0, 0)) 
        nivel = self.motor.nivel_actual
        
        # --- OPTIMIZACIÓN (Culling) ---
        # Calculamos qué filas y columnas caen dentro del área visible de la cámara
        col_inicio = max(0, int(self.camera_x // self.tam_celda))
        col_fin = min(self.motor.columnas, int((self.camera_x + config.ANCHO) // self.tam_celda) + 2)
        fila_inicio = max(0, int(self.camera_y // self.tam_celda))
        fila_fin = min(self.motor.filas, int((self.camera_y + config.ALTO) // self.tam_celda) + 2)

        # 1. Dibujamos el terreno base y objetos estáticos (Solo los visibles)
        for fila in range(fila_inicio, fila_fin):
            for col in range(col_inicio, col_fin):
                mundo_x = col * self.tam_celda
                mundo_y = fila * self.tam_celda
                
                # Coordenada en pantalla = Coordenada del mundo - Offset de la Cámara
                pantalla_x = mundo_x - self.camera_x
                pantalla_y = mundo_y - self.camera_y
                
                tipo_casilla = self.motor.mapa[fila][col]
                
                # El gestor dibuja usando la posición ajustada de pantalla
                self.gestor_terreno.dibujar_casilla(pantalla, tipo_casilla, pantalla_x, pantalla_y, self.tam_celda, nivel)

                if tipo_casilla in [self.motor.LLAVE, self.motor.CRISTAL, self.motor.MONEDA, self.motor.POCION]:
                    if tipo_casilla == self.motor.LLAVE:
                        tipo_llave = "jungla" if nivel == 1 else "desierto"
                        obj_grafico = Llave(pantalla_x, pantalla_y, self.e, tipo=tipo_llave)
                    else:
                        if tipo_casilla == self.motor.CRISTAL:
                            tipo_obj = "cristal"
                        elif tipo_casilla == self.motor.MONEDA:
                            tipo_obj = "moneda"
                        elif tipo_casilla == self.motor.POCION:
                            tipo_obj = "pocion"
                        obj_grafico = InteractableItem(pantalla_x, pantalla_y, self.e, tipo=tipo_obj)
                    obj_grafico.render(pantalla)
                    
                elif tipo_casilla == self.motor.COFRE:
                    pygame.draw.rect(pantalla, (139, 69, 19), (pantalla_x + 5, pantalla_y + 10, self.tam_celda - 10, self.tam_celda - 20))
                    pygame.draw.rect(pantalla, (255, 215, 0), (pantalla_x + self.tam_celda//2 - 5, pantalla_y + self.tam_celda//2, 10, 5))
                elif tipo_casilla == self.motor.PORTAL_MORADO:
                    pygame.draw.circle(pantalla, (128, 0, 128), (pantalla_x + self.tam_celda//2, pantalla_y + self.tam_celda//2), self.tam_celda//2 - 5)
                elif tipo_casilla == self.motor.CADAVER:
                    pygame.draw.circle(pantalla, (150, 0, 0), (pantalla_x + self.tam_celda//2, pantalla_y + self.tam_celda//2), self.tam_celda//2 - 5) 
                    pygame.draw.rect(pantalla, (200, 200, 200), (pantalla_x + self.tam_celda//2 - 10, pantalla_y + self.tam_celda//2 - 15, 20, 30)) 

        # 2. Renderizado Fluido de Enemigos
        for e_data in self.motor.enemigos:
            target_x = e_data["col"] * self.tam_celda
            target_y = e_data["fila"] * self.tam_celda
            
            if "x_visual" not in e_data:
                e_data["x_visual"] = target_x
                e_data["y_visual"] = target_y
                
            e_data["x_visual"] += (target_x - e_data["x_visual"]) * 0.2
            e_data["y_visual"] += (target_y - e_data["y_visual"]) * 0.2
            
            x_render = e_data["x_visual"] - self.camera_x
            y_render = e_data["y_visual"] - self.camera_y
            
            # Instanciar el gráfico correcto según el tipo
            if e_data["tipo"] == "vagabundo":
                enemigo_grafico = VistaVagabundo(0, 0, self.e, self.tam_celda)
            elif e_data["tipo"] == "estatico": # Opcional: si tienes sectarios en el mapa
                enemigo_grafico = VistaSectario(0, 0, self.e, self.tam_celda)
            else:
                enemigo_grafico = EnemigoSlime(0, 0, self.e, self.tam_celda)
                
            enemigo_grafico.setX(x_render)
            enemigo_grafico.setY(y_render)
            enemigo_grafico.render(pantalla)
                
        # 3. Renderizado del Jugador
        # Guardamos la posición absoluta del mundo
        temp_x = self.jugador_grafico.x
        temp_y = self.jugador_grafico.y
        
        # Le aplicamos temporalmente la posición de cámara para dibujarlo centrado
        self.jugador_grafico.x -= self.camera_x
        self.jugador_grafico.y -= self.camera_y
        self.jugador_grafico.render(pantalla)
        
        # Restauramos la matemática original
        self.jugador_grafico.x = temp_x
        self.jugador_grafico.y = temp_y

        # 4. Capas UI (Estáticas frente a la cámara)
        if self.motor.estado == "DERROTA":
            self.dibujar_overlay_derrota(pantalla)
        elif self.motor.estado == "DIALOGO":
            self.dibujar_dialogo(pantalla)