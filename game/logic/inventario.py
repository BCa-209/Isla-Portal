class PlayerInventory:
    def __init__(self):
        self.fragmentos = 0
        self.llave_jungla = True
        self.llave_desierto = True
        self.llave_cofre = False 
        
        self.cristales = 10
        self.monedas = 10
        self.pociones = 10
        self.gema_oscura = True
        
        self.salud_maxima = 100
        self.salud_actual = 100
        self.cordura = 100
        
        self.muertes_comunes = 0 # Controlador para el final especial
        
    def agregar_fragmento(self):
        if self.fragmentos < 5:
            self.fragmentos += 1