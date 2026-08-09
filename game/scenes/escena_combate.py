import pygame
import sys
from core.escena_base import EscenaBase
from game.logic.motor_combate import CombatManager
from game.logic.ia_enemigos import IAEnemigo
from game.entities.jugador import Protagonista
from game.entities.enemigos import EnemigoSlime, VistaSectario
import config

class EscenaCombate(EscenaBase):
    def __init__(self, motor_principal):
        self.e = config.ESCALA_BASE
        self.tam_celda = config.TAM_CELDA
        
        self.motor_principal = motor_principal
        self.inventario = motor_principal.inventario
        self.enemigo_data = motor_principal.enemigo_en_combate
        
        self.motor_combate = CombatManager(self.inventario)
        
        es_jefe = (self.enemigo_data.get("tipo") == "jefe")
        self.ia_enemigo = IAEnemigo(es_jefe=es_jefe)
        
        self.jugador_grafico = Protagonista(0, 0, self.e, self.tam_celda)
        self.jugador_grafico.setXY(150, 250)
        
        if es_jefe:
            self.enemigo_grafico = VistaSectario(0, 0, self.e, self.tam_celda)
        else:
            self.enemigo_grafico = EnemigoSlime(0, 0, self.e, self.tam_celda)
        self.enemigo_grafico.setXY(600, 250)
        
        pygame.font.init()
        self.fuente_ui = pygame.font.SysFont("arial", 24)
        self.fuente_titulo = pygame.font.SysFont("arial", 32, bold=True)
        
        self.opciones = ["ataque_rapido", "ataque_pesado", "pocion", "observar"]
        self.indice_seleccion = 0
        
        self.mensaje_resolucion = ""
        self.timer_resolucion = 0

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if self.motor_combate.estado == "SELECCION":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        self.indice_seleccion = (self.indice_seleccion - 1) % len(self.opciones)
                    elif evento.key == pygame.K_DOWN:
                        self.indice_seleccion = (self.indice_seleccion + 1) % len(self.opciones)
                    elif evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        accion_elegida = self.opciones[self.indice_seleccion]
                        
                        # Bloquear el uso de poción si no quedan en el inventario
                        if accion_elegida == "pocion" and self.inventario.pociones <= 0:
                            self.mensaje_resolucion = "¡No tienes pociones en el inventario!"
                            self.motor_combate.estado = "RESOLUCION"
                            self.timer_resolucion = 90
                            return
                        
                        accion_enemiga = self.ia_enemigo.elegir_accion()
                        self.motor_combate.fijar_acciones(accion_elegida, accion_enemiga)

    def actualizar(self):
        if self.motor_combate.estado == "EJECUCION":
            resultado = self.motor_combate.actualizar_timers()
            
            if resultado:
                self.aplicar_resolucion(resultado)
                self.motor_combate.estado = "RESOLUCION"
                self.timer_resolucion = 120 
                
        elif self.motor_combate.estado == "RESOLUCION":
            self.timer_resolucion -= 1
            if self.timer_resolucion <= 0:
                if self.ia_enemigo.hp_actual <= 0:
                    self.resolver_victoria()
                elif self.inventario.salud_actual <= 0:
                    self.resolver_derrota()
                else:
                    self.motor_combate.resetear_turno()

    def aplicar_resolucion(self, ganador):
        accion_j = self.motor_combate.accion_jugador
        accion_e = self.motor_combate.accion_enemigo
        
        if ganador == "jugador_primero":
            if accion_j["tipo"] == "ataque":
                self.ia_enemigo.recibir_dano(accion_j.get("dano", 0))
                self.mensaje_resolucion = f"¡Golpeas primero! El enemigo recibe {accion_j.get('dano', 0)} de daño."
            elif accion_j["tipo"] == "curacion":
                self.inventario.pociones -= 1
                curacion = accion_j.get("curacion", 0)
                self.inventario.salud_actual = min(self.inventario.salud_maxima, self.inventario.salud_actual + curacion)
                self.mensaje_resolucion = f"Te curas {curacion} HP rápidamente."
            elif accion_j["tipo"] == "utilidad":
                self.mensaje_resolucion = "Observas al enemigo con atención, despejando tu mente."
                self.inventario.cordura = min(100, self.inventario.cordura + 15)
                
        elif ganador == "enemigo_primero":
            if accion_e["tipo"] == "ataque":
                self.inventario.salud_actual -= accion_e.get("dano", 0)
                self.inventario.cordura -= 10
                self.mensaje_resolucion = f"¡El enemigo es más rápido! Recibes {accion_e.get('dano', 0)} de daño."
                
        elif ganador == "empate":
            if accion_j["tipo"] == "ataque":
                self.ia_enemigo.recibir_dano(accion_j.get("dano", 0))
            elif accion_j["tipo"] == "curacion":
                self.inventario.pociones -= 1
                curacion = accion_j.get("curacion", 0)
                self.inventario.salud_actual = min(self.inventario.salud_maxima, self.inventario.salud_actual + curacion)
                
            if accion_e["tipo"] == "ataque":
                self.inventario.salud_actual -= accion_e.get("dano", 0)
            self.mensaje_resolucion = "¡Ambas acciones ocurren al mismo tiempo!"

    def resolver_victoria(self):
        self.inventario.cordura = min(100, self.inventario.cordura + 25)
        
        if self.enemigo_data.get("tipo") == "jefe":
            self.motor_principal.mapa[self.enemigo_data["fila"]][self.enemigo_data["col"]] = self.motor_principal.TIERRA
            self.motor_principal.estado = "EN_CURSO"
            self.motor_principal.enemigo_en_combate = None
            
            self.inventario.llave_cofre = True # Entregar premio
            self.motor_principal.iniciar_dialogo("¡Has derrotado al Jefe! Obtienes la LLAVE DEL COFRE.")
        else:
            if self.enemigo_data in self.motor_principal.enemigos:
                self.motor_principal.enemigos.remove(self.enemigo_data)
            self.motor_principal.estado = "EN_CURSO"
            self.motor_principal.enemigo_en_combate = None

    def resolver_derrota(self):
        self.motor_principal.estado = "DERROTA"
        self.motor_principal.enemigo_en_combate = None

    def render(self, pantalla):
        pantalla.fill((20, 20, 25))
        
        pygame.draw.rect(pantalla, (40, 40, 50), (100, 350, 600, 200), border_radius=10)
        pygame.draw.rect(pantalla, (100, 100, 120), (100, 350, 600, 200), 2, border_radius=10)
        
        self.jugador_grafico.render(pantalla)
        self.enemigo_grafico.render(pantalla)
        
        texto_hp_jugador = self.fuente_ui.render(f"HP: {self.inventario.salud_actual}/{self.inventario.salud_maxima}", True, (50, 200, 50))
        texto_cordura = self.fuente_ui.render(f"Cordura: {self.inventario.cordura}%", True, (150, 150, 255))
        pantalla.blit(texto_hp_jugador, (120, 50))
        pantalla.blit(texto_cordura, (120, 80))
        
        nombre_enemigo = "Jefe Sectario" if self.enemigo_data.get("tipo") == "jefe" else "Bestia Oscura"
        texto_hp_enemigo = self.fuente_ui.render(f"{nombre_enemigo}: {self.ia_enemigo.hp_actual}/{self.ia_enemigo.hp_maximo}", True, (255, 50, 50))
        pantalla.blit(texto_hp_enemigo, (500, 50))
        
        if self.motor_combate.estado == "SELECCION":
            titulo_menu = self.fuente_titulo.render("ELIGE TU ACCIÓN", True, (255, 215, 0))
            pantalla.blit(titulo_menu, (120, 370))
            
            y_offset = 420
            for i, opcion in enumerate(self.opciones):
                color = (255, 255, 255) if i == self.indice_seleccion else (100, 100, 100)
                prefijo = "> " if i == self.indice_seleccion else "  "
                
                # Renderizado dinámico del nombre de la opción para mostrar el contador de pociones
                nombre_opcion = opcion.replace('_', ' ').upper()
                if opcion == "pocion":
                    nombre_opcion += f" (x{self.inventario.pociones})"
                    
                texto_opcion = self.fuente_ui.render(f"{prefijo}{nombre_opcion}", True, color)
                pantalla.blit(texto_opcion, (120, y_offset))
                y_offset += 30
                
        elif self.motor_combate.estado == "EJECUCION":
            info_enemigo = self.motor_combate.obtener_info_enemigo()
            texto_intencion = "???" if info_enemigo == "???" else info_enemigo["tipo"].upper()
            
            lbl_prep_j = self.fuente_ui.render(f"Preparando: {self.opciones[self.indice_seleccion].replace('_', ' ').upper()}", True, (255, 255, 255))
            lbl_prep_e = self.fuente_ui.render(f"Enemigo prepara: {texto_intencion}", True, (255, 100, 100))
            pantalla.blit(lbl_prep_j, (120, 380))
            pantalla.blit(lbl_prep_e, (450, 380))
            
            ancho_barra = 250
            
            progreso_j = min(1.0, self.motor_combate.timer_jugador / self.motor_combate.accion_jugador["prep"])
            pygame.draw.rect(pantalla, (100, 100, 100), (120, 420, ancho_barra, 20))
            pygame.draw.rect(pantalla, (0, 200, 255), (120, 420, int(ancho_barra * progreso_j), 20))
            
            progreso_e = min(1.0, self.motor_combate.timer_enemigo / self.motor_combate.accion_enemigo["prep"])
            pygame.draw.rect(pantalla, (100, 100, 100), (450, 420, ancho_barra, 20))
            pygame.draw.rect(pantalla, (255, 50, 50), (450, 420, int(ancho_barra * progreso_e), 20))
            
        elif self.motor_combate.estado == "RESOLUCION":
            texto_res = self.fuente_ui.render(self.mensaje_resolucion, True, (255, 255, 0))
            rect_res = texto_res.get_rect(center=(config.ANCHO // 2, 450))
            pantalla.blit(texto_res, rect_res)