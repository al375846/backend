from datetime import date
from typing import Optional
from app.enums.suscripcion import TipoSuscripcion
from pydantic import BaseModel, Field


class Suscripcion(BaseModel):
    tipo: TipoSuscripcion
    fecha_ini: date
    fecha_fin: Optional[date] = Field(None)
    

