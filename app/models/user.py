from app.models.db_base import DbBase
from pydantic import EmailStr
from datetime import date


class User(DbBase):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str
    username: str
    password: str
