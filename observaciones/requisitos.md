## Instrucciones Comunes
- Python >= 3.10
- Que pase *Flake8*
- Usar bloques `try-except`
- Se prefiere *context managers* para recursos como archivos o conexiones para limpieza automatica (`with` por ejemplo).
	- Si el programa crashea por algún comportamiento extraño, suspendes
- Todos los recursos deben ser manejados de forma correcta para evitar Leaks
- El código debe contener indicaciones del tipo de parámetros para las funciones (ej.`def fun(c: str)`), variables del tipo de devuelve y las variables cuando corresponda (mediante el uso del módulo *typing*).
- Debe pasar *mypy*
### Makefile
Se debe incluir un Makefile para automatizar tareas comunes, debe contener las siguientes reglas:
- *install* - Instala las dependencias de tu proyecto mediante *pip*, *uv*, *pipx* o el gestor de paquetes que uses.
- *run* - ejecuta el script principal de tu proyecto
- *debug* - Corre el script principal en modo debug usando el debugger incorporado de Python (ej. pdb)
- *clean* - Elimina archivos temporales o caché para mantener el ecosistema de tu proyecto limpio
- *lint* - Ejecuta los comandos `flake8 .` y `mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`
- *lint-strict* (opcional) - Ejecuta `flake8 .` y `mypy . --strict`

### Instrucciones adicionales
- Usa (sin subirlo al repositorio) programas de testeo para verificar que todo funcione. *pytest* o *unittest*.
- Incluye un *.gitignore*
- Es recomendado el uso de entornos virtuales(venv o conda) para el aislamiento de dependencias durante el desarrollo.

# Parte obligatoria
### Sinopsis
Implementarás un generador de laberintos en Python que coja un archivo de configuración, genera un laberinto, posiblemente perfecto (una única ruta entre entrada y salida), y lo escribe en un documento usando representación de muro hexadecimal. También harás una representación visual del laberinto y organizaras tu código para que la lógica de generación sea usable más tarde.

### Uso
El programa se ejecutará con la siguiente linea por terminal:
`python3 a_maze_ing.py config.txt`
- `a_maze_ing.py` - script principal del programa.
- `config.txt` - Es el único argumento a detectar. Es texto plano que define las opciones de generación. (el nombre del archivo puede variar).
Tu programa deberá de gestionar los errores sin explotar. No debe creshear en ningún momento y deberá de dar un error claro al usuario.
#### El archivo de configuración
El archivo deberá contener una pareja 'KEY = VALUE' por línea.
Las lineas que empiecen por #, son omitidas
Las siguientes keys son obligatorias en este archivo:

| Key         | Descripción                             |
| ----------- | --------------------------------------- |
| WIDTH       | Maze width<br>(number of cells)         |
| HEIGHT<br>  | Maze height                             |
| ENTRY       | Entry coordinates (x,y)                 |
| EXIT        | Exit coordinates (x,y)                  |
| OUTPUT_FILE | Output filename                         |
| PERFECT     | Is the maze Perfect?<br>(True or False) |
- Se pueden añadir keys adicionales si es necesario
- Un archivo de configuración base tiene que estar en el repositorio
### Requisitos del Laberinto
- Debe ser generado de forma aleatoria, pero reproductividad mediante una semilla es obligatoria.
- Cada celda del laberinto debe tener entre 0 y 4 paredes, en los puntos cardinales.
- El laberinto tiene ser valido, lo que significa:
	- La salida y entrada existen y son diferentes, dentro del laberinto.
	- La estructura se asegura de tener completa conectividad y sin celdas aisladas(menos del 42).
	-  Para la entrada y salida, debe de haber paredes en los bordes externos.
	- Los datos generados deben de ser coherentes: Cada celda vecina debe tener la misma pared si *Any*.
- El laberinto no debe de tener grandes áreas abiertas. Por ej, puedes tener un área de 2x3 o 3x2, pero no un 3x3. 
	- Los pasillos no pueden ser más largos de 2 celdas.
- Cuando sea representado de forma visual, el laberinto debe contener un "42" visible, formado por varias celdas cerradas.
- Si la bandera de "Perfect" está activa, el laberinto debe contener un único camino entre la entrada y la salida
- Si la bandera de "Perfect" **NO** está activada (opción predeterminada), el laberinto debe ser un tablero usable para un juego a lo Pac-Man, es decir:
	- Cada pasillo debe ser alcanzable (conectividad completa)
	- Las cuatro esquinas y el centro son pasillos abiertos.
	- Ofrece, mínimo, 2 rutas independientes (loops), permitiendo que el jugador tenga siempre una alternativa de escape.
	- Las calles sin salida deben de ser ocasionalmente raras de ver, (un par es aceptable).

Como error a controlar, si el laberinto es muy pequeño para albergar el 42, se debe imprimir un mensaje por pantalla avisandolo.
![[amazeing_example.png]]

### Formato archivo de salida
El laberinto generado debe de ser escrito en un archivo, usando un digito hexadecimal por cada celda, donde cada digito encapsula que paredes están cerradas

| Bit     | Dirección |
| ------- | --------- |
| 0 (LSB) | Norte     |
| 1       | Este      |
| 2       | Sur       |
| 3       | Oeste     |
- Un muro siendo cerrado establece el bit a 1, abierto significa 0. 
  Ej. 3 (binario 0011), significa que tiene abierto sur y oeste.
  Ej. A (binario 1010), significa que Este y Oeste están cerrados.
- Las celdas son almacenadas columna a columna, fila por línea en el archivo
- Después de una línea vacía, los 3 siguientes objetos se añaden en 3 lineas:
	- Las coordenadas de la entrada
	- Las coordenadas de la salida
	- El camino más corto desde la entrada a la salida, usando (N, E, S, W).
- Todas las líneas acaban en `\n`.
![[output_file_example.png]]

## Representación Visual
Tu programa debe proveer una forma de mostrar el laberinto visualmente, seguramente se use Renderizando en la terminal ASCII.
El visual debe mostrar de forma clara las paredes, la entrada y salida, y el camino de salida.

Las interacciones del usuario deben ser al menos:
- Regenerar un nuevo laberinto y mostrarlo por pantalla
- Mostrar/Esconder el camino más corto Entrada-Salida
- Cambiarle el color a las paredes
- Opcional: Establecer un color especifico para mostrar el patrón "42"
Pueden añadirse más funciones si se quiere

![[Ejemplo de visualización.png]]

## Requerimientos para la reusabilidad del código
- Debe implementarse la generación del Laberinto como una clase única, dentro de un módulo por separado, permitiendo que pueda ser importado en un futuro proyecto.
- Se debe hacer una documentación que describa:
	- Ejemplificar y usar el generador, con al menos un ejemplo básico.
	- Cómo pasan los parámetros personalizados (semilla, tamaño, etc)
	- Acceder a la estructura generada, y como acceder a al menos una solución
El módulo del generador de laberintos da acceso a la estructura del mismo, pero, no es necesario que sea el mismo formato que el archivo de salida.

Este módulo completo(código y documentación) debe estar disponible en un único archivo apropiado para una posterior instalación vía `pip`.
Este paquete se deberá llamar `mazegen-*` y el archivo debe de estar ubicado en la raíz del repositorio de Git.
- Tanto las extensiones `.tar.gz` como `.whl` están permitidas.
Ejemplo del nombre para el archivo: `mazegen-1.0.0-py3-none-any.whl`

Se debe proporcionar en tu repositorio todos los elementos necesarios para construir el paquete.
- En un entorno virtual, o similar, deberéis instalar las herramientas necesarias y construir el paquete, de nuevo, a partir de tus recursos.

Debido a que el generador de laberintos será necesario en futuros proyectos, debes incluir un *LICENSE.md*, en la raíz de tu repo, estableciendo que tu código será posiblemente re-usado.
La licencia que elijas debe permitir el "reuso" y distribución de tu generador.

El archivo *README.md* debe de incluir una breve descripción.