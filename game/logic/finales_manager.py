import json
import os

class EndingManager:
    def __init__(self, inventario):
        self.inventario = inventario
        self.textos_finales = self._cargar_json()
        self.lore = self._cargar_json()

    def _cargar_json(self):
        """Carga el archivo ending.json desde la carpeta data."""
        ruta = os.path.join("data", "ending.json")
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            print(f"[Advertencia] No se encontró el archivo {ruta}.")
            return {}

    def _obtener_final(self, clave):
        """Busca el título y el texto en el diccionario cargado."""
        datos = self.textos_finales.get(clave, {})
        titulo = datos.get("titulo", "Fin del Juego")
        texto = datos.get("texto", "El destino es incierto...")
        return titulo, texto

    def evaluar_final(self, contexto, decision=None):
        
        # 1. Finales por Muerte
        if contexto == "muerte_comun":
            self.inventario.muertes_comunes += 1
            if self.inventario.muertes_comunes == 1:
                return self._obtener_final("muerte_comun_1")
            else:
                return self._obtener_final("muerte_comun_2")
                
        elif contexto == "muerte_jefe":
            return self._obtener_final("muerte_jefe")
            
        # 2. Finales de Victoria (Decisión en el Monumento)
        elif contexto == "decision_monumento":
            if decision == "huir":
                return self._obtener_final("decision_huir")
                
            elif decision == "activar_portal":
                # Evaluamos el esfuerzo del jugador explorando
                if self.inventario.cristales >= 5:
                    return self._obtener_final("decision_activar_convergencia")
                else:
                    return self._obtener_final("decision_activar_fuga")
                    
            elif decision == "destruir_nucleo":
                return self._obtener_final("decision_destruir")

        # Por seguridad, si llega un contexto no programado
        return "FINAL DESCONOCIDO", "Has atravesado la membrana de la realidad. La Entidad Cósmica que te susurra desde el vacío absoluto se hace presente, sin tiempo ni espacio."