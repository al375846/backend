from pydantic.main import BaseModel
from app.enums.tipo_notificacion import TipoNotificacion
from typing import Optional
from app.models.establecimiento import EstablecimientoDB
from app.models.administrador import Administrador
from app.models.gerente import ResGerente,Gerente
from datetime import datetime
from app.enums.medicion import TipoMedicion
from odmantic import Model, Reference


class Notificacion(Model):
    fechaActivacion: datetime = datetime.now()
    contenido: str
    tipo_medicion: TipoMedicion
    establecimiento: EstablecimientoDB = Reference()
    leido: bool = False

class NotificacionAdmin(Model):
    responsable: Administrador = Reference()
    gerente: Gerente = Reference()
    tipo:TipoNotificacion
    contenido: Optional[str]
    fecha: datetime = datetime.now()

class NotificacionAdminRet(Model):
    gerente: ResGerente = Reference()
    tipo:TipoNotificacion
    contenido: Optional[str]
    fecha: datetime 




