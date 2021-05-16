from pydantic.main import BaseModel
from app.enums.tipo_notificacion import TipoNotificacion
from typing import Optional
from app.models.establecimiento import EstablecimientoDB, EstablecimientoRet
from app.models.administrador import Administrador
from app.models.gerente import ResGerente,Gerente, ResGerenteBM
from datetime import datetime
from app.enums.medicion import TipoMedicion
from odmantic import Model, Reference


class Notificacion(Model):
    fechaActivacion: datetime = datetime.now()
    contenido: str
    tipo_medicion: TipoMedicion
    establecimiento: EstablecimientoDB = Reference()
    leido: bool = False
    id_img:Optional[str]

class NotificacionRet(Model):
    fechaActivacion: datetime = datetime.now()
    contenido: str
    tipo_medicion: TipoMedicion
    establecimiento: EstablecimientoRet = Reference()
    leido: bool = False

class NotificacionAdmin(Model):
    responsable: Administrador = Reference()
    gerente: Optional[str] 
    tipo:TipoNotificacion
    contenido: Optional[str]
    fecha: datetime = datetime.now()

class NotificacionAdminRet(BaseModel):
    gerente: Optional[ResGerenteBM]
    tipo:TipoNotificacion
    contenido: Optional[str]
    fecha: datetime 




