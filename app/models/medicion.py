from datetime import datetime

from odmantic import EmbeddedModel


class Medicion(EmbeddedModel):
    identificador: str
    fecha: datetime = datetime.now()
    contenido: str