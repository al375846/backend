from typing import List, Optional

from fastapi import HTTPException, APIRouter, Depends, Body
from pydantic import EmailStr
from starlette import status

from app.db.db import db
from app.models.administrador import Administrador
from app.models.gerente import Gerente
from app.models.registro import Registro, ExistsEmail, ExistsEmailRequest
from app.models.user_data import UserData
from app.utils.security import encripta_pwd, get_current_admin
from app.utils.validation import existe_email

router = APIRouter(prefix="/gestion",
                   tags=["Gestión"])


@router.post("/registra_gerente", response_model=Gerente)
async def registro_gerente(gerente: Registro):
    if await existe_email(gerente.email):
        raise HTTPException(detail="email repetido", status_code=status.HTTP_409_CONFLICT)
    gerente.password = encripta_pwd(gerente.password)
    gdb = Gerente(**gerente.dict())
    await db.motor.save(gdb)
    return gdb


@router.post("/registra_administrador", response_model=Administrador)
async def registro_administrador(admin: Registro, _=Depends(get_current_admin)):
    if await existe_email(admin.email):
        raise HTTPException(detail="email repetido", status_code=status.HTTP_409_CONFLICT)
    admin.password = encripta_pwd(admin.password)
    gdb = Administrador(**admin.dict())
    await db.motor.save(gdb)
    return gdb


@router.delete("/baja_gerente", response_model=UserData)
async def baja_gerente(email_baja: EmailStr, _=Depends(get_current_admin)):
    gerente = await db.motor.find_one(Gerente, Gerente.email == email_baja)
    if gerente is None:
        raise HTTPException(detail="Usuario no existe", status_code=status.HTTP_404_NOT_FOUND)
    await db.motor.delete(gerente)
    return gerente


@router.delete("/baja_admin", response_model=UserData)
async def baja_admin(email_baja: EmailStr, _=Depends(get_current_admin)):
    admin = await db.motor.find_one(Administrador, Administrador.email == email_baja)
    if admin is None:
        raise HTTPException(detail="Usuario no existe", status_code=status.HTTP_404_NOT_FOUND)
    await db.motor.delete(admin)
    return admin


@router.post("/existe_email", response_model=ExistsEmail)
async def email_en_uso(email: ExistsEmailRequest = Body(...)) -> ExistsEmail:
    return ExistsEmail(exists=await existe_email(email.email))


@router.get("/gerentes", response_model=List[UserData])
async def get_gerentes(salta: int = 0, limite: Optional[int] = None, _=Depends(get_current_admin)):
    gerentes = list(await db.motor.find(Gerente, skip=salta, limit=limite))
    return gerentes
