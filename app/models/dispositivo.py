from app.enums.tipodispositivo import TipoDispositivo
from app.models.db_base import DbBase
from datetime import date


class Dispositivo(DbBase):
    modelo: str
    fechaRegistro: date
    activado: bool
    conectado: bool
    tipo: TipoDispositivo