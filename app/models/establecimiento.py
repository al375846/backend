from typing import List
from bson import ObjectId
from odmantic import EmbeddedModel
from pydantic.main import BaseModel


class Establecimiento(BaseModel):
    descriptor: str
    direccion: str
    aforo: int


class EstablecimientoDB(EmbeddedModel):
    descriptor: str
    direccion: str
    aforo: int
    dispositivos: List[ObjectId]
