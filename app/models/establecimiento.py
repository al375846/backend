from odmantic import Model
from pydantic.main import BaseModel

class Establecimiento(BaseModel):
    descriptor: str
    direccion: str
    aforo: int

class EstablecimientoDB(Model):
    descriptor: str
    direccion: str
    aforo: int