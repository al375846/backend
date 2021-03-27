from datetime import datetime

from odmantic import EmbeddedModel
from app.enums.medicion import TipoMedicion

class Medicion(EmbeddedModel):
    identificador: str
    fecha: datetime = datetime.now()
    contenido: str