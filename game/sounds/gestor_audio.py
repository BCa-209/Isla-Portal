import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sonidos = {}
        self.cargar_sonidos()
    
    def cargar_sonidos(self):
        """Cargar sonidos desde archivos MP3/WAV"""
        base_path = "assets/sounds/"
        sonidos_config = {
            'templo': 'temple.mp3',
            'cueva': 'cave.mp3',
            'final': 'final_real.mp3'
        }
        for nombre, archivo in sonidos_config.items():
            ruta_completa = os.path.join(base_path, archivo)
            try:
                if os.path.exists(ruta_completa):
                    self.sonidos[nombre] = pygame.mixer.Sound(ruta_completa)
                else:
                    self.sonidos[nombre] = None
            except Exception as e:
                self.sonidos[nombre] = None
    
    # MODIFICACIÓN: Añadimos loops=-1 para que la música se repita infinitamente
    def reproducir(self, nombre, loops=-1):
        """Reproducir un sonido por su nombre"""
        if nombre in self.sonidos and self.sonidos[nombre] is not None:
            try:
                self.sonidos[nombre].play(loops=loops)
            except:
                pass
    
    def detener_todos(self):
        """Detener todos los sonidos"""
        for sonido in self.sonidos.values():
            if sonido is not None:
                try:
                    sonido.stop()
                except:
                    pass
    
    def ajustar_volumen(self, nombre, volumen):
        """Ajustar volumen de un sonido (0.0 a 1.0)"""
        if nombre in self.sonidos and self.sonidos[nombre] is not None:
            try:
                self.sonidos[nombre].set_volume(volumen)
            except:
                pass