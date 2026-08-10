import config
import json
import os
import random
import heapq
from game.logic.inventario import PlayerInventory
from game.sounds.gestor_audio import SoundManager
from game.logic.finales_manager import EndingManager

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
        self.PORTAL_ROJO = 6
        self.LLAVE = 7 
        self.MONEDA = 8
        self.POCION = 9
        self.CUEVA = 10 
        self.COFRE = 11         
        self.PORTAL_MORADO = 12 
        self.CADAVER = 13

        self.PUENTE = 14
        self.TEMPLO = 15
        self.ENTRADATEMPLO = 16

        self.RUINAS = 17
        
        self.textos_items = self._cargar_json("items.json")
        self.textos_lore = self._cargar_json("lore.json")
        
        self.texto_dialogo = ""
        self.texto_lore = ""
        self.enemigo_en_combate = None
        
        self.mapas = {}
        self.enemigos_por_nivel = {}

        self.timer_locura = 0
        self.limite_locura = random.randint(300, 900)

        self.audio = SoundManager()
        
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
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
            [1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
            [1,1,1,0,12,0,1,1,1,1,0,0,0,0,2,2,2,2,2,0,0,4,0,1,1,1,1,1],
            [1,1,1,0,0,0,1,1,1,1,0,4,0,2,2,2,2,2,2,2,0,0,0,1,1,1,1,1],
            [1,1,1,1,0,1,1,1,0,0,0,0,2,2,2,2,2,2,2,2,0,0,0,1,1,1,1,1],
            [1,1,1,1,0,1,0,0,0,0,0,0,2,2,10,2,2,0,0,0,0,0,0,1,1,1,1,1],
            [1,1,1,1,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,0,0,0,1,1,1,1],
            [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
            [1,1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,1,1,1,1,1],
            [1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1],
            [1,1,0,9,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1],
            [1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,4,0,0,1,0,0,0,0,1,1],
            [1,1,1,0,0,0,9,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,3,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        self.enemigos_por_nivel[1] = [
            {"fila": 4, "col": 4, "tipo": "sectario"},
            {"fila": 8, "col": 14, "tipo": "sectario"},
        ]

        self.mapas[2] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
            [1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1],
            [1,1,0,6,0,0,1,1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1],
            [1,1,0,0,0,0,1,1,0,2,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,1,1,1,0,2,2,2,2,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1],
            [1,1,1,0,0,1,8,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,8,0,0,0,0,0,0,1,1,1],
            [1,1,1,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,2,2,2,0,0,1,1,1,1],
            [1,1,0,0,2,0,0,0,0,0,0,0,0,0,9,0,0,2,0,0,0,0,0,1,1,1,1,1],
            [1,1,0,2,2,2,0,2,0,2,0,2,2,0,0,0,0,0,0,2,0,0,0,1,1,1,1,1],
            [1,1,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,9,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,2,0,2,0,0,2,0,0,1,1,1,1],
            [1,1,0,2,2,0,0,0,0,0,1,1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,1,1],
            [1,1,0,0,0,0,0,0,0,1,1,0,0,8,8,0,0,0,2,0,0,0,0,3,0,0,1,1],
            [1,1,1,0,0,0,9,0,1,1,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        self.enemigos_por_nivel[2] = [
            {"fila": 13, "col": 5, "tipo": "vagabundo"},
            {"fila": 6, "col": 22, "tipo": "vagabundo"},
            {"fila": 4, "col": 10, "tipo": "vagabundo"}
        ]

        self.mapas[3] = [

            [1,1,1,1,1,2,2,2,2,2,2,2,2,2,1,1,1,1,1],  # 01
            [1,1,1,2,2,2,0,0,0,0,0,0,0,2,2,2,1,1,1],  # 02
            [1,1,1,2,0,0,0,0,0,0,0,0,0,0,0,2,1,1,1],  # 03
            [1,2,2,2,0,0,0,13,0,13,0,13,0,0,0,2,2,2,1],  # 04
            [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],  # 05
            [1,2,0,2,0,0,0,13,0,5,0,0,13,0,0,2,0,2,1],  # 06
            [1,2,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,2,1],  # 07
            [1,2,0,2,0,0,0,13,0,13,0,13,0,0,0,2,0,2,1],  # 08
            [1,2,0,2,2,2,0,0,0,0,0,0,0,2,2,2,0,2,1],  # 09
            [1,2,0,2,1,2,2,0,0,0,0,0,2,2,1,2,0,2,1],  # 10
            [1,2,0,2,1,1,2,2,2,2,2,2,2,1,1,2,0,2,1],  # 11
            [1,2,0,2,2,2,2,1,1,1,1,1,2,2,2,2,0,2,1],  # 12
            [1,2,0,0,0,0,2,1,1,1,1,1,2,0,0,0,0,2,1],  # 13
            [1,2,0,0,0,0,2,1,1,1,1,1,2,0,0,0,0,2,1],  # 14
            [1,2,0,0,0,0,2,1,1,1,1,1,2,0,0,11,0,2,1],  # 15
            [1,2,0,0,0,0,2,1,1,1,1,1,2,0,0,0,0,2,1],  # 16
            [1,2,2,0,0,0,2,2,2,2,2,2,2,0,0,0,2,2,1],  # 17
            [1,1,2,2,2,0,0,0,0,0,0,0,0,0,2,2,2,1,1],  # 18
            [1,1,1,1,2,2,2,2,2,0,2,2,2,2,2,1,1,1,1],  # 19
            [1,1,1,1,1,1,1,1,2,0,2,1,1,1,1,1,1,1,1],  # 20
            [1,1,1,1,1,1,1,1,2,0,2,1,1,1,1,1,1,1,1],  # 21
            [1,1,1,1,1,1,1,1,2,0,2,1,1,1,1,1,1,1,1],  # 22
            [1,1,1,1,1,1,1,1,2,0,2,1,1,1,1,1,1,1,1],  # 23
            [1,1,1,1,1,1,1,1,2,0,2,1,1,1,1,1,1,1,1],  # 24
            [1,1,1,1,1,1,2,2,2,0,2,2,2,1,1,1,1,1,1],  # 25
            [1,1,1,1,1,1,2,0,0,0,0,0,2,1,1,1,1,1,1],  # 26
            [1,1,1,1,1,1,2,0,0,0,0,0,2,1,1,1,1,1,1],  # 27
            [1,1,1,1,1,1,2,6,3,3,3,6,2,1,1,1,1,1,1],  # 28
            [1,1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1],  # 29
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # 30
        ]
        self.enemigos_por_nivel[3] = [
            {"fila": 4, "col": 5, "tipo": "sectario"},
            {"fila": 13, "col": 3, "tipo": "sectario"},
            {"fila": 13, "col": 14, "tipo": "vagabundo"},
            {"fila": 13, "col": 16, "tipo": "vagabundo"},
            {"fila": 5, "col": 9, "tipo": "lidersectario"}
        ]
        
        self.mapas[4] = [
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,0,0,0,2,0,2,2,2,2,2,0,2,0,0,2,2,2],
            [2,0,2,0,2,0,0,0,0,0,0,0,2,0,0,2,0,2],
            [2,0,2,0,2,0,0,0,0,0,0,0,2,0,0,2,0,2],
            [2,0,0,0,2,0,0,0,0,0,0,0,2,0,0,2,0,2],
            [2,0,2,0,2,0,0,0,13,0,0,0,2,0,0,2,0,2], 
            [2,0,2,0,2,0,0,0,0,0,0,0,2,0,0,2,0,2],
            [2,0,2,0,2,0,0,0,0,0,0,0,2,0,0,0,0,2],
            [2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
            [2,0,2,0,0,0,2,2,2,2,2,0,0,0,0,0,0,2],
            [2,6,2,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2], 
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        ]
        self.enemigos_por_nivel[4] = [
            # 5 8
            {"fila": 4, "col": 6, "tipo": "sectario"},
            {"fila": 5, "col": 6, "tipo": "sectario"},
            {"fila": 6, "col": 6, "tipo": "sectario"},
            {"fila": 4, "col": 10, "tipo": "sectario"},
            {"fila": 5, "col": 10, "tipo": "sectario"},
            {"fila": 6, "col": 10, "tipo": "sectario"},
            {"fila": 3, "col": 7, "tipo": "sectario"},
            {"fila": 3, "col": 8, "tipo": "sectario"},
            {"fila": 3, "col": 9, "tipo": "sectario"},
            {"fila": 7, "col": 7, "tipo": "sectario"},
            {"fila": 7, "col": 8, "tipo": "sectario"},
            {"fila": 7, "col": 9, "tipo": "sectario"},
            {"fila": 2, "col": 5, "tipo": "vagabundo"},
            {"fila": 2, "col": 11, "tipo": "vagabundo"}
            ]

    def cargar_nivel(self, nivel):
        self.nivel_actual = nivel
        self.mapa = self.mapas[nivel]
        self.enemigos = self.enemigos_por_nivel[nivel]
        self.filas = len(self.mapa)
        self.columnas = len(self.mapa[0])
        self.estado = "EN_CURSO"
        
        # Asignación de las nuevas posiciones iniciales
        if nivel == 1: # Isla Principal
            self.jugador_pos = [15, 6]
            self.pos_aparicion = [6, 6]
        elif nivel == 2: # Isla Desierta
            self.jugador_pos = [4, 3]
            self.pos_aparicion = [4, 3]
        elif nivel == 3: # Monumento Antiguo
            self.jugador_pos = [25, 9]
            self.pos_aparicion = [25, 9]
        elif nivel == 4: # Cueva Profunda
            self.jugador_pos = [9, 1]
            self.pos_aparicion = [2, 2]
            self.inventario.cordura = 50 # Efecto de locura al entrar a la cueva

        self.audio.detener_todos()
        if nivel == 3: # El Templo / Monumento Antiguo
            # Puedes ajustar el volumen de 0.0 (silencio) a 1.0 (máximo)
            self.audio.ajustar_volumen('templo', 0.5) 
            self.audio.reproducir('templo')
            
        elif nivel == 4: # La Cueva Profunda
            self.audio.ajustar_volumen('cueva', 0.3) 
            self.audio.reproducir('cueva')

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

    def evaluar_locura_espontanea(self):
        # Solo ocurre si estás caminando libremente por el mapa
        if self.estado != "EN_CURSO":
            return
            
        if self.inventario.cordura <= 80:
            self.timer_locura += 1
            
            if self.timer_locura >= self.limite_locura:
                # Reiniciamos el temporizador con un nuevo tiempo aleatorio
                self.timer_locura = 0
                self.limite_locura = random.randint(600, 1500) 
                
                # Seleccionamos y mostramos el pensamiento
                lista_locura = self.textos_lore.get("mensajes_locura", ["No puedo más..."])
                pensamiento = random.choice(lista_locura)
                
                # Usamos iniciar_dialogo, el cual automáticamente le aplicará 
                # la corrupción matemática (_aplicar_paranoia) antes de mostrarlo
                self.iniciar_dialogo(pensamiento)
        else:
            # Si el jugador se cura y su cordura sube de 30, el contador se reinicia pacíficamente
            self.timer_locura = 0

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
                # ---> CORRECCIÓN: FINAL BUENO EN EL TEMPLO <---
                manager = EndingManager(self.inventario)
                
                # Evaluamos el final pasándole la decisión "activar_portal"
                titulo, texto = manager.evaluar_final("decision_monumento", "activar_portal")
                
                # Guardamos los textos para mostrarlos en pantalla
                self.titulo_final = titulo
                self.texto_final = texto
                self.estado = "VICTORIA_PORTAL"
                
                # Detenemos la música de tensión del templo
                self.audio.detener_todos()
            else:
                self.iniciar_dialogo(self.textos_items.get("portal_cerrado", "Portal cerrado."))
                
        elif casilla == self.PORTAL_ROJO:
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