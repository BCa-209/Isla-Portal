class EscenaBase:
    """Plantilla base para garantizar que todas las escenas compartan la misma estructura."""
    def manejar_eventos(self, eventos):
        pass

    def actualizar(self):
        pass

    def render(self, pantalla):
        pass