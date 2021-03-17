from app.enums.tipodispositivo import TipoDispositivo
from datetime import datetime
from odmantic import Model


class Dispositivo(Model):
    modelo: str
    fechaRegistro: datetime
    activado: bool
    conectado: bool
    tipo: TipoDispositivo