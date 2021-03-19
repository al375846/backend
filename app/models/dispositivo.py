from app.enums.tipodispositivo import TipoDispositivo
from datetime import datetime
from odmantic import Model
from pydantic.main import BaseModel


class DispositivoDB(Model):
    modelo: str
    fechaRegistro: datetime
    activado: bool
    conectado: bool
    tipo: TipoDispositivo

class DispositivoCreate(BaseModel):
    modelo: str
    activado: bool
    conectado: bool
    tipo: TipoDispositivo