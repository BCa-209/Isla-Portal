import config
import json
import os
import random
import heapq
from game.logic.inventario import PlayerInventory

class GameManager:
    def __init__(self):
        self.estado = "EN_CURSO"
        self.inventario = PlayerInventory()
        self.nivel_actual = 1
        self.nivel_objetivo = 1 
        
        self.TIERRA = 0 
        self.AGUA = 1 
        self.ROCA = 2 
        self.PORTAL = 3 
        self.CRISTAL = 4 
        self.JEFE = 5
        self.PORTAL_AZUL = 6
        self.LLAVE = 7 
        self.MONEDA = 8
        self.POCION = 9
        self.CUEVA = 10 
        self.COFRE = 11         
        self.PORTAL_MORADO = 12 
        self.CADAVER = 13
        
        self.textos_items = self._cargar_json("items.json")
        self.textos_lore = self._cargar_json("lore.json")
        
        self.texto_dialogo = ""
        self.texto_lore = ""
        self.enemigo_en_combate = None
        
        self.mapas = {}
        self.enemigos_por_nivel = {}
        
        self._inicializar_mundo()
        self.cargar_nivel(self.nivel_actual)

    def _cargar_json(self, nombre_archivo):
        try:
            ruta = os.path.join("data", nombre_archivo)
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return {}

    def _inicializar_mundo(self):
        self.mapas[1] = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 2, 4, 0, 0, 1, 1, 1, 0, 2, 0, 1],
            [1, 0, 1, 1, 0, 10, 2, 0, 0, 0, 0, 1, 0, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 1],
            [1, 0, 2, 2, 0, 1, 1, 0, 2, 8, 0, 1, 0, 2, 0, 1], 
            [1, 0, 7, 2, 0, 1, 1, 0, 2, 2, 0, 1, 0, 0, 0, 1], 
            [1, 0, 4, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 1],
            [1, 0, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 2, 1],
            [1, 1, 0, 0, 0, 0, 0, 2, 0, 2, 4, 0, 0, 0, 3, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.enemigos_por_nivel[1] = [
            {"fila": 4, "col": 4, "tipo": "circulo", "ruta": [(0, 1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1), (-1, 0), (-1, 0)], "paso_actual": 0},
            {"fila": 10, "col": 14, "tipo": "vagabundo"}
        ]

        self.mapas[2] = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 12, 0, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 2, 2, 0, 1, 1, 1, 0, 4, 2],
            [2, 6, 2, 0, 0, 0, 2, 9, 2, 0, 0, 1, 0, 0, 0, 2], 
            [2, 6, 2, 0, 2, 0, 2, 0, 2, 2, 0, 0, 0, 2, 0, 2],
            [2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0, 2],
            [2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 2, 4, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 2],
            [2, 0, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0, 2, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 7, 2, 3, 2], 
            [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]
        self.enemigos_por_nivel[2] = [
            {"fila": 6, "col": 11, "tipo": "estatico"},
            {"fila": 9, "col": 7, "tipo": "estatico"}
        ]

        self.mapas[3] = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
            [1, 2, 0, 2, 2, 2, 11, 0, 0, 2, 2, 2, 2, 0, 2, 1],
            [1, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 1],
            [1, 2, 0, 2, 0, 0, 0, 5, 5, 0, 0, 0, 2, 0, 2, 1],
            [1, 2, 0, 2, 0, 0, 0, 5, 5, 0, 0, 0, 2, 0, 2, 1],
            [1, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 1],
            [1, 2, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 2, 1],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 6, 6, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.enemigos_por_nivel[3] = [
            {"fila": 7, "col": 7, "tipo": "estatico"},
            {"fila": 7, "col": 8, "tipo": "estatico"}
        ]
        
        self.mapas[4] = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 2], 
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]
        self.enemigos_por_nivel[4] = [
            {"fila": 4, "col": 7, "tipo": "estatico"},
            {"fila": 6, "col": 7, "tipo": "estatico"},
            {"fila": 5, "col": 6, "tipo": "estatico"},
            {"fila": 5, "col": 8, "tipo": "estatico"},
            {"fila": 3, "col": 8, "tipo": "vagabundo"}
        ]

    def cargar_nivel(self, nivel):
        self.nivel_actual = nivel
        self.mapa = self.mapas[nivel]
        self.enemigos = self.enemigos_por_nivel[nivel]
        self.filas = len(self.mapa)
        self.columnas = len(self.mapa[0])
        self.estado = "EN_CURSO"
        
        if nivel == 1:
            self.jugador_pos = [1, 1]
            self.pos_aparicion = [1, 1]
        elif nivel == 2:
            self.jugador_pos = [1, 1]
            self.pos_aparicion = [1, 1]
        elif nivel == 3:
            self.jugador_pos = [9, 7]
            self.pos_aparicion = [9, 7]
        elif nivel == 4:
            self.jugador_pos = [10, 2]
            self.pos_aparicion = [10, 2]
            self.inventario.cordura = 50 

    def _aplicar_paranoia(self, texto):
        """Corrompe el texto intercambiando letras por símbolos si la cordura es baja."""
        cordura = self.inventario.cordura
        
        # Si la cordura es mayor a 50, el texto se lee perfectamente
        if cordura > 50:
            return texto
            
        # Mientras menor sea la cordura, mayor será la probabilidad matemática de corrupción
        # A 0 de cordura, cerca del 30% del texto será ilegible.
        probabilidad_corrupcion = max(0, (90 - cordura) / 90.0)
        caracteres_extranos = "¡!@#$%&*?¿/X~+Ø‡"
        
        texto_corrupto = ""
        for char in texto:
            # Solo corrompemos letras, respetando los espacios y signos de puntuación originales
            if char.isalpha() and random.random() < probabilidad_corrupcion:
                texto_corrupto += random.choice(caracteres_extranos)
            else:
                texto_corrupto += char
                
        return texto_corrupto

    def preparar_carga(self, nivel_destino):
        self.nivel_objetivo = nivel_destino
        self.texto_lore = self.textos_lore.get(str(nivel_destino), "Misterios inexplorados...")
        self.estado = "CARGANDO"

    def preparar_carga(self, nivel_destino):
        self.nivel_objetivo = nivel_destino
        
        if self.inventario.cordura <= 45:
            # Selecciona un mensaje perturbador aleatorio
            lista_locura = self.textos_lore.get("mensajes_locura", ["Algo te observa..."])
            self.texto_lore = random.choice(lista_locura)
            # También corrompemos visualmente este texto
            self.texto_lore = self._aplicar_paranoia(self.texto_lore)
        else:
            # Carga el lore normal sin corrupción
            self.texto_lore = self.textos_lore.get(str(nivel_destino), "Misterios inexplorados...")
            
        self.estado = "CARGANDO"

    def iniciar_dialogo(self, texto):
        self.texto_dialogo = self._aplicar_paranoia(texto)
        self.estado = "DIALOGO"
        
    def cerrar_dialogo(self):
        self.texto_dialogo = ""
        self.estado = "EN_CURSO"
        
    def reiniciar_tras_derrota(self):
        self.estado = "EN_CURSO"
        self.jugador_pos = self.pos_aparicion.copy()

    def _heuristica_manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _obtener_vecinos_transitables(self, fila, col):
        vecinos = []
        # El Vagabundo no puede cruzar paredes, agua, cofres, portales, etc.
        obstaculos = [self.AGUA, self.ROCA, self.JEFE, self.COFRE, self.PORTAL_MORADO, self.CADAVER, self.CUEVA]
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for df, dc in direcciones:
            nf, nc = fila + df, col + dc
            if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                if self.mapa[nf][nc] not in obstaculos:
                    vecinos.append((nf, nc))
        return vecinos

    def _calcular_ruta_a_estrella(self, inicio, objetivo):
        frontera = []
        heapq.heappush(frontera, (0, inicio))
        costo_acumulado = {inicio: 0}
        padre = {inicio: None}

        while frontera:
            _, actual = heapq.heappop(frontera)

            if actual == objetivo:
                break

            for vecino in self._obtener_vecinos_transitables(actual[0], actual[1]):
                nuevo_costo = costo_acumulado[actual] + 1
                if vecino not in costo_acumulado or nuevo_costo < costo_acumulado[vecino]:
                    costo_acumulado[vecino] = nuevo_costo
                    # F(n) = G(n) + H(n)
                    prioridad = nuevo_costo + self._heuristica_manhattan(vecino, objetivo)
                    heapq.heappush(frontera, (prioridad, vecino))
                    padre[vecino] = actual

        if objetivo not in padre:
            return [] # No hay ruta posible (encerrado)

        # Reconstruir camino
        ruta = []
        actual = objetivo
        while actual != inicio:
            ruta.append(actual)
            actual = padre[actual]
        ruta.reverse()
        return ruta
    
    def actualizar_enemigos(self):
        if self.estado != "EN_CURSO":
            return
            
        for enemigo in self.enemigos:
            if enemigo.get("distraido"):
                continue # Si ya lo distrajiste (Sectario), no se mueve.
                
            if enemigo["tipo"] == "circulo":
                mov = enemigo["ruta"][enemigo["paso_actual"]]
                enemigo["fila"] += mov[0]
                enemigo["col"] += mov[1]
                enemigo["paso_actual"] = (enemigo["paso_actual"] + 1) % len(enemigo["ruta"])

            elif enemigo["tipo"] == "vagabundo":
                # Detectar al jugador dentro de un radio de 5 casillas

                df = self.jugador_pos[0] - enemigo["fila"]
                dc = self.jugador_pos[1] - enemigo["col"]

                distancia = (df ** 2 + dc ** 2) ** 0.5

                if distancia <= 5:

                    # Calcular la ruta con A*
                    inicio = (enemigo["fila"], enemigo["col"])
                    objetivo = (
                        self.jugador_pos[0],
                        self.jugador_pos[1]
                    )

                    ruta = self._calcular_ruta_a_estrella(
                        inicio,
                        objetivo
                    )

                    # Si hay ruta, avanzar una casilla
                    if len(ruta) > 0:
                        siguiente_paso = ruta[0]

                        enemigo["fila"] = siguiente_paso[0]
                        enemigo["col"] = siguiente_paso[1]

                    self._evaluar_colisiones_enemigos()

    def intentar_mover_jugador(self, delta_fila, delta_col):
        if self.estado != "EN_CURSO":
            return

        nueva_fila = self.jugador_pos[0] + delta_fila
        nueva_col = self.jugador_pos[1] + delta_col

        if 0 <= nueva_fila < self.filas and 0 <= nueva_col < self.columnas:
            tipo_casilla = self.mapa[nueva_fila][nueva_col]
            
            if tipo_casilla not in [self.AGUA, self.ROCA, self.JEFE, self.COFRE, self.PORTAL_MORADO, self.CADAVER]:
                self.jugador_pos = [nueva_fila, nueva_col]
                self._evaluar_interacciones(tipo_casilla, nueva_fila, nueva_col)
                self._evaluar_colisiones_enemigos()
            
            if tipo_casilla == self.JEFE:
                self.enemigo_en_combate = {"tipo": "jefe", "fila": nueva_fila, "col": nueva_col}
                self.estado = "COMBATE"
            elif tipo_casilla == self.COFRE:
                self._evaluar_interacciones(tipo_casilla, nueva_fila, nueva_col)
            elif tipo_casilla == self.PORTAL_MORADO:
                self._evaluar_interacciones(tipo_casilla, nueva_fila, nueva_col)
            elif tipo_casilla == self.CADAVER:
                self._evaluar_interacciones(tipo_casilla, nueva_fila, nueva_col)

    def _evaluar_colisiones_enemigos(self):
        for enemigo in self.enemigos:
            # NUEVO: Ignoramos la colisión si el enemigo está distraído con la moneda
            if enemigo.get("distraido"):
                continue
                
            if enemigo["fila"] == self.jugador_pos[0] and enemigo["col"] == self.jugador_pos[1]:
                self.enemigo_en_combate = enemigo
                self.estado = "COMBATE"

    def _evaluar_interacciones(self, casilla, fila, col):
        if casilla == self.CUEVA:
            self.preparar_carga(4) 
            
        elif casilla == self.CADAVER:
            self.iniciar_dialogo("Los restos de un ritual atroz. Mejor no acercarse más.")
            
        elif casilla == self.CRISTAL:
            self.inventario.cristales += 1
            self.inventario.agregar_fragmento()
            self.inventario.cordura = min(100, self.inventario.cordura + 10)
            self.mapa[fila][col] = self.TIERRA
            self.iniciar_dialogo(self.textos_items.get("cristal", "Objeto recolectado."))
            
        elif casilla == self.MONEDA:
            self.inventario.monedas += 1 # Sumar al contador
            self.inventario.cordura = min(100, self.inventario.cordura + 5)
            self.mapa[fila][col] = self.TIERRA
            self.iniciar_dialogo(self.textos_items.get("moneda", "Objeto recolectado."))
            
        elif casilla == self.POCION:
            self.inventario.pociones += 1
            self.inventario.cordura = min(100, self.inventario.cordura + 5)
            self.mapa[fila][col] = self.TIERRA
            self.iniciar_dialogo(self.textos_items.get("pocion", "Objeto recolectado."))
            
        elif casilla == self.LLAVE:
            self.inventario.cordura = max(0, self.inventario.cordura - 5)
            if self.nivel_actual == 1:
                self.inventario.llave_jungla = True
                self.iniciar_dialogo(self.textos_items.get("llave_jungla", "Llave obtenida."))
            elif self.nivel_actual == 2:
                self.inventario.llave_desierto = True
                self.iniciar_dialogo(self.textos_items.get("llave_desierto", "Llave obtenida."))
            self.mapa[fila][col] = self.TIERRA
            
        elif casilla == self.PORTAL:
            puede_cruzar = False
            if self.nivel_actual == 1 and self.inventario.llave_jungla:
                puede_cruzar = True
            elif self.nivel_actual == 2 and self.inventario.llave_desierto:
                puede_cruzar = True
                
            if puede_cruzar:
                if self.nivel_actual < 3:
                    self.preparar_carga(self.nivel_actual + 1)
            elif self.nivel_actual == 3:
                self.estado = "FIN"
            else:
                self.iniciar_dialogo(self.textos_items.get("portal_cerrado", "Portal cerrado."))
                
        elif casilla == self.PORTAL_AZUL:
            if self.nivel_actual == 4:
                self.preparar_carga(1) 
            elif self.nivel_actual > 1:
                self.preparar_carga(self.nivel_actual - 1)
                
        elif casilla == self.COFRE:
            if self.inventario.llave_cofre:
                self.inventario.gema_oscura = True
                self.mapa[fila][col] = self.TIERRA 
                self.iniciar_dialogo(self.textos_items.get("cofre_abierto", "Gema Oscura obtenida."))
            else:
                self.iniciar_dialogo(self.textos_items.get("cofre_cerrado", "Cofre sellado."))
                
        elif casilla == self.PORTAL_MORADO:
            if self.inventario.gema_oscura:
                self.inventario.cordura = 0 
                self.estado = "FINAL_COSMICO" 
            else:
                self.iniciar_dialogo(self.textos_items.get("portal_morado_cerrado", "Falta la Gema Oscura."))