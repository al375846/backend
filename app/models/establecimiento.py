from odmantic import Model, Reference
from pydantic.main import BaseModel

from app.models.gerente import Gerente


class Establecimiento(BaseModel):
    descriptor: str
    direccion: str
    aforo: int


class EstablecimientoDB(Model):
    descriptor: str
    direccion: str
    aforo: int
    gerente: Gerente = Reference()
