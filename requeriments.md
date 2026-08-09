# Propuesta de Proyecto Final
## 1. Información General
*   **Nombre del videojuego:** Islas Portal
*   **Integrante:** Brayan Luis Calderon Calderon
*   **Género del juego:** RPG 2D de exploración
*   **Descripción general:** El jugador despierta en un archipiélago misterioso formado por tres islas. Para avanzar deberá explorar distintos biomas, derrotar enemigos, encontrar objetos clave y activar antiguos portales utilizando llaves mágicas.
*   **Objetivo del jugador:** Explorar el archipiélago, derrotar al jefe final ubicado en el monumento antiguo y tomar una decisión que determinará uno de los múltiples finales del juego.

## 2. Justificación
Este proyecto representa una oportunidad excelente para aplicar un enfoque orientado a objetos y estructuras de datos sólidas para modularizar el código antes de entrar al motor. El diseño de múltiples finales controlados por variables de estado y la gestión del inventario plantean desafíos algorítmicos valiosos.

## 3. Entidades del Videojuego

### 3.1 Entidades Lógicas

| Nombre | Responsabilidad | Atributos principales | Comportamientos principales |
| :--- | :--- | :--- | :--- |
| **GameManager** | Gestiona el estado global del juego. | Estado (en curso, pausa, fin). | Calcula el porcentaje de completado general rastreando la exploración. |
| **PlayerInventory** | Estructura de datos que almacena el progreso. | Banderas booleanas para objetos, contador (0 a 5). | Lleva el registro de Cristales, Amuleto, Llaves, Núcleo y Fragmentos. |
| **Ending Manager** | Estructura condicional evaluada al final. | Decisión del jugador, estado del inventario. | Dispara uno de los 5 finales (Normal, Bueno, Malo, Alternativo, Secreto). |
| **BossController** | Script para la inteligencia artificial del jefe. | Fases de ataque. | Instancia la llave o libera energía al llegar a 0 HP. |

### 3.2 Entidades Gráficas

| Nombre | Qué representa | Cómo será dibujada | Observaciones |
| :--- | :--- | :--- | :--- |
| **Protagonista** | Personaje controlado. | Spritesheet de movimiento, animaciones idle y combate. | Requiere mayor detalle para el control del PlayerController. |
| **Enemigos** | Slimes, Murciélagos, Momias, etc. | Sprites animados de ataque, patrullaje y muerte. | Cambian según la isla o bioma. |
| **Entornos** | Mapas de las islas (Playa, Desierto, Monumento). | Tilesets y Backgrounds. | Distintos biomas visuales. |
| **UI y VFX** | Interfaces y efectos de transición. | Pantallas de transición. | Importante para el SceneController. |

## 4. Lógica del Juego
*   **Inicio de la partida:** Tras un naufragio, el protagonista despierta en una isla desconocida y debe explorar una antigua cueva.
*   **Movimiento del jugador:** El `PlayerController` maneja los inputs, las físicas de movimiento 2D, colisiones y estado de combate.
*   **Interacción entre entidades:** Los recolectables usan `InteractableItem` para actualizar el inventario al colisionar con el jugador. Los portales validan requisitos de acceso leyendo el inventario.
*   **Condiciones de victoria:** Llegar a la Isla Final, derrotar al Jefe Final en el monumento y tomar una decisión.
*   **Condiciones de derrota:** Recibir daño de la `EnemyAI` hasta perder toda la salud.
*   **Sistema de puntaje:** No aplica puntaje, sino un sistema de exploración basado en la obtención de los 5 Fragmentos Perdidos, lo cual impacta el árbol de finales.

## 5. Arquitectura básica propuesta
El proyecto se organizará mediante una arquitectura modular estricta orientada a objetos en Python, separando la infraestructura base, los componentes gráficos, el motor lógico y el flujo de escenas. Esta estructura garantiza el desacoplamiento de código, facilita el mantenimiento e independiza el renderizado del estado del juego.

```text
Isla-Portal/
assets/
  sounds/                   # Efectos de audio y música (.mp3)
    ambient_monument.mp3
    combat_boss.mp3
core/                       # Clases base abstractas (Herencia)
  entidad_base.py           # Plantilla con métodos de actualización y dibujo
  escena_base.py            # Plantilla para la gestión de estados de escena
game/
  entities/                 # Renderizado y primitivas gráficas
    jugador.py              # Dibujo vectorizado/primitivas del protagonista
    enemigos.py             # Formas y animaciones por código de enemigos
    objetos.py              # Representación gráfica de ítems y portales
  logic/                    # Motor del juego y reglas de negocio
    motor_juego.py          # Bucle principal, control de tiempos y físicas
    inventario.py           # Estructura de datos (booleans, fragmentos 0-5)
    finales_manager.py      # Evaluación de condiciones para los finales
  scenes/                   # Integración (Unión de Lógica + Gráficos)
    escena_menu.py          # Interfaz de inicio y pausa
    escena_isla.py          # Unifica lógica y renderizado de mapas/biomas
    escena_jefe.py          # Escenario del monumento y batalla final
  sounds/
    gestor_audio.py         # Wrapper para la reproducción de sonidos
config.py                   # Constantes globales (Resolución, Colores RGB, FPS)
main.py                     # Punto de entrada del juego
```

**Descripción de Capas:**
*   **Punto de Entrada (`main.py` y `config.py`):** Configura la ventana de PyGame, establece la tasa de refresco (FPS), define la paleta de colores RGB requerida para las primitivas gráficas y arranca la ejecución general.
*   **Capa Base (`/core/`):** Define las abstracciones principales. `entidad_base.py` fuerza a que todo objeto implemente un método de actualización de posición y un método de dibujo sobre la pantalla, mientras que `escena_base.py` define el contrato para el cambio de pantallas.
*   **Representación Gráfica (`/game/entities/`):** Responsable exclusivamente del aspecto visual. Al no utilizar imágenes de mapa de bits (sprites/textures), los personajes, enemigos y objetos se dibujan mediante algoritmos y primitivas de PyGame (polígonos, círculos, rectángulos y trazados de líneas).
*   **Core Lógico (`/game/logic/`):** Contiene el motor interno del videojuego. Administra el estado, evalúa colisiones matemáticas, procesa las reglas de progreso, calcula el porcentaje de exploración y ejecuta el árbol condicional de los 5 finales en base al inventario.
*   **Ensamblado y Escenas (`/game/scenes/`):** Actúa como el puente integrador. Es el lugar donde conviven e interactúan las entidades gráficas y el motor lógico. Gestiona el ciclo de actualización/dibujo en pantalla, los menús de la interfaz y las transiciones entre las distintas islas.
*   **Recursos de Audio (`/assets/sounds/` y `/game/sounds/`):** Único directorio asignado para archivos multimedia estáticos, gestionados mediante un módulo wrapper que ejecuta los cambios de música ambiental y efectos de combate.

## 6. Niveles del Juego

| Nivel | Descripción | Nuevas dificultades | Nuevas funcionalidades |
| :--- | :--- | :--- | :--- |
| **Isla Principal** | Bioma de playa, selva, río, cascada y cueva. | Combate básico con Slimes, Murciélagos y el Guardián de la Cueva. | Recolección de Cristal Azul, Amuleto Antiguo y Llave. Activación de Portal Azul. |
| **Isla Desierta** | Bioma de arena, dunas, ruinas, oasis y templo. | Enemigos más complejos: Escorpiones gigantes, Momias. | Búsqueda del Núcleo Solar y segunda llave para activar el Portal Rojo. |
| **Isla Final** | Isla rocosa, vegetación escasa, Monumento gigante. | No hay enemigos comunes, combate directo contra el Jefe Final por fases. | Transición al interior del monumento, evento OnDeath del jefe y decisión final. |

## 7. Recursos Multimedia
*   **Sonidos y Música:** El `AudioManager` controlará cambios en música ambiental al entrar al monumento o en batallas.
*   **Efectos visuales:** Transiciones entre escenas.

## 8. Riesgos Técnicos
El riesgo técnico principal recae en el sistema de transición entre mapas (`SceneController`) sin perder el progreso del jugador almacenado en el `PlayerInventory`. Para resolverlo, será crucial gestionar la persistencia de datos y asegurar que el `Ending Manager` reciba el estado correcto de las variables en la escena final para detonar la cinemática adecuada.
