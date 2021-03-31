from app.models.establecimiento import EstablecimientoDB
from datetime import datetime
from app.enums.medicion import TipoMedicion
from odmantic import Model, Reference


class Notificacion(Model):
    fechaActivacion: datetime = datetime.now()
    contenido: str
    tipo_medicion: TipoMedicion
    establecimiento: EstablecimientoDB = Reference()
    leido: bool = False
    
