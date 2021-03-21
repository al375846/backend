from datetime import datetime
from typing import Optional

from odmantic import Model
from pydantic.main import BaseModel

from app.enums.tipodispositivo import TipoDispositivo


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
