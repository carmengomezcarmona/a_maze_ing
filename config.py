
# config.py (El libro de instrucciones)
# Qué es?: El lector del archivo config.txt.
# Para qué sirve: Lee lo que tú le pidas en el texto
# (por ejemplo, "quiero un mapa de 10x10") y
# se lo explica al programa para que sepa las reglas antes de empezar


class Config:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def parse(self) -> dict:
        # Esqueleto básico: devolverá las reglas leídas del archivo
        return {}
