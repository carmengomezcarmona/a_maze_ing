
# maze.py (El constructor del laberinto)
# ¿Qué es?: El obrero que junta muchas casillas (Cell) para
# hacer el mapa entero.
# Para qué sirve: Agarra el tamaño que le dio config.py,
# crea una cuadrícula de casillas y tira las paredes
# necesarias para crear los caminos.

from cell import Cell


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = []

    def generate(self) -> None:
        pass
