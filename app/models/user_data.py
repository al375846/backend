from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    nombre: str
    apellidos: str
    username: str
    email: EmailStr
    telefono: str
