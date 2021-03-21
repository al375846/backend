from app.enums.tipodispositivo import TipoDispositivo
from datetime import datetime
from odmantic import Model, Reference
from pydantic.main import BaseModel
from app.models.establecimiento import EstablecimientoDB
from typing import Optional


class DispositivoDB(Model):
    modelo: str
    fechaRegistro: datetime = datetime.now()
    activado: bool
    conectado: bool
    tipo: TipoDispositivo
    establecimiento: Optional[str] = None

class DispositivoCreate(BaseModel):
    modelo: str
    activado: bool
    conectado: bool
    tipo: TipoDispositivo