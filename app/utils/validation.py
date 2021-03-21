from pydantic import EmailStr

from app.db.db import db
from app.models.administrador import Administrador
from app.models.gerente import Gerente


async def existe_email(email: EmailStr):
    n1 = len(await db.motor.find(Administrador, Administrador.email == email))
    n2 = len(await db.motor.find(Gerente, Gerente.email == email))
    if n1 + n2 > 0:
        return True
    return False
