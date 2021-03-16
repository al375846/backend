from app.models.db_base import DbBase
from pydantic import EmailStr
from datetime import date

class Medicion(DbBase):
    identificador: str
    fecha: date
    contenido: str