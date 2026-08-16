Los apartados que describen el proyecto es:
- Generación
- Validación
- Reusabilidad
- Empaquetado pip
- Interfaz Visual (por terminal o por otros)

## Reparto (por hacer)
### gapostig: Bloque Motor
genera el laberinto, lo valida, lo resuelve, y se empaqueta como librería pip reutilizable.

| Tarea                             | Detalle                                                                                                                                               |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Modelo de datos                   | `Grid` de celdas, cada celda = 4 bits (N=1,E=2,S=4,W=8) según tabla del enunciado                                                                     |
| Algoritmo de generación           | Recursive backtracker (recomendado, fácil de razonar y de convertir en "perfecto")                                                                    |
| Modo PERFECT=True                 | Un único camino, sin bucles (spanning tree puro)                                                                                                      |
| Modo PERFECT=False <br>(Pac-Man)  | Partir del perfecto y quitar muros extra para crear ≥2 rutas independientes, garantizar accesibilidad de las 4 esquinas + centro, minimizar dead-ends |
| Restricción de anchura de pasillo | Nunca una zona abierta 3×3: comprobar tras cada apertura de muro<br>                                                                                  |
| Patrón "42"                       | Reservar un bloque de celdas totalmente cerradas con esa forma (o error si el maze es demasiado pequeño)                                              |
| Coherencia de muros               | Si celda (x,y) tiene muro Este, celda (x+1,y) debe tener muro Oeste (invariante que debe mantenerse siempre, no solo comprobarse al final)            |
| Reproducibilidad                  | Parámetro `seed` en el constructor                                                                                                                    |
| Solver                            | BFS desde entry hasta exit → devuelve string de letras N/E/S/W                                                                                        |
| Empaquetado pip                   | `pyproject.toml`, build co`n python -m build`, generar `mazegen-*.whl`                                                                                |
| Docstrings + type hints           | PEP257 + typing, para pasar mypy                                                                                                                      |
| Tests unitarios                   | grid, algoritmos, validador, solver                                                                                                                   |

### carmgome: Bloque App
parsea la config, llama al motor, escribe el fichero de salida en formato hexadecimal, y muestra la visualización interactiva.

| Tarea                             | Detalle                                                                                                                                                     |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `a_maze_ing.py`                   | Orquesta: lee `argv`, llama a `config_parser`, instancia `MazeGenerator`, llama a `output_writer`, lanza `display`                                          |
| Parser de config                  | `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT` obligatorios + ignorar líneas `#`; validar tipos y rangos                                      |
| Gestión de errores                | Fichero no encontrado, sintaxis inválida, entry=exit, fuera de rango, maze imposible → mensajes claros, nunca crash                                         |
| `output_writer	`                  | Escribe grid fila a fila en hex, línea vacía, luego entry/exit/solución con `\n` final en cada línea                                                        |
| Visualización                     | ASCII en terminal (más rápido de entregar que MLX): mostrar muros, entry, exit, patrón 42; menú: regenerar / mostrar-ocultar camino / rotar colores / salir |
| ntegración con `maze_analyzer.py` | Probar el output generado con el analizador dado, iterar hasta que valide ambos modos                                                                       |
| Makefile                          | install/run/debug/clean/lint/lint-strict                                                                                                                    |
| README.md                         | Toda la documentación exigida (ver sección 4)                                                                                                               |
| Tests                             | config_parser, output_writer, tests end-to-end (config → fichero de salida)                                                                                 |


## Estructura de carpetas
```
a-maze-ing/
├── a_maze_ing.py                 # archivo principal (el main)
├── config.txt                    # config por defecto (obligatoria en el repo)
├── Makefile                      
├── .gitignore
├── README.md
├── LICENSE.md                    # licencia que permita reutilizar mazegen en otro proyecto
├── pyproject.toml                # metadata para construir el paquete mazegen
```
#### === PAQUETE REUTILIZABLE (gabriel) ===
```
├── mazegen/                      
│   ├── __init__.py                # expone MazeGenerator
│   ├── generator.py               # clase MazeGenerator (orquestador)
│   ├── grid.py                    # Cell / Grid: representación en bits (N,E,S,W)
│   ├── algorithms.py              # recursive backtracker, (+bonus: Kruskal/Prim)
│   ├── validator.py               # corridors ≤2 celdas, conectividad, coherencia muros
│   ├── pattern42.py               # inserción del patrón "42"
│   ├── solver.py                  # BFS/DFS -> camino más corto (string NESW)
│   └── py.typed
```
#### === APLICACIÓN (carmen) ===
```
|── app/                          
│   ├── config_parser.py           # lectura KEY=VALUE, comentarios #, validación
│   ├── output_writer.py           # escritura fichero hex + entry/exit/path
│   ├── errors.py                  # excepciones propias + mensajes claros
│   └── display/
│       ├── ascii_view.py          # render ASCII en terminal + menú interactivo
│       └── mlx_view.py            # (opcional) render gráfico MLX
```
#### Empaquetado
```
|── dist/                          # generado por `python -m build` -> mazegen-*.whl/.tar.gz
│   └── mazegen-1.0.0-py3-none-any.whl   # ⚠️ debe copiarse/estar también en la RAÍZ del repo
``` 
#### Test
```
├── tests/                         # tests propios (no evaluados pero exigidos)
│   ├── test_grid.py
│   ├── test_algorithms.py
│   ├── test_validator.py
│   ├── test_solver.py
│   ├── test_config_parser.py
│   └── test_output_writer.py
│
└── maze_analyzer.py                # el script que da el enunciado, para autocomprobar
```
## Checklist README.md
- [x] Primera línea en cursiva: This project has been created as part of the 42 curriculum by carmgome, gapostig ✅ 
- [ ] Sección Description
- [ ] Sección Instructions (compilación/instalación/ejecución)
- [ ] Sección Resources (referencias + cómo se usó la IA, para qué tareas y en qué partes)
- [ ] Formato completo del fichero de config
- [ ] Algoritmo de generación elegido y por qué
- [ ] Qué parte del código es reutilizable y cómo (instanciar, parámetros, acceder a estructura/solución — con ejemplo de código)
- [ ] Roles de cada miembro del equipo
- [ ] Planificación inicial vs. real
- [ ] Qué funcionó bien / qué mejoraríais
- [ ] Herramientas específicas usadas

## Puntos de atención especiales (donde suele fallar la gente)

1. **Coherencia de muros**: no vale generar cada celda de forma independiente; un muro es una propiedad compartida entre dos celdas vecinas.
2.  **Anchura de pasillo**: hay que comprobarlo dinámicamente al abrir muros en el modo no-perfecto, no solo al final.
3. **"42" como excepción a la conectividad**: esas celdas están aisladas a propósito; el validador de conectividad global debe excluirlas explícitamente.
4. **Modo Pac-Man ≠ perfecto con un muro quitado**: el enunciado lo prohíbe explícitamente, hace falta ≥2 rutas independientes reales.
5. **El paquete `mazegen-*` debe estar en la raíz del repo**, no solo construible desde `mazegen/`.
6. **Nunca debe crashear**: todo error (config mal formada, maze imposible, tamaño insuficiente para el "42", etc.) debe capturarse y mostrar un mensaje.

## Fases sugeridas (con puntos de sincronización)

**Fase 0 — Diseño conjunto (media jornada, juntos)**
- Fijar el contrato de `MazeGenerator` de arriba.
- Decidir formato interno de config y estructura de celdas.
- Elegir licencia (LICENSE.md) y algoritmo.

**Fase 1 — En paralelo**
- A: `grid.py` + recursive backtracker básico (modo perfecto) + tests.
- B: `config_parser.py` + `errors.py` + tests, usando un `MazeGenerator` "fake"/stub que cumpla el contrato.

**Fase 2 — En paralelo**
- A: modo no-perfecto (Pac-Man: loops, esquinas, centro, dead-ends), validador de corridor-width y coherencia de muros, patrón 42.
- B: `output_writer.py` + primera versión de `a_maze_ing.py` conectando parser → (stub) generator → writer.

**Fase 3 — Integración 1**
- Sustituir el stub por el `MazeGenerator` real de A.
- Ejecutar `maze_analyzer.py` sobre las salidas y corregir juntos lo que falle.

**Fase 4 — En paralelo**
- A: `solver.py` (BFS), empaquetado pip (`pyproject.toml`, build), docstrings/mypy/flake8 en `mazegen/`.
- B: `ascii_view.py` con el menú interactivo completo, mypy/flake8 en `app/`.

**Fase 5 — Integración final + pulido**
- Makefile completo, `.gitignore`, README.md, LICENSE.md.
- Construir el `.whl` y verificarlo en un venv limpio (esto os lo pueden pedir en la evaluación).
- Revisión cruzada: cada uno lee el código del otro y debe poder explicarlo (regla anti-"no entiendo lo que generó la IA").

**Fase 6 (si hay tiempo) — Bonus**
- No dead-ends en modo Pac-Man (braided maze).
- Segundo algoritmo (Kruskal o Prim) seleccionable por config.
- Animación de generación.
