from datetime import datetime
from typing import Optional
from app.enums.suscripcion import TipoSuscripcion
from odmantic import Field,EmbeddedModel


class Suscripcion(EmbeddedModel):
    tipo: TipoSuscripcion
    fecha_ini: datetime
    fecha_fin: Optional[datetime] = Field(None)
    

