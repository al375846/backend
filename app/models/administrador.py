from datetime import datetime

from pydantic.networks import EmailStr

from odmantic import Model


class Administrador(Model):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str
    username: str
    password: str
    fecha_contratacion: datetime
