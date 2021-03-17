from odmantic import Model

class Establecimiento(Model):
    identificador: str
    direccion: str
    aforo: int