from app.enums.tipo_notificacion import TipoNotificacion
from app.models.notificacion import Notificacion, NotificacionAdmin
from app.config import FIREBASE_TOKEN
from pyfcm.fcm import FCMNotification
from app.models.generic_respones import BasicReturn
from typing import List, Optional

from fastapi import HTTPException, APIRouter, Depends, Body
from pydantic import EmailStr
from starlette import status
from random import randint

from app.db.db import db
from app.models.administrador import Administrador
from app.models.gerente import Gerente, ResGerente
from app.models.registro import Registro, ExistsEmail, ExistsEmailRequest
from app.models.user_data import UpdateUser, UserData
from app.utils.security import encripta_pwd, get_current_admin, get_current_gerente
from app.utils.validation import existe_email

router = APIRouter(prefix="/gestion", tags=["Gestión"])

push_service = FCMNotification(api_key=FIREBASE_TOKEN)


@router.post("/registra_gerente", response_model=ResGerente)
async def registro_gerente(gerente: Registro, _=Depends(get_current_admin)):
    if await existe_email(gerente.email):
        raise HTTPException(detail="email repetido",
                            status_code=status.HTTP_409_CONFLICT)
    gerente.password = encripta_pwd(gerente.password)
    gdb = Gerente(**gerente.dict())
    await db.motor.save(gdb)
    return gdb


@router.put("/edita_gerente", response_model=ResGerente)
async def edita_gerente(gerente: UpdateUser,
                        current: Gerente = Depends(get_current_gerente)):
    if gerente.nombre is not None:
        current.nombre = gerente.nombre
    if gerente.apellidos is not None:
        current.apellidos = gerente.apellidos
    if gerente.telefono is not None:
        current.telefono = gerente.telefono
    await db.motor.save(current)
    return current


@router.post("/registra_administrador", response_model=Administrador)
async def registro_administrador(admin: Registro,
                                 _=Depends(get_current_admin)):
    if await existe_email(admin.email):
        raise HTTPException(detail="email repetido",
                            status_code=status.HTTP_409_CONFLICT)
    admin.password = encripta_pwd(admin.password)
    gdb = Administrador(**admin.dict())
    await db.motor.save(gdb)
    return gdb


@router.delete("/baja_gerente", response_model=UserData)
async def baja_gerente(email_baja: EmailStr, _=Depends(get_current_admin)):
    gerente = await db.motor.find_one(Gerente, Gerente.email == email_baja)
    if gerente is None:
        raise HTTPException(detail="Usuario no existe",
                            status_code=status.HTTP_404_NOT_FOUND)
    await db.motor.delete(gerente)
    return gerente


@router.post("/solicita_baja", response_model=BasicReturn)
async def solicita_baja_gerente(
        gerente: Gerente = Depends(get_current_gerente)):

    solicitudes = await db.motor.find(NotificacionAdmin, {+NotificacionAdmin.gerente : {"$eq":gerente.id}, +NotificacionAdmin.tipo :{ "$eq":TipoNotificacion.baja.value}})
    if len(solicitudes) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya se ha realizado una solicitud previamente.")
    admins = (await db.motor.find(Administrador))
    ind = randint(0, len(admins) - 1)
    responsable = admins[ind]
    solicitud = NotificacionAdmin(responsable=responsable,
                                  gerente=gerente,
                                  tipo=TipoNotificacion.baja)
    await db.motor.save(solicitud)

    if len(responsable.phone_tokens) > 0:
        message_title = "Nueva solicitud baja"
        message_body = f"El usuario con email {gerente.email} ha solicitado darse de baja."

        result = push_service.notify_multiple_devices(
            registration_ids=responsable.phone_tokens,
            message_title=message_title,
            message_body=message_body)
        print(result)
    return BasicReturn()


@router.delete("/baja_admin", response_model=UserData)
async def baja_admin(email_baja: EmailStr, _=Depends(get_current_admin)):
    admin = await db.motor.find_one(Administrador,
                                    Administrador.email == email_baja)
    if admin is None:
        raise HTTPException(detail="Usuario no existe",
                            status_code=status.HTTP_404_NOT_FOUND)
    await db.motor.delete(admin)
    return admin


@router.post("/existe_email", response_model=ExistsEmail)
async def email_en_uso(email: ExistsEmailRequest = Body(...)) -> ExistsEmail:
    return ExistsEmail(exists=await existe_email(email.email))


@router.get("/gerentes", response_model=List[UserData])
async def get_gerentes(salta: int = 0,
                       limite: Optional[int] = None,
                       _=Depends(get_current_admin)):
    gerentes = list(await db.motor.find(Gerente, skip=salta, limit=limite))
    return gerentes
