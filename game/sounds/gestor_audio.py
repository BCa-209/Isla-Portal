import pygame

class AudioManager:
    """Wrapper para la reproducción de sonidos.""" #[cite: 2]
    def __init__(self):
        pygame.mixer.init()
        self.pista_actual = None
        
    def reproducir_musica_ambiental(self, archivo):
        """Controlará cambios en música ambiental al entrar al monumento o en batallas.""" #[cite: 2]
        try:
            pygame.mixer.music.load(f"assets/sounds/{archivo}") #[cite: 2]
            pygame.mixer.music.play(-1) # Loop infinito
            self.pista_actual = archivo
        except pygame.error:
            print(f"No se pudo cargar el audio: {archivo}")
            
    def reproducir_efecto(self, archivo_efecto):
        """Ejecuta los efectos de combate o recolección.""" #[cite: 2]
        try:
            sonido = pygame.mixer.Sound(f"assets/sounds/{archivo_efecto}") #[cite: 2]
            sonido.play()
        except pygame.error:
            pass