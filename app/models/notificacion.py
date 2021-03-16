from app.models.db_base import DbBase
from datetime import date
from pydantic import HttpUrl

class Notificacion(DbBase):
    fechaActivacion: date
    contenido: str
    leido: bool
    imagen: HttpUrl