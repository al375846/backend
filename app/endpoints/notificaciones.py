from app.enums.medicion import TipoMedicion
from app.models.notificacion import Notificacion
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

