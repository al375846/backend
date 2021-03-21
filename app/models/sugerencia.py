from odmantic import Model


class Sugerencia(Model):
    identificador: str
    contenido: str
    resolucion: bool
