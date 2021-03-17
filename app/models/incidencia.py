from odmantic import Model
from pydantic import EmailStr

class Incidencia(Model):
    titulo: str
    cuerpo: str
    email_origen: EmailStr
    email_destino: EmailStr
    
