from app.models.generic_respones import BasicReturn
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from app.models.establecimiento import Establecimiento, EstablecimientoDB
from app.models.gerente import Gerente
from app.models.administrador import Administrador
from typing import List
from app.utils.security import get_current_admin, get_current_gerente
from fastapi.params import Depends
from app.enums.medicion import TipoMedicion
from app.models.notificacion import Notificacion, NotificacionAdmin, NotificacionAdminRet, NotificacionRet
from odmantic import ObjectId
from app.db.db import db
from app.config import FIREBASE_TOKEN

from pyfcm import FCMNotification
from fastapi import APIRouter, HTTPException,status

router = APIRouter(prefix="/notificaciones", tags=["notificaciones"])

push_service = FCMNotification(api_key=FIREBASE_TOKEN)


@router.get("/notify")
async def push(id: ObjectId):
    notification = await db.motor.find_one(Notificacion, Notificacion.id == id)
    tokens = notification.establecimiento.gerente.phone_tokens
    if len(tokens) > 0:
        # Send to multiple devices by passing a list of ids.
        message_title = "Alerta"
        message_body = "Alerta"
        if notification.tipo_medicion == TipoMedicion.aforo:
            message_title = f"Alerta aforo - {notification.establecimiento.descriptor}"
            message_body = f"Se ha superado el aforo máximo.\n Aforo actual: {notification.contenido}"
        if notification.tipo_medicion == TipoMedicion.aire:
            message_title = f"Alerta aire - {notification.establecimiento.descriptor}"
            message_body = f"Se han superado los límites de CO2 recomendados.\n Nivel actual: {notification.contenido}"
        if notification.tipo_medicion == TipoMedicion.distancia:
            message_title = f"Alerta distancia - {notification.establecimiento.descriptor}"
            message_body = f"Se han superado la distáncia entre personas."
        result = push_service.notify_multiple_devices(
            registration_ids=tokens,
            message_title=message_title,
            message_body=message_body)
        print(result)


@router.get("/admin", response_model=List[NotificacionAdminRet])
async def listado_notificaciones_admin(
        admin: Administrador = Depends(get_current_admin)):
    listado = await db.motor.find(NotificacionAdmin,
                                  NotificacionAdmin.responsable == admin.id)
    #listado = list(map(lambda x: NotificacionAdminRet(**x.dict()),listado))
    res = sorted(listado,key=lambda x: x.fecha)
    res = list(reversed(res))
    ids = {ObjectId(g.gerente) for g in res}
    gecoll = db.motor.get_collection(Gerente)

    docs = await gecoll.find({
        '_id': {
            "$in": list(ids)
        }
    }).to_list(length=None)

    gerentes = {str(g['_id']):Gerente(**g) for g in docs}
    print(list(ids))
    print(gerentes)
    res = [NotificacionAdminRet(gerente=gerentes.get(b.gerente),tipo = b.tipo, contenido = b.contenido,fecha = b.fecha) for b in res]

    return res


@router.get("/gerente", response_model=List[NotificacionRet])
async def listado_notificaciones_gerente(
        gerente: Gerente = Depends(get_current_gerente)):
    establecimietos = await db.motor.find(
        EstablecimientoDB, EstablecimientoDB.gerente == gerente.id)
    dict_establecimientos = {est.id: est for est in establecimietos}
    noticoll = db.motor.get_collection(Notificacion)
    docs = await noticoll.find({
        +Notificacion.establecimiento: {
            "$in": list(dict_establecimientos.keys())
        }
    }).to_list(length=None)
    listado = []
    for doc in docs:
        est = dict_establecimientos[doc['establecimiento']]
        del doc['establecimiento']
        listado.append(Notificacion(establecimiento=est,id=doc['_id'], **doc))
        
    listado = sorted(listado, key=lambda x: x.fechaActivacion)
    listado.reverse()
    return listado

@router.post("/gerente/leido", response_model=BasicReturn)
async def notificacion_leida(idn:ObjectId,
        gerente: Gerente = Depends(get_current_gerente)):
    notificacion = await db.motor.find_one(Notificacion,Notificacion.id == idn)

    if notificacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No existe notificación")
    
    if notificacion.establecimiento.gerente.id != gerente.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Notificacion no en propiedad")
    
    notificacion.leido = True
    await db.motor.save(notificacion)
    return BasicReturn()

