# Juego del Sapito

## Estructura del Proyecto
Ejemplo de la estructura del juego del sapito para futuras actualizaciones
``` text
Juego-Sapito/
│
├── core/
│   ├── entidad_base.py
│   └── escena_base.py
│
├── assets/
│   ├── sounds/
│       ├── win.mp3
│       ├── lose.mp3
│       └── move.mp3
│
├── game/
│   ├── entities/
│   │   ├── tablero.py
│   │   ├── cursor.py
│   ├── logic/
│   │   └── tres_en_raya.py
│   └── scenes/
│       └── escena_juego.py
│
├── config.py
└── main.py
```
\ISLAS-PORTAL
│   config.py
│   main.py
│
├───assets
│   ├───images
│   │       carga_nivel_1.png
│   │       carga_nivel_2.png
│   │       carga_nivel_3.png
│   │       carga_nivel_4.png
│   │
│   └───sounds
│           cave.mp3
│           final_real.mp3
│           temple.mp3
│
├───core
│   │   entidad_base.py
│   │   escena_base.py
│   │   __init__.py
│   │
│   └───__pycache__
│
├───data
│       ending.json
│       items.json
│       lore.json
│
└───game
    ├───entities
    │       enemigos.py
    │       jugador.py
    │       objetos.py
    │       __init__.py
    │
    ├───graphics
    │       terreno.py
    │
    ├───logic
    │       finales_manager.py
    │       ia_enemigos.py
    │       inventario.py
    │       motor_combate.py
    │       motor_juego.py
    │       __init__.py
    │
    ├───scenes
    │       escena_combate.py
    │       escena_cosmica.py
    │       escena_isla.py
    │       escena_jefe.py
    │       escena_menu.py
    │       __init__.py
    │
    └───sounds
            gestor_audio.py
            __init__.py