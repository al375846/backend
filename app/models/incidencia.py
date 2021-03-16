from app.models.db_base import DbBase
from pydantic import EmailStr

class Incidencia(DbBase):
    titulo: str
    cuerpo: str
    email_origen: EmailStr
    email_destino: EmailStr
    
