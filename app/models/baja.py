from pydantic.main import BaseModel
from app.models.gerente import Gerente
from app.models.administrador import Administrador

from odmantic import Model, Reference

class SolicitudBaja(Model):
    responsable: Administrador = Reference()
    solicita: Gerente = Reference()

