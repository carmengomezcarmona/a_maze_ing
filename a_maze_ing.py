
# main.py (El director del juego)
# ¿Qué es?: El botón de encendido.
# Para qué sirve: Es el único archivo que tú ejecutas.
# Su trabajo es llamar al lector, luego al constructor,
# luego al detective y finalmente al artista, en el orden correcto.


from cell import Cell
from config import Config
from display import MazeDisplay
from maze import MazeGenerator
from solver import MazeSolver


def main() -> None:
    print("A-Maze-ing iniciado correctamente.")


if __name__ == "__main__":
    main()
