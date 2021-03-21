from datetime import datetime

from odmantic import Model
from pydantic.networks import EmailStr


class Administrador(Model):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str
    username: str
    password: str
    fecha_contratacion: datetime = datetime.now()
