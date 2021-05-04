from pydantic.main import BaseModel
from app.models.gerente import Gerente
from odmantic import Model, Reference


class Incidencia(Model):
    titulo: str
    cuerpo: str
    gerente: Gerente = Reference()
class NewIncidencia(BaseModel):
    titulo: str
    cuerpo: str
