from odmantic import Model, Reference
from pydantic.main import BaseModel

from app.models.gerente import Gerente
from app.models.medicion import Medicion
from typing import List, Optional


class Establecimiento(BaseModel):
    descriptor: str
    direccion: str
    aforo: int


class EstablecimientoDB(Model):
    descriptor: str
    direccion: str
    aforo: int
    gerente: Gerente = Reference()
    mediciones: Optional[List[Medicion]] = []
