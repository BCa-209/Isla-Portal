# Sistema de Combate — Acciones Simultáneas

## Concepto

Sistema híbrido entre **combate por turnos y tiempo real**. El jugador y los enemigos **seleccionan sus acciones simultáneamente**, pero estas se ejecutan en tiempo real según el tiempo de preparación de cada acción.

No existe movimiento durante el combate.

---

## Flujo del combate

```text
Jugador selecciona acción
          +
Enemigo selecciona acción
          ↓
   Comienza la ejecución
          ↓
Las acciones avanzan en tiempo real
          ↓
Se ejecuta primero la acción
que termine su preparación
          ↓
Se aplican daños y efectos
          ↓
Nueva selección de acciones
```

---

## Acciones

Cada acción tiene:

* **Daño**
* **Tiempo de preparación**
* **Tiempo de recuperación**
* **Costo**
* **Efectos especiales**

Ejemplo:

```text
ATAQUE RÁPIDO
Daño: 15
Preparación: 0.6 s

ATAQUE PESADO
Daño: 35
Preparación: 1.8 s

POCIÓN
Curación: 30 HP
Preparación: 0.5 s

OBSERVAR
Sin daño
Preparación: 0.8 s
Revela información del enemigo
```

---

## Ejemplo

El jugador selecciona:

```text
ATAQUE PESADO
Preparación: 1.8 s
```

El enemigo selecciona:

```text
RITUAL
Preparación: 1.2 s
```

Durante el combate:

```text
0.0s ───────────────────── 1.8s

Jugador:
[████████████████████]

Enemigo:
[█████████████]
        ↑
     RITUAL
```

El ritual termina primero, por lo que el enemigo actúa antes que el jugador.

---

## Decisiones estratégicas

El sistema permite elegir entre **potencia y velocidad**:

| Acción        | Velocidad | Potencia     |
| ------------- | --------- | ------------ |
| Ataque rápido | Alta      | Baja         |
| Ataque pesado | Baja      | Alta         |
| Poción        | Alta      | Recuperación |
| Observar      | Media     | Información  |
| Interrumpir   | Alta      | Situacional  |

El jugador debe anticipar lo que hará el enemigo y elegir la acción adecuada.

---

## Interacciones

Las acciones pueden contrarrestarse entre sí:

```text
ATAQUE RÁPIDO
      ↓
interrumpe
      ↓
RITUAL
```

```text
DEFENSA
      ↓
reduce
      ↓
ATAQUE
```

```text
OBSERVAR
      ↓
revela
      ↓
RITUAL / DEBILIDAD
```

Esto permite que el combate sea más estratégico que simplemente atacar repetidamente.

---

## Adaptación Lovecraftiana

El sistema puede incorporar **Cordura** y **Conocimiento**.

### Cordura

Afecta la percepción del combate:

```text
Cordura alta
→ información fiable

Cordura baja
→ información incompleta
→ acciones desconocidas
→ posibles alteraciones visuales
```

### Observación

Permite descubrir información progresivamente:

```text
OBSERVAR

Debilidad: ???
Próxima acción: ???
Habilidad especial: ???
```

Después de observar:

```text
OBSERVAR

Debilidad: Ataques físicos
Próxima acción: Ritual
Habilidad especial: ???
```

---

## Jefes

Los jefes pueden utilizar acciones con preparación larga:

```text
┌─────────────────────────┐
│      LÍDER SECTARIO     │
│                         │
│ Preparando: RITUAL      │
│                         │
│ ████████████░░░ 80%     │
└─────────────────────────┘
```

El jugador debe decidir si:

* atacar;
* interrumpir;
* observar;
* usar una poción;
* asumir el riesgo y esperar.

Esto permite que las mecánicas de combate refuercen la narrativa del ritual y del culto.

---

## Ventajas

* Combina estrategia por turnos con tensión en tiempo real.
* No necesita movimiento.
* Las pociones tienen riesgo porque requieren tiempo.
* Permite enemigos con patrones diferentes.
* Las acciones pueden interrumpirse y contrarrestarse.
* Encaja bien con rituales, cultistas y horror cósmico.
* Es relativamente viable de implementar en Pygame.

## Riesgo principal

La **IA enemiga** debe elegir acciones de manera coherente. Si el enemigo selecciona acciones completamente aleatorias, el sistema pierde gran parte de su componente estratégico.

Por ello, conviene diseñar enemigos con **patrones de comportamiento reconocibles**, que el jugador pueda aprender mediante `OBSERVAR`.
