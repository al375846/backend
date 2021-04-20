from app.models.administrador import Administrador
from typing import List
from app.utils.security import get_current_admin
from fastapi.params import Depends
from app.enums.medicion import TipoMedicion
from app.models.notificacion import Notificacion, NotificacionAdmin, NotificacionAdminRet
from odmantic import ObjectId
from app.db.db import db
from app.config import FIREBASE_TOKEN

from pyfcm import FCMNotification
from fastapi import APIRouter

router = APIRouter(prefix="/notificaciones",
                   tags=["notificaciones"])

push_service = FCMNotification(api_key=FIREBASE_TOKEN)

@router.get("/notify")
async def push(id:ObjectId):
    notification = await db.motor.find_one(Notificacion,Notificacion.id == id)
    tokens = notification.establecimiento.gerente.phone_tokens
    if len(tokens) > 0:
        # Send to multiple devices by passing a list of ids.
        message_title = "Alerta"
        message_body= "Alerta"
        if notification.tipo_medicion == TipoMedicion.aforo:
            message_title = f"Alerta aforo - {notification.establecimiento.descriptor}"
            message_body = f"Se ha superado el aforo máximo.\n Aforo actual: {notification.contenido}"
        if notification.tipo_medicion == TipoMedicion.aire:
            message_title = f"Alerta aire - {notification.establecimiento.descriptor}"
            message_body = f"Se han superado los límites de CO2 recomendados.\n Nivel actual: {notification.contenido}"
        if notification.tipo_medicion == TipoMedicion.distancia:
            message_title = f"Alerta distancia - {notification.establecimiento.descriptor}"
            message_body = f"Se han superado la distáncia entre personas."            
        result = push_service.notify_multiple_devices(registration_ids=tokens, message_title=message_title, message_body=message_body)
        print(result)


@router.get("/admin", response_model=List[NotificacionAdminRet])
async def listado_notificaciones_admin(admin: Administrador = Depends(get_current_admin)):
    listado = await db.motor.find(NotificacionAdmin,NotificacionAdmin.responsable == admin.id)
    #listado = list(map(lambda x: NotificacionAdminRet(**x.dict()),listado))
    return listado

