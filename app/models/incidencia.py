from pydantic.main import BaseModel
from pydantic import Field
from app.models.gerente import Gerente
from odmantic import Model, Reference


class Incidencia(Model):
    cuerpo: str 
    titulo: str 
    gerente: Gerente = Reference()
class NewIncidencia(BaseModel):
    titulo: str = Field(...,min_length=1)
    cuerpo: str = Field(...,min_length=1)
