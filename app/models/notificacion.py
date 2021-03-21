from datetime import datetime

from odmantic import Model
from pydantic import HttpUrl


class Notificacion(Model):
    fechaActivacion: datetime
    contenido: str
    leido: bool
    imagen: HttpUrl
