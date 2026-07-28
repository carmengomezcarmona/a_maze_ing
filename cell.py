
# cell.py (La casilla)
# ¿Qué es?: La plantilla para crear una sola casilla de tu laberinto.
# Para qué sirve: Le dice al ordenador cómo es una casilla por dentro:
# "Tengo 4 paredes (Norte, Sur, Este, Oeste) y
# de momento no me ha visitado nadie"


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False
