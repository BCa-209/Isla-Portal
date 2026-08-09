class PlayerInventory:
    def __init__(self):
        self.fragmentos = 0
        self.llave_jungla = False
        self.llave_desierto = False
        self.llave_cofre = False  
        
        self.cristales = 0
        self.monedas = 0
        self.pociones = 0  
        self.gema_oscura = False
        
        self.salud_maxima = 100
        self.salud_actual = 100
        self.cordura = 40 
        
        self.muertes_comunes = 0 # Controlador para el final especial
        
    def agregar_fragmento(self):
        if self.fragmentos < 5:
            self.fragmentos += 1