from pydantic.main import BaseModel
from app.models.suscripcion import Suscripcion
from pydantic.networks import EmailStr
from typing import List, Optional
from odmantic import Model
from pydantic import root_validator
from app.db.db import db


class Gerente(Model):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str
    password: str
    username: str
    suscripciones: Optional[List[Suscripcion]]




