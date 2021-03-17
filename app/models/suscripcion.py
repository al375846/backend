from datetime import datetime
from typing import Optional
from app.enums.suscripcion import TipoSuscripcion
from odmantic import Model


class Suscripcion(Model):
    tipo: TipoSuscripcion
    fecha_ini: datetime
    fecha_fin: Optional[date] = Field(None)
    

