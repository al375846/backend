from app.config import FIREBASE_TOKEN
from pyfcm.fcm import FCMNotification
from app.enums.tipo_notificacion import TipoNotificacion
from fastapi.param_functions import Depends
from fastapi import APIRouter, Body

from random import randint

from app.models.administrador import Administrador
from app.models.generic_respones import BasicReturn
from app.models.gerente import Gerente
from app.models.notificacion import NotificacionAdmin

from app.utils.security import get_current_gerente

from app.db.db import db


router = APIRouter(prefix="/sugerencia", tags=["sugerencia"])

push_service = FCMNotification(api_key=FIREBASE_TOKEN)


@router.post("", response_model=BasicReturn)
async def newSugerencia(
    contenido: str = Body(...,min_length=1,embed=True), gerente: Gerente = Depends(get_current_gerente)
):

    admins = await db.motor.find(Administrador)
    ind = randint(0, len(admins) - 1)
    responsable = admins[ind]
    solicitud = NotificacionAdmin(
        responsable=responsable,
        gerente=gerente,
        contenido=contenido,
        tipo=TipoNotificacion.sugerencia,
    )
    await db.motor.save(solicitud)

    if len(responsable.phone_tokens) > 0:
        message_title = "Nueva sujerencia"
        message_body = (
            f"El usuario con email {gerente.email} ha realizado una sujerencia."
        )

        push_service.notify_multiple_devices(
            registration_ids=responsable.phone_tokens,
            message_title=message_title,
            message_body=message_body,
        )
    return BasicReturn()
