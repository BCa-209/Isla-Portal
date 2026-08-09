class BaseGrafica:
    def __init__(self, x, y, e):
        self.x = x
        self.y = y
        self.e = e
        self.color = (255, 255, 255)
        self.alfa = 0

    def setColor(self, color):
        self.color = color
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def setXY(self, x, y):
        self.x = x
        self.y = y
    def setEscala(self, e):
        self.e = e
    def setAlfa(self, alfa):
        self.alfa = alfa
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getXY(self):
        return (self.x, self.y)
    def getEscala(self):
        return self.e
    def getColor(self):
        return self.color
    def getAlfa(self):
        return self.alfa

class BaseLogica:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def moverArriba(self):
        self.fila -= 1
    def moverAbajo(self):
        self.fila += 1
    def moverIzquierda(self):
        self.columna -= 1
    def moverDerecha(self):
        self.columna += 1
    def setFila(self, fila):
        self.fila = fila
    def setColumna(self, columna):
        self.columna = columna
    def getFila(self):
        return self.fila
    def getColumna(self):
        return self.columna
    def getPosicion(self):
        return (self.fila, self.columna)

class EntidadJuego(BaseGrafica, BaseLogica):
    """
    Clase intermedia para manejar herencia múltiple.
    Hereda de BaseGrafica y BaseLogica.
    """
    def __init__(self, fila, columna, e, tam_celda):
        BaseLogica.__init__(self, fila, columna)
        BaseGrafica.__init__(self, columna * tam_celda, fila * tam_celda, e)
        self.tam_celda = tam_celda

    def actualizar_coordenadas(self):
        # Sincroniza la posicion logica con la posicion grafica
        self.setXY(self.getColumna() * self.tam_celda, self.getFila() * self.tam_celda)

    def moverArriba(self):
        super().moverArriba()
        self.actualizar_coordenadas()

    def moverAbajo(self):
        super().moverAbajo()
        self.actualizar_coordenadas()

    def moverIzquierda(self):
        super().moverIzquierda()
        self.actualizar_coordenadas()

    def moverDerecha(self):
        super().moverDerecha()
        self.actualizar_coordenadas()