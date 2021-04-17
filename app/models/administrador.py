from datetime import datetime
from typing import List

from odmantic import Model
from pydantic.networks import EmailStr


class Administrador(Model):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str
    username: str
    password: str
    phone_tokens: List[str] = []
    fecha_contratacion: datetime = datetime.now()
