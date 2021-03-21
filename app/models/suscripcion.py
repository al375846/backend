from datetime import datetime
from typing import Optional

from odmantic import Field, EmbeddedModel

from app.enums.suscripcion import TipoSuscripcion


class Suscripcion(EmbeddedModel):
    tipo: TipoSuscripcion
    fecha_ini: datetime
    fecha_fin: Optional[datetime] = Field(None)
