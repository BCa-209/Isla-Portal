import pygame
import sys
import config
from game.scenes.escena_isla import EscenaIsla
from game.scenes.escena_combate import EscenaCombate
from game.scenes.escena_cosmica import EscenaCosmica
from game.scenes.escena_jefe import EscenaJefe  # <-- NUEVO IMPORT

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
    pygame.display.set_caption("Islas Portal")
    reloj = pygame.time.Clock()
    
    escena_exploracion = EscenaIsla()
    escena_actual = escena_exploracion
    
    while True:
        eventos = pygame.event.get()
        
        escena_actual.manejar_eventos(eventos)
        escena_actual.actualizar()
        escena_actual.render(pantalla)
        
        # Gestor de transiciones
        if isinstance(escena_actual, EscenaIsla):
            if escena_actual.motor.estado == "COMBATE":
                escena_actual = EscenaCombate(escena_actual.motor)
            elif escena_actual.motor.estado == "FINAL_COSMICO":
                escena_actual = EscenaCosmica() 
            elif escena_actual.motor.estado == "FIN":  
                # <-- AQUÍ CONECTAMOS LA ESCENA DE DECISIÓN CLÁSICA
                escena_actual = EscenaJefe(escena_actual.motor.inventario) 
                
        elif isinstance(escena_actual, EscenaCombate):
            if escena_actual.motor_principal.estado in ["EN_CURSO", "DERROTA", "DIALOGO"]:
                escena_actual = escena_exploracion
        
        pygame.display.flip()
        reloj.tick(config.FPS)

if __name__ == "__main__":
    main()