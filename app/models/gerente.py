from typing import List, Optional

from odmantic import Model
from pydantic.networks import EmailStr

from app.models.suscripcion import Suscripcion


class Gerente(Model):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str
    password: str
    username: str
    suscripciones: Optional[List[Suscripcion]]

class ResGerente(Model):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str