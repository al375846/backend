from app.models.establecimiento import EstablecimientoDB
from datetime import datetime

from odmantic import Model, Reference
from pydantic import HttpUrl


class Notificacion(Model):
    fechaActivacion: datetime
    contenido: str
    establecimiento: EstablecimientoDB = Reference()
    leido: bool = False
    
