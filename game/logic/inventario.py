class PlayerInventory:
    def __init__(self):
        self.fragmentos = 0
        self.llave_jungla = False
        self.llave_desierto = False
        self.llave_cofre = False  
        
        self.cristal = False
        self.moneda = False
        self.pociones = 10  
        self.gema_oscura = False # NUEVO OBJETO
        
        self.salud_maxima = 100
        self.salud_actual = 100
        self.cordura = 100 
        
    def agregar_fragmento(self):
        if self.fragmentos < 5:
            self.fragmentos += 1