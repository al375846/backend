
from datetime import datetime
from odmantic import Model
class Medicion(Model):
    identificador: str
    fecha: datetime
    contenido: str