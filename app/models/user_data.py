from typing import Optional
from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    nombre: str
    apellidos: str
    username: str
    email: EmailStr
    telefono: str

class UpdateUser(BaseModel):
    nombre: Optional[str]
    apellidos: Optional[str]
    email: Optional[EmailStr]
    telefono: Optional[str]

class LoginData(BaseModel):
    email: EmailStr
    password: str
